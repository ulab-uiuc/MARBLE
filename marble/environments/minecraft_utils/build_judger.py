import argparse
import json
import os
import shutil
import threading

import numpy as np
from javascript import On, require

from marble.environments.minecraft_utils.utils import *

parser = argparse.ArgumentParser()
parser.add_argument('--idx', type=int, default=0, help='the index of the building to be judged')
parser.add_argument('--mc_version', type=str, default="1.19.2", help='the version of minecraft')
parser.add_argument('--agent_num', type=int, default=1, help='how many agents in the test')
parser.add_argument('--host', type=str, default="localhost", help='the host of the server')
parser.add_argument("--port", type=int, default=25565, help="the port of the server")
parser.add_argument('--dig_needed', type=bool, default=False, help='whether use tools dig blocks')
parser.add_argument("--agent_names", type=str, default="", help="the name of the agents in A,B,C format")
parser.add_argument("--task_name", type=str, default="test", help="the name of the task")

args = parser.parse_args()
select_idx = args.idx
agent_num = args.agent_num
dig_needed = args.dig_needed
agent_names = args.agent_names.split(",")
task_name = args.task_name

with open(".cache/load_status.cache", "w") as f:
    json.dump({"status": "loading"}, f, indent=4)

if not os.path.exists("result"):
    os.makedirs("result")

mineflayer = require('mineflayer')
Vec3 = require("vec3")
minecraftData = require('minecraft-data')
mcData = minecraftData(args.mc_version)

y_b = -60
bot = mineflayer.createBot({
    "host": args.host,
    "port": args.port,
    'username': "build_judge",
    'checkTimeoutInterval': 600000,
    'auth': 'offline',
    'version': "1.19.2",
})

### reset the environments
last_time = time.time()
start_time = None
task_data = None
with open("data/score.json", "w") as f:
    json.dump([], f, indent=4)

complexity = 0
max_action_time = 0
max_time = 0

# metric
block_hit_rate = 0
view_hit_rate = 0
efficiency = 0

# time 
last_update_time = time.time()
wait_interval = 600
max_block_hit_rate = 0

if not os.path.exists('data/blueprint_description_all.json'):
    with open('data/blueprint_description_all.json', 'w') as f:
        json.dump({}, f, indent=4)

def calculate_balance():
    # 计算每个agent的时间
    if not os.path.exists('data/action_log.json'):
        return
    with open('data/action_log.json', 'r') as f:
        data = json.load(f)
    agent_time = []
    for name, actions in data.items():
        total_time = 0
        for action in actions:
            total_time += action['duration']
        agent_time.append(total_time)
    for i in range(agent_num - len(agent_time)):
        agent_time.append(0)
    time_array = np.array(agent_time)
    
    # 对时间进行归一化处理
    time_array = (time_array - np.min(time_array)) / (np.max(time_array) - np.min(time_array) + 1e-8)
    
    # 计算并返回 Balanced Agent Utilization Score (BAUS)
    return 1 - np.sqrt(np.sum((time_array - np.mean(time_array))**2)) / (len(time_array) * np.mean(time_array) + 1e-8)

def measure_complexity(data, height_weight=0.02, dig_needed=False):
    blocks = data['blocks']
    complexity = 0
    ground_level = min(block['position'][1] for block in blocks) - 1
    dig_num = 0
    for block in blocks:
        x, y, z = block['position']

        if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
            continue

        if dig_needed:
            if 'log' in block['name'] or 'stone' in block['name']:
                dig_num += 1
        # Check for neighbors in all six directions
        connect_paths = []
        for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            if any(b['position'] == [x + dx, y + dy, z + dz] for b in blocks):
                connect_paths.append([dx, dy, dz])

        # Count the ground as a neighbor
        if y == ground_level:
            connect_paths.append([0, -1, 0])

        # facing W, E, S, N,(5/6) x, y, z,(2/6) A (6/6)
        filter_paths = []
        for path in connect_paths:
            if block["facing"] == "W":
                if path == [-1, 0, 0]:
                    continue
            elif block["facing"] == "E":
                if path == [1, 0, 0]:
                    continue
            elif block["facing"] == "S":
                if path == [0, 0, -1]:
                    continue
            elif block["facing"] == "N":
                if path == [0, 0, 1]:
                    continue
            elif block["facing"] == "x":
                if path != [0, -1, 0] and path != [0, 1, 0]:
                    continue
            elif block["facing"] == "y":
                if path != [-1, 0, 0] and path != [1, 0, 0]:
                    continue
            elif block["facing"] == "z":
                if path != [0, 0, -1] and path != [0, 0, 1]:
                    continue

            filter_paths.append(path)
        connect_paths = filter_paths

        # Add to the complexity score, weighting by height
        complexity += (1 / (len(connect_paths) + 1) + (y - ground_level) * height_weight) * 2  # at least two actions
    if dig_needed:
        complexity += dig_num * 1  # at least one action dig

    return complexity

def json_to_string_list(json_data):
    string_list = []

    def process_element(element):
        res = ""
        if isinstance(element, dict):
            for key, value in element.items():
                res += f"{key}:" + process_element(value) + ' '
            res = res[:-1]
        elif isinstance(element, list):
            res += '['
            for idx, item in enumerate(element):
                res += process_element(item) + ' '
            res = res[:-1] + ']'
        else:
            res += str(element)
        return res

    for data in json_data:
        if isinstance(data, str):
            string_list.append(data)
        else:
            string_list.append(process_element(data))

    return string_list

@On(bot, 'spawn')
def handleViewer(*args):

    for name in agent_names:
        bot.chat(f'/op {name}')
        time.sleep(.2)

    def render(data, x_bias=0, y_bias=-60, z_bias=0):
        for b in data["blocks"]:
            time.sleep(.1)
            x, y, z = b["position"][0] + x_bias, b["position"][1] + y_bias, b["position"][2] + z_bias
            if b["facing"] in ["W", "E", "S", "N"]:
                cvt = {"W": "west", "E": "east", "S": "south", "N": "north"}
                bot.chat(f'/setblock {x} {y} {z} {b["name"]}[facing={cvt[b["facing"]]}]')
            elif b["facing"] in ["x", "y", "z"]:
                bot.chat(f'/setblock {x} {y} {z} {b["name"]}[axis={b["facing"]}]')
            elif b["facing"] == "A":
                bot.chat(f'/setblock {x} {y} {z} {b["name"]}')

    def clear(data, x_bias=0, y_bias=-60, z_bias=0):
        for b in data["blocks"]:
            x, y, z = b["position"][0] + x_bias, b["position"][1] + y_bias, b["position"][2] + z_bias
            # time.sleep(.01)
            bot.chat(f'/setblock {x} {y} {z} air')

    def core(select_idx):
        with open("data/building_blue_print.json", 'r') as f:
            blue_prints = json.load(f)

        # select_idx, select_idx-1, select_idx+1 clear and render
        # time.sleep(2)
        # don't render for high speed
        # render(blue_prints[select_idx], blue_prints[select_idx]["size"][0] // 2 + 4, y_b + 30, 0)
        bot.chat(f"/setblock -3 {y_b + 2} 0 minecraft:oak_wall_sign[facing=west]")

        bot.chat(f"/data merge block {-3} {y_b + 2} {0} " +
                 "{Text2:'{\"text\":\"" + blue_prints[select_idx]['name'] + "\",\"color\":\"blue\"}'}")

        task(blue_prints[select_idx])

        with open(".cache/load_status.cache", "w") as f:
            json.dump({"status": "loaded"}, f, indent=4)

        global start_time
        start_time = time.time()

    def task(data):
        global task_data
        task_data = data.copy()

        bot.chat(f'/setblock -4 {y_b} 0 chest[facing=west]')
        # set small house
        bot.chat(f'/setblock -4 {y_b} -1 minecraft:crafting_table')
        bot.chat(f'/setblock -4 {y_b} 1 minecraft:furnace[facing=west]')
        bot.chat(f'/setblock -4 {y_b} -2 minecraft:spruce_planks')
        bot.chat(f'/setblock -4 {y_b} 2 minecraft:spruce_planks')
        bot.chat(f'/fill -3 {y_b} -3 -3 {y_b + 1} 3 minecraft:spruce_planks')
        # set fence
        bot.chat(f'/setblock -4 {y_b} -3 minecraft:spruce_fence')
        bot.chat(f'/setblock -4 {y_b} 3 minecraft:spruce_fence')

        blocks_list = []
        for b in task_data["blocks"]:
            if b["name"] == "air" or b["name"] == "water" or b["name"] == "lava":
                continue
            b["position"][0] += -task_data["size"][0] // 2 - 8
            b["position"][1] += y_b
            blocks_list.append(b)
        task_data["blocks"] = blocks_list
        with open("data/map.json", 'w') as f:
            json.dump(task_data, f, indent=4)

        if dig_needed:
            material_pairs = material_factory_load('data/map.json', bot, Vec3, mcData, center_pos=(-12, -60, -12), rate=.5)
        time.sleep(2)
        building_material_load('data/map.json', bot, dig_needed=dig_needed)
        bot.chat(f"/time set 0")

        with open("data/blueprint_description_all.json", 'r') as f:
            blueprint_description_all = json.load(f)

        assert "task_" + str(select_idx) in blueprint_description_all.keys()

        string_list = blueprint_description_all["task_" + str(select_idx)]
        with open('data/map_description.json', 'w') as f:
            json.dump(string_list, f, indent=4)
        global complexity, max_action_time, max_time
        complexity = measure_complexity(task_data, dig_needed=dig_needed)
        bot.chat(f" complexity {complexity}") # 1 - 1000
        max_action_time = (np.log(complexity) + 1) * 60 + 180
        max_time = (np.log(complexity) + 1) * 180 + 600

    def check_block(Block, block_dict):
        if Block["name"] == "air" or Block["name"] == "water" or Block["name"] == "lava":
            return False
        if Block["name"] == block_dict["name"]:
            if "facing" not in block_dict.keys() or block_dict["facing"] == "A":
                return True
            if Block._properties["facing"] and block_dict["facing"] in ["W", "E", "S", "N"]:
                if Block._properties["facing"] == "east" and block_dict["facing"] == "E":
                    return True
                if Block._properties["facing"] == "west" and block_dict["facing"] == "W":
                    return True
                if Block._properties["facing"] == "south" and block_dict["facing"] == "S":
                    return True
                if Block._properties["facing"] == "north" and block_dict["facing"] == "N":
                    return True
            if Block._properties["axis"] and block_dict["facing"] in ["x", "y", "z"]:
                if Block._properties["axis"] == "x" and block_dict["facing"] == "x":
                    return True
                if Block._properties["axis"] == "y" and block_dict["facing"] == "y":
                    return True
                if Block._properties["axis"] == "z" and block_dict["facing"] == "z":
                    return True
        return False

    def cal_block_hit_rate(data):
        hit_num = 0
        total_num = 0
        for block in data["blocks"]:
            if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                continue
            total_num += 1
            b = bot.blockAt(Vec3(block["position"][0], block["position"][1], block["position"][2]))
            if check_block(b, block):
                hit_num += 1

        if total_num == 0:
            return 1

        return hit_num * 1. / total_num

    def cal_view_hit_rate(data):
        hit_rate_list = []
        # 从五个视角看，每个视角看到的方块与data中的方块的交并比
        x_min, y_min, z_min = 100000, 100000, 100000
        for block in data["blocks"]:
            x_min = min(x_min, block["position"][0])
            y_min = min(y_min, block["position"][1])
            z_min = min(z_min, block["position"][2])

        # 正面
        view_blocks_map = []
        for delta_y in range(data['size'][1] + 1):
            view_blocks_line = []
            for delta_z in range(data['size'][2] + 1):
                view_blocks_line.append({"x": -100000, "name": "air"})
            view_blocks_map.append(view_blocks_line)
        for block in data["blocks"]:
            if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                continue
            delta_y = block["position"][1] - y_min
            delta_z = block["position"][2] - z_min
            if view_blocks_map[delta_y][delta_z]["x"] < block["position"][0]:
                view_blocks_map[delta_y][delta_z]["x"] = block["position"][0]
                view_blocks_map[delta_y][delta_z]["name"] = block["name"]
        hit_num = 0
        total_num = 0
        for delta_y in range(data['size'][1] + 1):
            for delta_z in range(data['size'][2] + 1):
                if view_blocks_map[delta_y][delta_z]["name"] == "air" or view_blocks_map[delta_y][delta_z][
                    "name"] == "water" or \
                        view_blocks_map[delta_y][delta_z]["name"] == "lava":
                    continue
                total_num += 1
                for x in range(data['size'][0], -1, -1):
                    block = bot.blockAt(Vec3(x_min + x, y_min + delta_y, z_min + delta_z))
                    if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                        continue
                    if check_block(block, view_blocks_map[delta_y][delta_z]):
                        hit_num += 1
                    break
        hit_rate_list.append(hit_num * 1. / total_num)

        # 右面
        view_blocks_map = []
        for delta_x in range(data['size'][0] + 1):
            view_blocks_line = []
            for delta_y in range(data['size'][1] + 1):
                view_blocks_line.append({"z": 100000, "name": "air"})
            view_blocks_map.append(view_blocks_line)
        for block in data["blocks"]:
            if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                continue
            delta_x = block["position"][0] - x_min
            delta_y = block["position"][1] - y_min
            if view_blocks_map[delta_x][delta_y]["z"] > block["position"][2]:
                view_blocks_map[delta_x][delta_y]["z"] = block["position"][2]
                view_blocks_map[delta_x][delta_y]["name"] = block["name"]
        hit_num = 0
        total_num = 0
        for delta_x in range(data['size'][0] + 1):
            for delta_y in range(data['size'][1] + 1):
                if view_blocks_map[delta_x][delta_y]["name"] == "air" or view_blocks_map[delta_x][delta_y][
                    "name"] == "water" or \
                        view_blocks_map[delta_x][delta_y]["name"] == "lava":
                    continue
                total_num += 1
                for z in range(data['size'][2] + 1):
                    block = bot.blockAt(Vec3(x_min + delta_x, y_min + delta_y, z_min + z))
                    if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                        continue
                    if block["name"] == view_blocks_map[delta_x][delta_y]["name"]:
                        hit_num += 1
                    break
        hit_rate_list.append(hit_num * 1. / total_num)

        # 左面
        view_blocks_map = []
        for delta_x in range(data['size'][0] + 1):
            view_blocks_line = []
            for delta_y in range(data['size'][1] + 1):
                view_blocks_line.append({"z": -100000, "name": "air"})
            view_blocks_map.append(view_blocks_line)
        for block in data["blocks"]:
            if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                continue
            delta_x = block["position"][0] - x_min
            delta_y = block["position"][1] - y_min
            if view_blocks_map[delta_x][delta_y]["z"] < block["position"][2]:
                view_blocks_map[delta_x][delta_y]["z"] = block["position"][2]
                view_blocks_map[delta_x][delta_y]["name"] = block["name"]
        hit_num = 0
        total_num = 0
        for delta_x in range(data['size'][0] + 1):
            for delta_y in range(data['size'][1] + 1):
                if view_blocks_map[delta_x][delta_y]["name"] == "air" or view_blocks_map[delta_x][delta_y][
                    "name"] == "water" or \
                        view_blocks_map[delta_x][delta_y]["name"] == "lava":
                    continue
                total_num += 1
                for z in range(data['size'][2], -1, -1):
                    block = bot.blockAt(Vec3(x_min + delta_x, y_min + delta_y, z_min + z))
                    if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                        continue
                    if block["name"] == view_blocks_map[delta_x][delta_y]["name"]:
                        hit_num += 1
                    break
        hit_rate_list.append(hit_num * 1. / total_num)

        # 背面
        view_blocks_map = []
        for delta_y in range(data['size'][1] + 1):
            view_blocks_line = []
            for delta_z in range(data['size'][2] + 1):
                view_blocks_line.append({"x": 100000, "name": "air"})
            view_blocks_map.append(view_blocks_line)
        for block in data["blocks"]:
            if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                continue
            delta_y = block["position"][1] - y_min
            delta_z = block["position"][2] - z_min
            if view_blocks_map[delta_y][delta_z]["x"] > block["position"][0]:
                view_blocks_map[delta_y][delta_z]["x"] = block["position"][0]
                view_blocks_map[delta_y][delta_z]["name"] = block["name"]
        hit_num = 0
        total_num = 0
        for delta_y in range(data['size'][1] + 1):
            for delta_z in range(data['size'][2] + 1):
                if view_blocks_map[delta_y][delta_z]["name"] == "air" or view_blocks_map[delta_y][delta_z][
                    "name"] == "water" or \
                        view_blocks_map[delta_y][delta_z]["name"] == "lava":
                    continue
                total_num += 1
                for x in range(data['size'][0] + 1):
                    block = bot.blockAt(Vec3(x_min + x, y_min + delta_y, z_min + delta_z))
                    if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                        continue
                    if block["name"] == view_blocks_map[delta_y][delta_z]["name"]:
                        hit_num += 1
                    break
        hit_rate_list.append(hit_num * 1. / total_num)

        # 上面
        view_blocks_map = []
        for delta_z in range(data['size'][2] + 1):
            view_blocks_line = []
            for delta_x in range(data['size'][0] + 1):
                view_blocks_line.append({"y": -100000, "name": "air"})
            view_blocks_map.append(view_blocks_line)
        for block in data["blocks"]:
            if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                continue
            delta_z = block["position"][2] - z_min
            delta_x = block["position"][0] - x_min
            if view_blocks_map[delta_z][delta_x]["y"] < block["position"][1]:
                view_blocks_map[delta_z][delta_x]["y"] = block["position"][1]
                view_blocks_map[delta_z][delta_x]["name"] = block["name"]
        hit_num = 0
        total_num = 0
        for delta_z in range(data['size'][2] + 1):
            for delta_x in range(data['size'][0] + 1):
                if view_blocks_map[delta_z][delta_x]["name"] == "air" or view_blocks_map[delta_z][delta_x][
                    "name"] == "water" or \
                        view_blocks_map[delta_z][delta_x]["name"] == "lava":
                    continue
                total_num += 1
                for y in range(data['size'][1], -1, -1):
                    block = bot.blockAt(Vec3(x_min + delta_x, y_min + y, z_min + delta_z))
                    if block["name"] == "air" or block["name"] == "water" or block["name"] == "lava":
                        continue
                    if block["name"] == view_blocks_map[delta_z][delta_x]["name"]:
                        hit_num += 1
                    break
        hit_rate_list.append(hit_num * 1. / total_num)

        hit_rate = sum(hit_rate_list) / len(hit_rate_list)
        return hit_rate

    
    time.sleep(.1)
    bot.chat(f'/tp @s -5 {y_b} 0')
    time.sleep(.1)
    bot.chat(f'/tp @e[type=player,gamemode=survival] @s')
    bot.chat(f'/clear @e[type=player,gamemode=survival]')
    bot.chat('/time set day')
    time.sleep(.1)
    bot.chat('/weather clear')
    time.sleep(.1)
    bot.chat('/gamerule doDaylightCycle false')
    time.sleep(.1)
    bot.chat('/gamemode spectator')
    time.sleep(.1)
    bot.chat('/kill @e[type=!minecraft:player]')
    bot.chat('/kill @e[type=!minecraft:player]')

    for y in range(y_b + 20, y_b - 1, -1):
        bot.chat(f"/fill 0 {y} -40 40 {y} 40 minecraft:air")
        time.sleep(.1)

    for y in range(y_b + 20, y_b - 1, -1):
        bot.chat(f"/fill -2 {y} -19 -40 {y} 19 minecraft:air")
        time.sleep(.1)

    # 更新地面
    bot.chat(f'/fill -19 {y_b - 1} -20 -5 {y_b - 2} 7 minecraft:stone_bricks')
    time.sleep(.1)
    bot.chat(f'/fill -19 {y_b} -20 -19 {y_b + 15} 7 minecraft:glass')
    time.sleep(.1)
    bot.chat(f'/fill -5 {y_b} -20 -5 {y_b + 15} 7 minecraft:glass')
    time.sleep(.1)
    bot.chat(f'/fill -19 {y_b} 7 -5 {y_b + 15} 7 minecraft:glass')
    time.sleep(.1)
    bot.chat(f'/fill -19 {y_b} -20 -5 {y_b + 15} -20 minecraft:glass')
    time.sleep(.1)
    bot.chat(f'/fill -5 {y_b} -4 -5 {y_b + 4} 4 minecraft:air')
    time.sleep(.1)
    bot.chat(f'/fill -2 {y_b} 4 -2 {y_b + 4} -4 minecraft:stone_bricks')
    time.sleep(.1)
    bot.chat(f'/fill -2 {y_b} 4 -5 {y_b + 4} 4 minecraft:stone_bricks')
    time.sleep(.1)
    bot.chat(f'/fill -2 {y_b} -4 -5 {y_b + 4} -4 minecraft:stone_bricks')
    time.sleep(.1)
    bot.chat(f'/fill -2 {y_b + 4} -4 -5 {y_b + 4} 4 minecraft:glass')
    time.sleep(.1)
    bot.chat(f'/clear @e[distance=..10,type=minecraft:player]')


    t = threading.Thread(target=core, args=(select_idx,))
    t.start()

    @On(bot, "time")
    def handle(this):
        def calculate_action_time():
            if not os.path.exists('data/action_log.json'):
                return 0
            with open('data/action_log.json', 'r') as f:
                data = json.load(f)
            time_list = []
            for name, actions in data.items():
                for action in actions:
                    start = time.mktime(time.strptime(action['start_time'], "%Y-%m-%d %H:%M:%S"))
                    end = time.mktime(time.strptime(action['end_time'], "%Y-%m-%d %H:%M:%S"))
                    time_list.append((start, end))
            if len(time_list) == 0:
                return 0

            # 计算覆盖的总时间
            total_time = 0  # 单位：秒
            time_list.sort(key=lambda x: x[0])  # 按照开始时间排序
            start, end = time_list[0]
            for i in range(1, len(time_list)):
                if time_list[i][0] < end:
                    end = max(end, time_list[i][1])
                else:
                    total_time += end - start
                    start, end = time_list[i]
            total_time += end - start

            return total_time
        
        # if int(time.time()) % 20 == 0:
        #     bot.chat(f'/tp @e[type=player,gamemode=survival] @s')

        global last_time, start_time, last_update_time, max_block_hit_rate
        global block_hit_rate, view_hit_rate, efficiency, wait_interval, complexity
        now_time = time.time()

        if now_time - last_time > 1:
            if block_hit_rate == 1 and view_hit_rate == 1:
                efficiency = max_action_time / calculate_action_time()
                bot.chat(f"finish {efficiency}")
                # 给出结束信号和写入文件
                if not os.path.exists(os.path.join("result", task_name)):
                    os.mkdir(os.path.join("result", task_name))
                else:
                    shutil.rmtree(os.path.join("result", task_name))
                    os.mkdir(os.path.join("result", task_name))
                with open(os.path.join(os.path.join("result", task_name), "score.json"), "w") as f:
                    json.dump({
                        "block_hit_rate": block_hit_rate,
                        "view_hit_rate": view_hit_rate,
                        "efficiency": efficiency,
                        "use_time": calculate_action_time(),
                        "end_reason": "complete task",
                        "complexity": complexity,
                        "end_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))
                    }, f, indent=4)
                shutil.move("data/action_log.json", os.path.join(os.path.join("result", task_name), "action_log.json"))
                shutil.move("data/tokens.json", os.path.join(os.path.join("result", task_name), "tokens.json"))
                with open(".cache/load_status.cache", "w") as f:
                    json.dump({"status": "end"}, f, indent=4)

            if start_time and now_time and calculate_action_time() > max_action_time and task_data:
                efficiency = 1
                bot.chat(f'time out')
                # 给出结束信号和写入文件
                if not os.path.exists(os.path.join("result", task_name)):
                    os.mkdir(os.path.join("result", task_name))
                else:
                    shutil.rmtree(os.path.join("result", task_name))
                    os.mkdir(os.path.join("result", task_name))
                with open(os.path.join(os.path.join("result", task_name), "score.json"), "w") as f:
                    json.dump({
                        "block_hit_rate": block_hit_rate,
                        "view_hit_rate": view_hit_rate,
                        "efficiency": efficiency,
                        "use_time": calculate_action_time(),
                        "end_reason": "action time out",
                        "complexity": complexity,
                        "end_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))
                    }, f, indent=4)
                with open(".cache/load_status.cache", "w") as f:
                    json.dump({"status": "end"}, f, indent=4)

            if start_time and now_time and now_time - start_time > max_time and task_data:
                action_time = calculate_action_time()
                if action_time == 0:
                    efficiency = 1
                else:
                    efficiency = max_action_time / action_time
                bot.chat(f'time out')
                # 给出结束信号和写入文件
                if not os.path.exists(os.path.join("result", task_name)):
                    os.mkdir(os.path.join("result", task_name))
                else:
                    shutil.rmtree(os.path.join("result", task_name))
                    os.mkdir(os.path.join("result", task_name))
                with open(os.path.join(os.path.join("result", task_name), "score.json"), "w") as f:
                    json.dump({
                        "block_hit_rate": block_hit_rate,
                        "view_hit_rate": view_hit_rate,
                        "efficiency": efficiency,
                        "use_time": calculate_action_time(),
                        "end_reason": "max time out",
                        "complexity": complexity,
                        "end_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))
                    }, f, indent=4)
                with open(".cache/load_status.cache", "w") as f:
                    json.dump({"status": "end"}, f, indent=4)

            if last_update_time and start_time and task_data and last_update_time - start_time > wait_interval and now_time - last_update_time > wait_interval:
                action_time = calculate_action_time()
                if action_time == 0:
                    efficiency = 1
                else:
                    efficiency = max_action_time / action_time
                bot.chat(f'time out')
                # 给出结束信号和写入文件
                if not os.path.exists(os.path.join("result", task_name)):
                    os.mkdir(os.path.join("result", task_name))
                else:
                    shutil.rmtree(os.path.join("result", task_name))
                    os.mkdir(os.path.join("result", task_name))
                with open(os.path.join(os.path.join("result", task_name), "score.json"), "w") as f:
                    json.dump({
                        "block_hit_rate": block_hit_rate,
                        "view_hit_rate": view_hit_rate,
                        "efficiency": efficiency,
                        "use_time": calculate_action_time(),
                        "end_reason": "no better score in wait interval",
                        "complexity": complexity,
                        "end_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))
                    }, f, indent=4)
                with open(".cache/load_status.cache", "w") as f:
                    json.dump({"status": "end"}, f, indent=4)

            with open(".cache/heart_beat.cache", "w") as f:
                json.dump({"time": now_time}, f, indent=4)

        if now_time - last_time > 10 and task_data:
            block_hit_rate = cal_block_hit_rate(task_data)
            if block_hit_rate > max_block_hit_rate:
                max_block_hit_rate = block_hit_rate
                last_update_time = time.time()

            view_hit_rate = cal_view_hit_rate(task_data)
            bot.chat(f' block_hit_rate: {block_hit_rate}')
            print(f' block_hit_rate: {block_hit_rate}')
            time.sleep(.1)
            bot.chat(f' view_hit_rate: {view_hit_rate}')
            print(f' view_hit_rate: {view_hit_rate}')
            time.sleep(.1)

            # bot.chat(f' complexity: {complexity}')

            with open("data/score.json", "r") as f:
                score = json.load(f)
            score.append(
                {"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "block_hit_rate": block_hit_rate,
                 "view_hit_rate": view_hit_rate})
            with open("data/score.json", "w") as f:
                json.dump(score, f, indent=4)

            last_time = now_time

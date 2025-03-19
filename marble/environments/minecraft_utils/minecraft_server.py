import argparse
import time
from functools import wraps
from math import floor
from random import choice, randint

import names
from flask import Flask, jsonify, request

from marble.environments.minecraft_utils.env_api import *

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
os.environ["REQ_TIMEOUT"] = "1800000"
app = Flask(__name__)
msg_list = []  # 用于存储消息队列，每次获取后清除当前的消息队列
# Pickable = False

parser = argparse.ArgumentParser()
parser.add_argument('-P', '--port', type=int, default=25565)
parser.add_argument('-H', '--host', type=str, default='localhost')
parser.add_argument('-U', '--username', type=str, default=names.get_full_name().replace(' ', '_'))
parser.add_argument('-W', '--worldname', type=str)
parser.add_argument('-LP', '--local_port', type=int, default=5000)
parser.add_argument('-D', '--debug', type=bool, default=False)
args = parser.parse_args()
local_port = args.local_port
print(f"Agent {args.username} login {args.worldname} at {args.host}:{args.port}")
# VIEW_PORT = 3000
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
collectBlock = require('mineflayer-collectblock')
pvp = require("mineflayer-pvp").plugin
minecraftHawkEye = require("minecrafthawkeye")
Vec3 = require("vec3")
# viewer = require('prismarine-viewer').mineflayer
Socks = require("socks5-client")
minecraftData = require('minecraft-data')
mcData = minecraftData('1.19.2')
# print(mcData.itemsByName['yellow_carpet'])
bot = mineflayer.createBot({
    "host": args.host,
    "port": args.port,
    'username': args.username.replace(' ', '_'),
    'checkTimeoutInterval': 60*60*1000,
    'auth': 'offline',
    'version': '1.19.2',
})
bot.loadPlugin(pathfinder.pathfinder)
bot.loadPlugin(collectBlock.plugin)
bot.loadPlugin(pvp)
bot.loadPlugin(minecraftHawkEye.default)

VISIBLE_ONLY = True # 是否只看到可见的方块 | False: 开金手指

# 定义修饰器
def log_activity(bot):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 在函数执行前打印
            # bot.chat(f"{bot.username} is going to do task: {func.__name__}")
            try:
                # 执行函数
                result = func(*args, **kwargs) # 这里可以增加更多的反馈信息
                # 在函数执行后打印(\1\n@log)
                # bot.chat(f"{bot.username} has done task: {func.__name__}")
                return result
            except Exception as e:
                # 如果发生异常，打印异常信息
                # bot.chat(f"{bot.username} Error in task: {func.__name__} - {str(e)}")
                raise e
        return wrapper
    return decorator

@app.route('/hello', methods=['GET'])
@log_activity(bot)
def hello_world():
    return 'Hello World!'


@app.route('/post_render', methods=['POST'])
@log_activity(bot)
def render_structure():
    """render_structure: render the structure."""
    data = request.get_json()
    id = data.get('id')
    center_pos = data.get('center_pos')
    try:
        with open("../minecraft/building_blue_print.json", "r") as f:
            structure_list = json.load(f)
        structure = structure_list[id]
        for b in structure["blocks"]:
            time.sleep(.05)
            x, y, z = b["position"][0] + center_pos[0], b["position"][1] + center_pos[1], b["position"][2] + center_pos[2]
            if b["facing"] in ["W", "E", "S", "N"]:
                cvt = {"W": "west", "E": "east", "S": "south", "N": "north"}
                bot.chat(f'/setblock {x} {y} {z} {b["name"]}[facing={cvt[b["facing"]]}]')
            elif b["facing"] in ["x", "y", "z"]:
                bot.chat(f'/setblock {x} {y} {z} {b["name"]}[axis={b["facing"]}]')
            elif b["facing"] == "A":
                bot.chat(f'/setblock {x} {y} {z} {b["name"]}')


    except Exception as e:
        return jsonify({'message': str(e), 'status': False})
    
    return jsonify({'message': "render success", 'status': True})

@app.route('/post_msg', methods=['POST'])
@log_activity(bot)  # 获取前端发来的消息
def get_msg():
    """get_msg: get the message from the message queue."""
    global msg_list
    msg = msg_list
    msg_list = []
    return jsonify({'message': msg, 'status': True})


@app.route('/post_time', methods=['POST'])
@log_activity(bot)  # 获取前端的时间
def get_time():
    return jsonify({'time': str(bot.time.timeOfDay)})

@app.route('/post_lay', methods=['POST'])
@log_activity(bot)
def lay_():
    """lay: lay the block."""
    data = request.get_json()
    x_1, y_1, z_1, x_2, y_2, z_2 = data.get('x_1'), data.get('y_1'), data.get('z_1'), data.get('x_2'), data.get('y_2'), data.get('z_2')
    need = (abs(x_1 - x_2) + 1) * (abs(y_1 - y_2) + 1) * (abs(z_1 - z_2) + 1)
    tag, msg = move_to(pathfinder, bot, Vec3, 3, Vec3(x_1, y_1, z_1))
    if not tag:
        return jsonify({'message': msg, 'status': False})
    tag, msg = move_to(pathfinder, bot, Vec3, 3, Vec3(x_2, y_2, z_2))
    if not tag:
        return jsonify({'message': msg, 'status': False})
    
    if countInventoryItems(bot, 'dirt')[1] < need:
        return jsonify({'message': f"Don't have enough dirt in inventory, have {countInventoryItems(bot, 'dirt')[1]}, need {need}", 'status': False})
    if x_1 == x_2 and y_1 == y_2:
        for z in range(min(z_1, z_2), max(z_1, z_2) + 1):
            bot.chat(f"/setblock {x_1} {y_1} {z} dirt")
            move_to(pathfinder, bot, Vec3, 3, Vec3(x_1, y_1, z+1))
            time.sleep(1)
    elif z_1 == z_2 and y_1 == y_2:
        for x in range(min(x_1, x_2), max(x_1, x_2) + 1):
            bot.chat(f"/setblock {x} {y_1} {z_1} dirt")
            move_to(pathfinder, bot, Vec3, 3, Vec3(x, y_1, z_1+1))
            time.sleep(1)
    else:
        return jsonify({'message': "only lay dirt in axis x or z is supported", 'status': False})
    
    return jsonify({'message': "lay success", 'status': True})

@app.route('/post_remove', methods=['POST'])
@log_activity(bot)
def remove_():
    """remove: remove the block."""
    data = request.get_json()
    x_1, y_1, z_1, x_2, y_2, z_2 = data.get('x_1'), data.get('y_1'), data.get('z_1'), data.get('x_2'), data.get('y_2'), data.get('z_2')
    tag, msg = move_to(pathfinder, bot, Vec3, 3, Vec3(x_1, y_1, z_1))
    if not tag:
        return jsonify({'message': msg, 'status': False})
    tag, msg = move_to(pathfinder, bot, Vec3, 3, Vec3(x_2, y_2, z_2))
    if not tag:
        return jsonify({'message': msg, 'status': False})
    if x_1 == x_2 and y_1 == y_2:
        for z in range(min(z_1, z_2), max(z_1, z_2) + 1):
            if bot.blockAt(Vec3(x_1, y_1, z)).name == "dirt":
                bot.chat(f"/setblock {x_1} {y_1} {z} air")
            move_to(pathfinder, bot, Vec3, 3, Vec3(x_1, y_1, z+1))
            time.sleep(1)
    elif z_1 == z_2 and y_1 == y_2:
        for x in range(min(x_1, x_2), max(x_1, x_2) + 1):
            if bot.blockAt(Vec3(x_1, y_1, z)).name == "dirt":
                bot.chat(f"/setblock {x_1} {y_1} {z} air")
            move_to(pathfinder, bot, Vec3, 3, Vec3(x, y_1, z_1+1))
            time.sleep(1)
    else:
        return jsonify({'message': "only remove dirt in axis x or z is supported", 'status': False})
    return jsonify({'message': "remove dirt line success", 'status': True})


@app.route('/post_erect', methods=['POST'])
@log_activity(bot)
def erect():
    """erect: erect the structure."""
    data = request.get_json()
    top_x, top_y, top_z = data.get('top_x'), data.get('top_y'), data.get('top_z')
    
    # 计算top 和 bot 的距离
    distance = ((top_x - bot.entity.position.x) ** 2 + (top_y - bot.entity.position.y) ** 2 + (top_z - bot.entity.position.z) ** 2) ** .5
    if distance > 32:
        return jsonify({'message': "the distance is too far", 'status': False})

    # bottom 是遍历找到的最低的方块
    if bot.blockAt(Vec3(top_x, top_y, top_z)).name != "air":
        return jsonify({'message': "the top is not air", 'status': False})
    
    bottom_y = top_y
    for y in range(top_y, -64, -1):
        if bot.blockAt(Vec3(top_x, y, top_z)).name != "air":
            bottom_y = y
            break

    # 计算需要的方块数量
    need_dirt = (top_y - bottom_y) 
    need_ladder = (top_y - bottom_y)
    if countInventoryItems(bot, "dirt")[1] < need_dirt and countInventoryItems(bot, "ladder")[1] < need_ladder:
        return jsonify({'message': f"Don't have enough dirt and ladder in inventory, have {countInventoryItems(bot, 'dirt')[1]}, need {need_dirt}, have {countInventoryItems(bot, 'ladder')[1]}, need {need_ladder}", 'status': False})
    if countInventoryItems(bot, "dirt")[1] < need_dirt:
        return jsonify({'message': f"Don't have enough dirt in inventory, have {countInventoryItems(bot, 'dirt')[1]}, need {need_dirt}", 'status': False})
    if countInventoryItems(bot, "ladder")[1] < need_ladder:
        return jsonify({'message': f"Don't have enough ladder in inventory, have {countInventoryItems(bot, 'ladder')[1]}, need {need_ladder}", 'status': False})
    # 从低到高，放置方块
    x = top_x
    z = top_z
    move_to(pathfinder, bot, Vec3, 3, Vec3(x, bottom_y, z+5))
    for y in range(bottom_y, top_y):
        if bot.blockAt(Vec3(x, y, z)).name == "air":
            bot.chat(f"/setblock {x} {y} {z} dirt")
        if bot.blockAt(Vec3(x+1, y, z)).name == "air":
            bot.chat(f"/setblock {x+1} {y} {z} ladder[facing=east]")
        if bot.blockAt(Vec3(x-1, y, z)).name == "air":
            bot.chat(f"/setblock {x-1} {y} {z} ladder[facing=west]")
        if bot.blockAt(Vec3(x, y, z+1)).name == "air":
            bot.chat(f"/setblock {x} {y} {z+1} ladder[facing=south]")
        if bot.blockAt(Vec3(x, y, z-1)).name == "air":
            bot.chat(f"/setblock {x} {y} {z-1} ladder[facing=north]")
            bot.chat(f"/clear @s dirt 1")
            bot.chat(f"/clear @s ladder 1")
        # bot.chat(f"setblock {x} {y} {z} spruce_planks")
        move_to(pathfinder, bot, Vec3, 3, Vec3(x, y, z+1))
        time.sleep(.1)
    return jsonify({'message': "erect success", 'status': True})

@app.route('/post_dismantle', methods=['POST'])
@log_activity(bot)
def dismantle():
    """dismantle: dismantle the structure."""
    data = request.get_json()
    top_x, top_y, top_z = data.get('top_x'), data.get('top_y'), data.get('top_z')
    # 计算top 和 bot 的距离
    distance = ((top_x - bot.entity.position.x) ** 2 + (top_y - bot.entity.position.y) ** 2 + (top_z - bot.entity.position.z) ** 2) ** .5
    if distance > 32:
        return jsonify({'message': "the distance is too far", 'status': False})
    # bottom 是遍历找到的最低的方块
    if bot.blockAt(Vec3(top_x, top_y, top_z)).name == "air" and bot.blockAt(Vec3(top_x, top_y-1, top_z)).name == "air":
        return jsonify({'message': "the top is air", 'status': False})
    bottom_y = top_y
    bottom_y = -59
    # 从高到低，放置方块
    x = top_x
    z = top_z
    for y in range(top_y, bottom_y, -1):
        if bot.blockAt(Vec3(x, y, z)).name == "dirt":
            bot.chat(f"/setblock {x} {y} {z} air")
            bot.chat(f"/give @s dirt 1")
            bot.chat(f"/give @s ladder 1")
        bot.chat(f"setblock {x} {y} {z} air {bot.blockAt(Vec3(x, y, z)).name}")
        move_to(pathfinder, bot, Vec3, 3, Vec3(x, y, z+1))
        time.sleep(.1)
    return jsonify({'message': "dismantle success", 'status': True})

@app.route('/post_find', methods=['POST'])
@log_activity(bot)
def find():
    """find name distance count: find tag in the distance, and count is the number of items you want to find."""
    data = request.get_json()
    name, distance, count = data.get('name'), data.get('distance'), data.get('count')
    center_pos = bot.entity.position
    # 随机移动一下 防止卡住
    random_x = randint(-4, 4)
    random_z = randint(-4, 4)
    move_to(pathfinder, bot, Vec3, 3, Vec3(center_pos.x+random_x, center_pos.y, center_pos.z+random_z))

    distance = min(32, max(16, distance)) # 限制在16-32之间
    envs_info = get_envs_info(bot, distance)
    if name == "":
        # bot.chat(f"can not find anything match '{data.get('name')}'")
        msg = get_envs_info2str(bot, RENDER_DISTANCE=16, same_entity_num=3)
        blocks = BlocksNearby(bot, Vec3, mcData, RenderRange=distance, max_same_block=3,visible_only=VISIBLE_ONLY)
        hint = readNearestSign(bot, Vec3, mcData, max_distance=5)
        for block in blocks:
            msg += f"{block['name']} at {block['position']}\n"
        if hint:
            msg += f"the sign nearby said: {hint}"
        
        if os.path.exists(".cache/env.cache"):
            with open(".cache/env.cache", "r") as f:
                cache = json.load(f)
            # 找到距离小于5的cache
            for c in cache:
                pos = c["center"]
                if (pos[0] - bot.entity.position.x) ** 2 + (pos[1] - bot.entity.position.y) ** 2 + (
                        pos[2] - bot.entity.position.z) ** 2 < 25:
                    msg += f"the env in the room: {c['state']}"
        return jsonify({'message': f"can not find anything match '{name}', environment: "+ msg, 'status': False, 'data':[]})
    
    observation = ""
    # 耗时操作
    name, pos_list_raw = find_everything_(bot, Vec3, envs_info, mcData, name, distance, count, visible_only=VISIBLE_ONLY)
  
    # remove duplicate
    # bot.chat(f"pos_list_raw {pos_list_raw}")
    pos_list = []
    for pos in pos_list_raw:
        for pos2 in pos_list:
            if floor(pos.x + .5) == floor(pos2.x + .5) and floor(pos.y + .5) == floor(pos2.y + .5) and floor(pos.z + .5) == floor(
                    pos2.z + .5):
                break
        else:
            pos_list.append(pos)

    pos_data = []

    if len(pos_list) > 0:
        str_pos_list = f'I found {name} '
        # if pos_list is dict:
        if type(pos_list) == dict:
            for pos in pos_list:
                str_pos_list += f'at {pos},'
                pos_data.append({"x": floor(pos["x"] + .5), "y": floor(pos["y"] + .5), "z": floor(pos["z"] + .5)})
        else:
            for pos in pos_list:
                str_pos_list += f'at {floor(pos.x + .5)} {floor(pos.y + .5)} {floor(pos.z + .5)},'
                pos_data.append({"x": floor(pos.x + .5), "y": floor(pos.y + .5), "z": floor(pos.z + .5)})
        observation += str_pos_list
        done = True
        return jsonify({'message': observation, 'status': done, 'data':pos_data})
    else:
        observation += f"can not find item with name '{name}'"
        done = False
        return jsonify({'message': observation, 'status': done, 'data':[]})
 
@app.route('/post_hand', methods=['POST'])
@log_activity(bot)
def hand():
    """hand item to entity_name: hand item to entity_name."""
    data = request.get_json()
    from_name, target_name, item_name, count = data.get('from_name'), data.get('target_name'), data.get('item_name'), data.get('item_count')
    
    # move to the target
    envs_info = get_envs_info(bot, 128)
    tag, msg = move_to_nearest_(pathfinder, bot, Vec3, envs_info, mcData, 2, target_name)
    if not tag:
        return jsonify({'message': msg, 'status': False})
    entities = get_entity_by('username', envs_info, target_name)
    if not entities:
        return jsonify({'message': f"{target_name} is not valid", 'status': False})
    entities = get_entity_by('username', envs_info, from_name)
    if not entities:
        return jsonify({'message': f"{from_name} is not valid", 'status': False})
    if countInventoryItems(bot, item_name)[1] < count and (not bot.heldItem or bot.heldItem.name != item_name.lower().replace(" ", "_")):
        return jsonify({'message': f"{from_name} don't have enough {item_name} in inventory", 'status': False})
    bot.chat(f"/clear {from_name} {item_name} {count}")
    time.sleep(1)
    bot.chat(f"/give {target_name} {item_name} {count}")
    return jsonify({'message': f"give {item_name} from {from_name} to {target_name}", 'status': True})

@app.route('/post_move_to', methods=['POST'])
@log_activity(bot)
def move_to_():
    """move_to name: move to the entity by name or postion x y z."""
    data = request.get_json()
    name = data.get('name')
    envs_info = get_envs_info(bot, 128)
    tag, msg = move_to_nearest_(pathfinder, bot, Vec3, envs_info, mcData, 5, name)
    done = tag
    move_to_nearest_(pathfinder, bot, Vec3, envs_info, mcData, 1, name)
    return jsonify({'message': msg, 'status': done})


@app.route('/post_move_to_pos', methods=['POST'])
@log_activity(bot)
def move_to_pos():
    """move_to_pos x y z: move to the position x y z."""
    data = request.get_json()
    x, y, z = data.get('x'), data.get('y'), data.get('z')
    tag1, msg1 = move_to(pathfinder, bot, Vec3, 3, Vec3(x, y, z))
    tag2, msg2 = move_to(pathfinder, bot, Vec3, 2, Vec3(x, y, z))
    tag3, msg3 = move_to(pathfinder, bot, Vec3, 1, Vec3(x, y, z))
    # lookAtPlayer(bot, entity['position'])
    return jsonify({'message': msg1, 'status': tag1})


@app.route('/post_use_on', methods=['POST'])
@log_activity(bot)
def use_on():
    """use_on item_name entity_name: For example, you can use shears on sheep, use bucket on cow."""
    data = request.get_json()
    item_name, entity_name = data.get('item_name'), data.get('entity_name')
    envs_info = get_envs_info(bot, 128)
    msg, tag = useOnNearest(bot, Vec3, pathfinder, envs_info, mcData, item_name, entity_name)
    done = tag
    return jsonify({'message': msg, 'status': done})


@app.route('/post_sleep', methods=['POST'])
@log_activity(bot)
def sleep_():
    """sleep: to sleep."""
    msg = sleep(bot, Vec3, mcData)
    done = True
    return jsonify({'message': msg, 'status': done})


@app.route('/post_wake', methods=['POST'])
@log_activity(bot)
def wake_():
    """wake: to wake."""
    msg = wake(bot)
    done = True
    return jsonify({'message': msg, 'status': done})


@app.route('/post_dig', methods=['POST'])
@log_activity(bot)
def dig():
    """dig x y z: dig block at x y z."""
    data = request.get_json()
    x, y, z = data.get('x'), data.get('y'), data.get('z')
    msg, tag = dig_at(bot, pathfinder, Vec3, (x, y, z))
    
    return jsonify({'message': msg, 'status': tag})


@app.route('/post_place', methods=['POST'])
@log_activity(bot)
def place():
    """place item_name x y z facing: place item at x y z, facing is one of [W, E, S, N, x, y, z, A]."""
    data = request.get_json()
    item_name, x, y, z, facing = data.get('item_name'), data.get('x'), data.get('y'), data.get('z'), data.get('facing')
    if facing.lower() == 'default':
        facing = 'A'
    if facing.lower() == 'up' or facing.lower() == 'down':
        facing = 'y'
    if facing.lower() == 'north' or facing.lower() == 'south':
        facing = 'z'
    if facing.lower() == 'west' or facing.lower() == 'east':
        facing = 'x'
    if facing not in ['x', 'y', 'z', "W", "E", "S", "N", "A"]:
        return jsonify({'message': "facing is one of [W, E, S, N, x, y, z, A]", 'status': False})
    flag, msg = asyncio.run(place_axis(bot, mcData, pathfinder, Vec3, item_name, (x, y, z), facing))

    # 随机移动一下 防止卡住
    random_x = choice([-5, -4, -3, 3, 4, 5])
    random_z = choice([-5, -4, -3, 3, 4, 5])
    center_pos = bot.entity.position
    move_to(pathfinder, bot, Vec3, 3, Vec3(center_pos.x+random_x, center_pos.y, center_pos.z+random_z))
    if not flag and item_name == 'ladder':
        return jsonify({'message': f"{msg}, there is no block to support it.", 'status': False})
    return jsonify({'message': msg, 'status': flag})


@app.route('/post_attack', methods=['POST'])
@log_activity(bot)
def attack_():
    """attack name:  to attack the nearest entity."""
    data = request.get_json()
    name = data.get('name')
    envs_info = get_envs_info(bot, 128)
    msg, tag = asyncio.run(attack(bot, envs_info, mcData, name))
    done = tag
    return jsonify({'message': msg, 'status': done})


@app.route('/post_equip', methods=['POST'])
@log_activity(bot)
def equip_():
    """equip slot item_name:  to equip item on hand,head,torso,legs,feet,off-hand."""
    data = request.get_json() 
    
    slot, item_name = data.get('slot'), data.get('item_name')
    slot = "hand" if slot == "mainhand" else slot
    if bot.heldItem and slot == "hand":
        if bot.heldItem.name == item_name or bot.heldItem.name == item_name.replace(" ", "_"):
            return jsonify({'message': f"{bot.username} already has {data.get('item_name')} in hand", 'status': True})
    observation = ""
    value_data = []
    try:
        if not findInventoryItems(bot, item_name):
            observation += f"I don't have {item_name} in my inventory"
            return jsonify({'message': observation, 'status': False, 'data': []})
        else:
            msg, done = equip(bot, item_name, slot)
            observation += msg
            return jsonify({'message': observation, 'status': done, 'data': value_data})
    except:
        observation += "equip fail"
        done = False
        return jsonify({'message': observation, 'status': done, 'data': value_data})


@app.route('/post_toss', methods=['POST'])
@log_activity(bot)
def toss_():
    """toss item_name count:  to throw item out."""
    data = request.get_json()
    item_name, count = data.get('item_name'), data.get('count', 1)
    msg, tag = toss(bot, mcData, item_name, count)
    return jsonify({'message': msg, 'status': tag})


@app.route('/post_environment', methods=['POST'])
@log_activity(bot)  # 获取环境信息
def environment():
    """environment:  to get the environment info."""
    msg = get_envs_info2str(bot, RENDER_DISTANCE=32, same_entity_num=3)
    blocks = BlocksNearby(bot, Vec3, mcData, RenderRange=32, max_same_block=3, visible_only=VISIBLE_ONLY)
    hint = readNearestSign(bot, Vec3, mcData, max_distance=5)
    for block in blocks:
        msg += f"{block['name']} at {block['position']}\n"
    if hint:
        msg += f"the sign nearby said: {hint}"
    
    if os.path.exists(".cache/env.cache"):
        with open(".cache/env.cache", "r") as f:
            cache = json.load(f)
        # 找到距离小于5的cache
        for c in cache:
            pos = c["center"]
            if (pos[0] - bot.entity.position.x) ** 2 + (pos[1] - bot.entity.position.y) ** 2 + (
                    pos[2] - bot.entity.position.z) ** 2 < 25:
                msg["sign"] += f"The subtask in this room: {c['task_description']}"
                msg["sign"] += f"The env in the room: {c['state']}"
    done = True
    return jsonify({'message': msg, 'status': done})

@app.route('/post_environment_dict', methods=['POST'])
@log_activity(bot)  # 获取环境信息
def environment_info():
    """environment:  to get the environment info."""
    msg = get_envs_info_dict(bot, RENDER_DISTANCE=32, same_entity_num=3)
    blocks = BlocksNearby(bot, Vec3, mcData, RenderRange=32, max_same_block=3, visible_only=VISIBLE_ONLY)
    hint = readNearestSign(bot, Vec3, mcData, max_distance=5)
    msg["blocks"] = blocks
    msg["sign"] = hint
    if os.path.exists(".cache/env.cache"):
        with open(".cache/env.cache", "r") as f:
            cache = json.load(f)
        # 找到距离小于5的cache
        for c in cache:
            pos = c["center"]
            if (pos[0] - bot.entity.position.x) ** 2 + (pos[1] - bot.entity.position.y) ** 2 + (
                    pos[2] - bot.entity.position.z) ** 2 < 25:
                msg["sign"] += f"The subtask in this room: {c['task_description']}"
                msg["sign"] += f"The env in the room: {c['state']}"
    done = True
    return jsonify({'message': msg, 'status': done})


@app.route('/post_entity', methods=['POST'])
@log_activity(bot)
def entity():
    """entity distance name:  to get the entity info in range distance."""
    data = request.get_json()
    name = data.get('name', "")
    info, num = get_agent_info2str(bot, RENDER_DISTANCE=32, idle=False, with_humans=False, name=name)
    return jsonify({'message': info, 'status': True, 'data': num})


@app.route('/post_get', methods=['POST'])
@log_activity(bot)
def get():
    """get item_name count:  to get item from one chest, container, etc."""
    data = request.get_json()
    item_name, from_name, item_count = data.get('item_name'), data.get('from_name'), data.get('item_count')
    envs_info = get_envs_info(bot, 128)
    if item_count is None:
        item_count = 1
    if item_count < 0:
        item_count = -item_count
    tag, flag, data = asyncio.run(
        interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, from_name, get_item_name=item_name, count=-item_count))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_put', methods=['POST'])
@log_activity(bot)
def put():
    """put item_name count:  to put item to one chest, container, etc."""
    data = request.get_json()
    item_name, to_name, item_count = data.get('item_name'), data.get('to_name'), data.get('item_count')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(
        interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, to_name, get_item_name=item_name, count=item_count))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_smelt', methods=['POST'])
@log_activity(bot)
def smelt():
    """smelt item_name item_count material:  to smelt item in the furnace. fuel_item is one of [wood, coal, charcoal, lava_bucket, etc]."""
    data = request.get_json()
    item_name, item_count, fuel_item_name = data.get('item_name'), data.get('item_count'), data.get('fuel_item_name')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, name="furnace", get_item_name=item_name, count=item_count,
                                             fuel_item_name=fuel_item_name))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_craft', methods=['POST'])
@log_activity(bot)
def craft():
    """craft item_name count:  to craft item in the crafting_table."""
    data = request.get_json()
    item_name, count = data.get('item_name'), data.get('count')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(
        interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, 'crafting_table', get_item_name=item_name, count=count))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_enchant', methods=['POST'])
@log_activity(bot)
def enchant():
    """enchant item_name count:  to enchant item in the enchanting_table."""
    data = request.get_json()
    item_name, count = data.get('item_name'), data.get('count')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(
        interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, 'enchanting_table', get_item_name=item_name,
                         count=count))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_trade', methods=['POST'])
@log_activity(bot)
def trade():
    """trade item_name count:  to trade item with the entity."""
    data = request.get_json()
    item_name, with_name, count = data.get('item_name'), data.get('with_name'), data.get('count')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(
        interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, with_name, get_item_name=item_name, count=count))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_repair', methods=['POST'])
@log_activity(bot)
def repair():
    """repair item_name material:  to repair item in the anvil. material is one of [wood, stone, iron, diamond, gold]."""
    data = request.get_json()
    item_name, material = data.get('item_name'), data.get('material')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, 'anvil', repair_item_name=item_name,
                                             get_item_name=material))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_eat', methods=['POST'])
@log_activity(bot)
def eat():
    """eat item_name:  to eat item."""
    data = request.get_json()
    item_name = data.get('item_name')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, item_name))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_drink', methods=['POST'])
@log_activity(bot)
def drink():
    """drink item_name count:  to drink item."""
    data = request.get_json()
    item_name, count = data.get('item_name'), data.get('count')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, item_name))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_wear', methods=['POST'])
@log_activity(bot)
def wear():
    """wear slot item_name:  to wear item on head,torso,legs,feet,off-hand."""
    data = request.get_json()
    slot, item_name = data.get('slot'), data.get('item_name')
    observation = ""
    value_data = []
    try:
        if not findInventoryItems(bot, item_name):
            envs_info = get_envs_info(bot, 128)
            msg, flag, value_data = asyncio.run(
                interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, 'chest', get_item_name=item_name))
            observation += msg
        msg, done = equip(bot, item_name, slot)
        observation += msg
        return jsonify({'message': observation, 'status': done, 'data': value_data})
    except:
        observation += "equip fail"
        done = False
        return jsonify({'message': observation, 'status': done, 'data': value_data})
    
@app.route('/post_find_inventory', methods=['POST'])
@log_activity(bot)
def find_inventory():
    """find_inventory item_name:  to find if there is item in the inventory and return count."""
    data = request.get_json()
    item_name = data.get('item_name')
    tag, count = findInventoryItems(bot, item_name)
    return jsonify({'message': "", 'status': tag, 'data': count})


@app.route('/post_open', methods=['POST'])
@log_activity(bot)
def open_():
    """open item_name:  to open the door, gate, fence_gate, trapdoor, chest, etc, return the items names if open chest"""
    data = request.get_json()
    item_name = data.get('item_name')
    if item_name == "inventory":
        items = getInventoryItems(bot)
        data = [ {"name": item["name"], "count": item["count"]} for item in items]
        return jsonify({'message': f"opened the inventory", 'status': True, 'data': data})
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, item_name))
    return jsonify({'message': tag, 'status': flag, 'data': data})


@app.route('/post_close', methods=['POST'])
@log_activity(bot)
def close_():
    """close item_name:  to close the door, gate, fence_gate, trapdoor, chest, etc."""
    data = request.get_json()
    item_name = data.get('item_name')
    envs_info = get_envs_info(bot, 128)
    tag, flag, data = asyncio.run(interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, item_name))
    if flag:
        return jsonify({'message': "I close " + item_name, 'status': flag, 'data': data})
    else:
        return jsonify({'message': "I cannot close " + item_name + ", it is still open.", 'status': flag, 'data': data})


@app.route('/post_activate', methods=['POST'])
@log_activity(bot)
def activate():
    """activate item_name:  to activate the button, lever, pressure_plate, etc."""
    data = request.get_json()
    item_name = data.get('item_name')
    x, y, z = data.get('x'), data.get('y'), data.get('z')
    if x is not None and y is not None and z is not None:
        move_to(pathfinder, bot, Vec3, 1, Vec3(x, y, z))
    envs_info = get_envs_info(bot, 128)
    item_past = bot.blockAt(Vec3(x, y, z))
    item_now_open = item_past._properties["open"]
    item_now_powered = item_past._properties["powered"]
    tag, flag, data = asyncio.run(interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, 3, item_name, target_position=Vec3(x, y, z)))
    item_now = bot.blockAt(Vec3(x, y, z))
    

    description = ""
    description += f"I interact with {item_now['name']} at {x} {y} {z}"
    if item_now_open == True:
        description += ", I close it now."
    elif item_now_open == False:
        description += ", I open it now."
    
    if item_now_powered == True:
        description += ", I turn it off now."
    elif item_now_powered == False:
        description += ", I turn it on now."
    
    if item_now_open == None and item_now_powered == None:
        description += ", it is not working."
        return jsonify({'message': description, 'status': False, 'data': data})
    
    if flag:
        return jsonify({'message': description, 'status': flag, 'data': data})
    else:
        return jsonify({'message': "I cannot activate " + item_name + ", it is not working.", 'status': flag,
                        'data': data})


@app.route('/post_mount', methods=['POST'])
@log_activity(bot)
def mount_():
    """mount entity_name:  to mount the entity."""
    data = request.get_json()
    entity_name = data.get('entity_name')
    try:
        msg, done = mount(bot, entity_name)
        return jsonify({'message': msg, 'status': done})
    except:
        done = False
        return jsonify({'message': "mount fail", 'status': done})


@app.route('/post_dismount', methods=['POST'])
@log_activity(bot)
def dismount_():
    """dismount:  to dismount the entity."""
    try:
        msg, done = dismount(bot)
        return jsonify({'message': msg, 'status': done})
    except:
        done = False
        return jsonify({'message': "dismount fail", 'status': done})


@app.route('/post_ride', methods=['POST'])
@log_activity(bot)
def ride():
    """ride entity_name:  to ride the entity."""
    data = request.get_json()
    entity_name = data.get('entity_name')
    try:
        msg, done = mount(bot, entity_name)
        return jsonify({'message': msg, 'status': done})
    except:
        done = False
        return jsonify({'message': "ride fail", 'status': done})


@app.route('/post_disride', methods=['POST'])
@log_activity(bot)
def disride():
    """disride:  to disride the entity."""
    try:
        msg, done = dismount(bot)
        return jsonify({'message': msg, 'status': done})
    except:
        done = False
        return jsonify({'message': "disride fail", 'status': done})


@app.route('/post_talk_to', methods=['POST'])
@log_activity(bot)
def talk_to():
    """talk_to entity_name message:  to talk to the entity."""
    data = request.get_json()
    entity_name, message = data.get('entity_name'), data.get('message')
    chat_long(bot, entity_name, message, "talk")
    return jsonify({'message': f"I talk to {entity_name} {message}", 'status': True})


@app.route('/post_done', methods=['POST'])
@log_activity(bot)
def done():
    """done:  to end the task."""
    data = request.get_json()
    feedback = data.get('feedback')
    print(feedback)
    return jsonify({'message': "I done", 'status': True})


@app.route('/post_action', methods=['POST'])
@log_activity(bot)
def action():
    """action action_name seconds:  to do action for seconds, action_name is one of [swing_arm, forward, back, left, right, jump, sprint]."""
    data = request.get_json()
    action_name, seconds = data.get('action_name'), data.get('seconds')
    if action_name == 'swing_arm':
        start_time = time.time()
        while time.time() - start_time < seconds:
            bot.swingArm()
        return jsonify({'message': "I swing my arms.", 'status': True})
    elif action_name == 'forward':
        while seconds > 0:
            bot.setControlState('forward', True)
            seconds -= 1
            time.sleep(1)
        bot.setControlState('forward', False)
        return jsonify({'message': "I move forward in a few seconds", 'status': True})
    elif action_name == 'back':
        while seconds > 0:
            bot.setControlState('back', True)
            seconds -= 1
            time.sleep(1)
        bot.setControlState('back', False)
        return jsonify({'message': "I move back in a few seconds", 'status': True})
    elif action_name == 'left':
        seconds = 1
        while seconds > 0:
            bot.setControlState('left', True)
            seconds -= 1
            time.sleep(1)
        bot.setControlState('left', False)
        return jsonify({'message': "I move left in a few seconds", 'status': True})
    elif action_name == 'right':
        while seconds > 0:
            bot.setControlState('right', True)
            seconds -= 1
            time.sleep(1)
        bot.setControlState('right', False)
        return jsonify({'message': "I move right in a few seconds", 'status': True})
    elif action_name == 'sprint':
        while seconds > 0:
            bot.setControlState('sprint', True)
            seconds -= 1
            time.sleep(1)
        bot.setControlState('sprint', False)
        return jsonify({'message': "I sprint in a few seconds", 'status': True})
    elif action_name == 'jump':
        while seconds > 0:
            bot.setControlState('jump', True)
            seconds -= 1
            time.sleep(1)
        bot.setControlState('jump', False)
        return jsonify({'message': "I jump in a few seconds", 'status': True})
    else:
        return jsonify({'message': "I cannot do this action", 'status': False})


@app.route('/post_look_at', methods=['POST'])
@log_activity(bot)
def look_at():
    """look_at name: use this to look at someone or something."""
    data = request.get_json()
    name = data.get('name')
    envs_info = get_envs_info(bot, 128)
    pos = find_nearest_(bot, Vec3, envs_info, mcData, name)
    if pos != None:
        lookAtPlayer(bot, pos)
    done = pos != None
    if not done:
        return jsonify({'message': f"cannot find {name}.", 'status': done})
    else:
        return jsonify({'message': f"I look at {name}.", 'status': done})


@app.route('/post_start_fishing', methods=['POST'])
@log_activity(bot)
def start_fishing():
    """start_fishing: start fishing."""
    envs_info = get_envs_info(bot, 128)
    msg, tag = startFishing(bot, Vec3, envs_info, mcData)
    done = tag
    return jsonify({'message': msg, 'status': done})


@app.route('/post_stop_fishing', methods=['POST'])
@log_activity(bot)
def stop_fishing():
    """stop_fishing: stop fishing."""
    msg, tag = stopFishing(bot)
    done = tag
    return jsonify({'message': msg, 'status': done})


@app.route('/post_read', methods=['POST'])
@log_activity(bot)
def read_():
    """read name: only support read book or sign."""
    data = request.get_json()
    name = data.get('name')
    envs_info = get_envs_info(bot, 128)
    msg, tag = read(bot, Vec3, envs_info, mcData, name)
    done = tag
    return jsonify({'message': msg, 'status': done})


@app.route('/post_read_page', methods=['POST'])
@log_activity(bot)
def read_page():
    """read name: this is how you read content from book page."""
    data = request.get_json()
    name, page = data.get('name'), data.get('page')
    envs_info = get_envs_info(bot, 128)
    msg, tag = read(bot, Vec3, envs_info, mcData, name, page)
    done = tag
    return jsonify({'message': msg, 'status': done})


@app.route('/post_write', methods=['POST'])
@log_activity(bot)
def write_():
    """write name: this is how you write content on writable book or sign."""
    data = request.get_json()
    name, content = data.get('name'), data.get('content')
    envs_info = get_envs_info(bot, 128)
    msg, tag = write(bot, Vec3, envs_info, mcData, name, content)
    done = tag
    return jsonify({'message': msg, 'status': done})


@app.route('/post_chat', methods=['POST'])
@log_activity(bot)
def chat_():
    """chat message: this is how you chat."""
    data = request.get_json()
    message = data.get('msg')
    message_copy = message
    while True:
        if len(message_copy) > 256:
            bot.chat(message_copy[:256])
            time.sleep(.5)
            message_copy = message_copy[256:]
        else:
            bot.chat(message_copy)
            break
    return jsonify({'message': f"I chat {message}", 'status': True})

@On(bot, 'spawn')
def handleViewer(*args):
    path = [bot.entity.position]

    bot.chat('/gamemode survival')
    time.sleep(.1)
    bot.chat('/clear @s')
    time.sleep(.1)

    @On(bot, 'move')
    def handleMove(*args):
        try:
            if (path[-1].distanceTo(bot.entity.position) > 1.5):
                path.append(bot.entity.position)
                # bot.viewer.drawLine('path', path)
        except:
            pass

    @On(bot, 'chat')
    def handle(this, username, message, *args):
        try:
            global msg_list
            msg_list += [{"username": username, "message": message}]
        except:
            pass
        
    @On(bot, "whisper")
    def handle(this, username, message, *args):
        global msg_list
        msg_list += [{"username": username, "message": message}]

@On(bot, "itemDrop")
def handle(this, entity):
    bot.chat("item drop")
    global Pickable
    dis = distanceTo(bot.entity.position, entity['position'])
    if dis < 5:
        move_to(pathfinder, bot, Vec3, 1, entity['position'])



from waitress import serve

serve(app, port=local_port)

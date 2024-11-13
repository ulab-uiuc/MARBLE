import random
import time
import asyncio
from javascript import require, On
import sys
import io
import os
import json
from collections import deque

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

env_infos = None
update_time = 0
update_interval = .5


def getBlock(bot, Vec3, x, y, z):
    while True:
        try:
            block = bot.blockAt(Vec3(x, y, z))
            return block
        except Exception as e:
            time.sleep(1)
            continue

def readNearestSign(bot, Vec3, mcData, max_distance=7) -> str:
    sign_block_name_list = ['oak_sign', 'spruce_sign', 'birch_sign', 'jungle_sign', 'acacia_sign', 'dark_oak_sign', 'mangrove_sign', 'palm_sign', 'redwood_sign', 'willow_sign']
    sign_block_name_list += ['oak_wall_sign', 'spruce_wall_sign', 'birch_wall_sign', 'jungle_wall_sign', 'acacia_wall_sign', 'dark_oak_wall_sign', 'mangrove_wall_sign', 'palm_wall_sign', 'redwood_wall_sign', 'willow_wall_sign']
    blocks = []
    for block_name in sign_block_name_list:
        new_blocks = bot.findBlocks(
            {
                "point": bot.entity.position,
                "matching": findSomething(bot, mcData, block_name)[0],
                "maxDistance": max_distance,
                "count": 1,
            }
        )
        for block in new_blocks:
            blocks.append(block)
    if len(blocks) > 0:
        # sort by distance
        bot.chat(f"find {len(blocks)} signs")
        blocks.sort(key=lambda x: distanceTo(x, bot.entity.position))
        block = bot.blockAt(blocks[0])
        text = block.getSignText()
        return text.join('\n')
    else:
        return ""

from math import floor
def bfs_search(bot, Vec3, bot_position, max_distance):
    queue = deque([(bot_position, 0),
                   ((bot_position[0], bot_position[1]-1, bot_position[2]), 1),
                   ((bot_position[0], bot_position[1]+1, bot_position[2]), 1)])

    visited = set()  # 用于跟踪已经访问过的位置
    visible_blocks = []  # 用于存储可见方块的字典

    while queue:
        position, distance = queue.popleft()  # 从队列的左侧弹出元素
        if distance > max_distance or position in visited:
            continue
        visited.add(position)
        block = getBlock(bot, Vec3, *position)
        if block["name"] != "air":
            # bot.chat(f"bfs {block['name']}")
            visible_blocks.append({
                "name": block["name"],
                "position": [floor(position[0]), floor(position[1]), floor(position[2])],
                "facing": block["_properties"]["facing"],
                "axis": block["_properties"]["axis"],
                "part": block["_properties"]["part"],
                "hinge": block["_properties"]["hinge"],
                "powered": block["_properties"]["powered"],
                "face": block["_properties"]["face"],
                "open": block["_properties"]["open"]}
                )
            # 去除 None属性
            visible_blocks[-1] = {k: v for k, v in visible_blocks[-1].items() if v is not None}
            if "fence" not in block["name"]:
                continue            

        x, y, z = position
        for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            next_position = (x + dx, y + dy, z + dz)
            if next_position not in visited:  # 检查是否已访问
                queue.append((next_position, distance + 1))  # 将新位置添加到队列的右侧

    return visible_blocks

def BlocksNearby(bot, Vec3, mcData, RenderRange=5, max_time=3, max_same_block=3, max_block_num=24, visible_only=True):
    import math
    if visible_only:
        anchor_pos = bot.entity.position
        blocks = bfs_search(bot, Vec3, (anchor_pos.x, anchor_pos.y, anchor_pos.z), RenderRange)
        
        # 去除重复超过max_same_block次的方块
        new_blocks = []
        block_dict = {}
        for block in blocks:
            if block["name"] in block_dict:
                block_dict[block["name"]] += 1
                if block_dict[block["name"]] > max_same_block:
                    continue
            else:
                block_dict[block["name"]] = 1
            new_blocks.append(block)
        return new_blocks
    try:
        anchor_pos = bot.entity.position

        start_time = time.time()
        blocks = []
        block_dict = {}
        half_range = int(RenderRange / 2)
        for total in range(int(RenderRange / 2 * math.sqrt(3))):
            for x in range(-half_range, half_range):
                for y in range(-half_range // 2, half_range // 2):
                    for z in range(-half_range, half_range):
                        if abs(x) + abs(y) + abs(z) != total:
                            continue
                        if len(blocks) > max_block_num:
                            return blocks
                        elif len(blocks) > 0 and total > 24:
                            return blocks
                        elif total > 32:
                            return blocks
                        elif time.time() - start_time > max_time:
                            return blocks
                        block = getBlock(bot, Vec3, anchor_pos.x + x, anchor_pos.y + y, anchor_pos.z + z)
                        # filter grass air
                        hit = False
                        for tag in ['air']:
                            if tag in block["name"]:
                                hit = True
                                break
                        if hit:
                            continue

                        if 'bed' in block["name"] and block["_properties"]['part'] == 'head':
                            continue

                        if 'door' in block["name"] and block["_properties"]['part'] == 'upper':
                            continue

                        facing = block["_properties"]["axis"]
                        if not facing:
                            facing = block["_properties"]["facing"]
                            if facing == 'south':
                                facing = 'S'
                            elif facing == 'north':
                                facing = 'N'
                            elif facing == 'west':
                                facing = 'W'
                            elif facing == 'east':
                                facing = 'E'

                        # same block should only be added max_same_block times
                        if block['name'] in block_dict:
                            block_dict[block['name']] += 1
                            if block_dict[block['name']] > max_same_block:
                                continue
                        else:
                            block_dict[block['name']] = 1

                        if "potted" in block["name"]:
                            if facing:
                                blocks.append(
                                    {"flower_pot": [floor(block['position'].x), floor(block['position'].y), floor(block['position'].z)],
                                     "facing": facing})
                                blocks.append(
                                    {block["name"].replace("potted_", ""): [floor(block['position'].x), floor(block['position'].y), floor(block['position'].z)],
                                        "facing": facing})
                            else:
                                blocks.append(
                                    {"flower_pot": [floor(block['position'].x), floor(block['position'].y), floor(block['position'].z)]})
                                blocks.append(
                                    {block["name"].replace("potted_", ""): [floor(block['position'].x), floor(block['position'].y), floor(block['position'].z)]})

                        elif "_wall_" in block["name"]:
                            if facing:
                                blocks.append(
                                    {"name": block["name"].replace("_wall_", "_"), "position": [floor(block['position'].x), floor(block['position'].y), floor(block['position'].z)],
                                     "facing": facing})
                            else:
                                blocks.append(
                                    {"name": block["name"].replace("_wall_", "_"), "position": [floor(block['position'].x), floor(block['position'].y), floor(block['position'].z)]})



                        else:
                            if facing:
                                blocks.append(
                                    {"name": block["name"], "position": [floor(block['position'].x), floor(block['position'].y), floor(block['position'].z)],
                                     "facing": facing})
                            else:
                                blocks.append(
                                    {"name": block["name"], "position": [floor(block['position'].x), floor(block['position'].y), floor(block['position'].z)]})
        return blocks
    except Exception as e:
        print(e)
        return []


def BlocksSearch(bot, Vec3, mcData, RenderRange=5, hint="", count=-1, max_time=1):
    import math
    anchor_pos = bot.entity.position
    blocks = []
    RenderRange = min(RenderRange, 16)
    half_range = int(RenderRange / 2)
    start_time = time.time()
    for total in range(int(RenderRange / 2 * math.sqrt(3))):
        for x in range(-half_range, half_range):
            for y in range(-half_range // 2, half_range // 2):
                for z in range(-half_range, half_range):
                    if abs(x) + abs(y) + abs(z) != total:
                        continue
                    if len(blocks) > 10:
                        return blocks
                    elif len(blocks) > 0 and total > 16:
                        return blocks
                    elif total > 24:
                        return blocks
                    elif count > 0 and len(blocks) >= count:
                        return blocks
                    elif time.time() - start_time > max_time:
                        return blocks
                    block = getBlock(bot, Vec3, anchor_pos.x + x, anchor_pos.y + y, anchor_pos.z + z)
                    # filter air
                    hit = False
                    for tag in ['air', ]:
                        if tag in block["name"]:
                            hit = True
                            break
                    if hit:
                        continue

                    # #[DEBUG] print(block["name"],hint)
                    if hint not in block["name"]:
                        continue

                    if 'bed' in block["name"] and block["_properties"]['part'] == 'head':
                        continue

                    if 'door' in block["name"] and block["_properties"]['part'] == 'upper':
                        continue
                    # #[DEBUG] print(block)
                    blocks.append(block)

    random.shuffle(blocks)
    return blocks


def bag_info(bot):
    '''
    获取背包中的物品信息，并以字符串返回
    '''
    items = getInventoryItems(bot)
    # #[DEBUG] print(type(items))
    if len(items) == 0:
        str_items = "baglist empty"
        # lookAtPlayer(bot, entity['position'])
        return str_items
    elif items:
        str_items = 'I have '
        for item in items:
            str_items += f'{item["name"]}({item["count"]}) in my bag\n'
        # lookAtPlayer(bot, entity['position'])
        return str_items
    else:
        return "baglist open fail"


def chat_long(bot, name, message, type='msg'):
    '''
    防止不同版本的最长字数限制，分段传输
    '''
    if type == 'msg':
        if len(message) < 256:
            time.sleep(.5)
            bot.chat(f'msg {name} {message}')
            return
        while len(message) > 0:
            time.sleep(.5)
            bot.chat(f'msg {name} {message[:200]}' + '[SENDING]')
            message = message[200:]
        # bot.chat(f'msg {name} [SEND]')

    else:
        if len(message) < 256:
            time.sleep(.5)
            bot.chat(f'{name} talk_to {message}')
            return
        while len(message) > 0:
            time.sleep(.5)
            bot.chat(f'{name} talk_to {message[:200]}' + '[SENDING]')
            message = message[200:]
        bot.chat(f'{name} talk_to [SEND]')


def getEntityInfo(bot, entity, post_info, observation_list, perception_range):
    '''
    获取指定范围的实体信息
    '''
    try:
        if entity['username'] == bot.entity.username:
            return
        obs = ""
        if distanceTo(bot.entity.position, entity['position']) < perception_range:
            if entity['username']:
                obs = entity['username'] + f" {post_info}"
            else:
                obs = entity['name'] + f" {post_info}"
        if obs != "" and obs not in observation_list:
            observation_list.append(obs)
        return observation_list
    except:
        return observation_list


def name_check(bot, Vec3, mcData, name):
    '''
    检查llm输出的tag是否符合要求
    '''
    n, p_list = find_everything_(bot, Vec3, get_envs_info(bot, 128), mcData, name)
    if len(p_list) != 0 and n == name:
        return name
    else:
        name, tag = findSimilarName(name)
        return name



def mulList(elements, num):
    '''
    一个功能函数
    '''
    newList = []
    for i in elements:
        newList.append(i * num)
    return tuple(newList)


def get_envs_info(bot, RENDER_DISTANCE=16, same_entity_num=2):
    """
    实时更新的环境信息字典
    """
    global env_infos, update_time, update_interval
    if env_infos == None or time.time() - update_time > update_interval:
        update_time = time.time()

        def getEquipment(bot):
            slots = bot.inventory.slots
            heldItem = bot.heldItem
            return slots, heldItem

        def getEntities(bot):
            entities = bot.entities
            return entities

        def getTime(bot):
            timeOfDay = bot.time.timeOfDay
            if timeOfDay < 1000:
                time = "sunrise"
            elif timeOfDay < 3000:
                time = "day"  # 1000
            elif timeOfDay < 9000:
                time = "noon"  #
            elif timeOfDay < 15000:
                time = "sunset"  #
            elif timeOfDay < 18000:
                time = "night"
            elif timeOfDay < 23000:
                time = "midnight"
            else:
                time = "sunrise"
            return time

        health = bot.health
        food = bot.food
        saturation = bot.foodSaturation
        oxygen = bot.oxygenLevel
        position = bot.entity.position
        # velocity = bot.entity.velocity
        # yaw = bot.entity.yaw
        # pitch = bot.entity.pitch
        # onGround = bot.entity.onGround
        equipment = getEquipment(bot)

        name = bot.entity.username
        # timeSinceOnGround = bot.entity.timeSinceOnGround
        # isInWater = bot.entity.isInWater
        # isInLava = bot.entity.isInLava
        # isInWeb = bot.entity.isInWeb
        # isCollidedHorizontally = bot.entity.isCollidedHorizontally
        # isCollidedVertically = bot.entity.isCollidedVertically
        # biome = bot.blockAt(bot.entity.position).biome.name if bot.blockAt(bot.entity.position) else "None"
        entities = getEntities(bot)
        timeOfDay = getTime(bot)

        # inventoryUsed = bot.inventoryUsed()
        # elapsedTime = bot.globalTickCounter

        status_info = {
            'entities': entities,
            'my_name': name,
            'health': health,
            'food': food,
            'saturation': saturation,
            'oxygen': oxygen,
            'timeOfDay': timeOfDay,
            'position': position,
            # 'velocity': velocity,
            # 'yaw': yaw,
            # 'pitch': pitch,
            # 'onGround': onGround,
            'equipment': equipment,
            # 'timeSinceOnGround': timeSinceOnGround,
            # 'isInWater': isInWater,
            # 'isInLava': isInLava,
            # 'isInWeb': isInWeb,
            # 'isCollidedHorizontally': isCollidedHorizontally,
            # 'isCollidedVertically': isCollidedVertically,
            # 'biome': biome,
            # 'inventoryUsed': inventoryUsed,
            # 'elapsedTime': elapsedTime
        }
        # clean the dict
        env_infos = dict(status_info)
    return env_infos.copy()

def get_envs_info_dict(bot, RENDER_DISTANCE=32, same_entity_num=2):
    status_info = get_envs_info(bot, RENDER_DISTANCE, same_entity_num)

    if status_info['equipment'][1]:
        status_info['I_held_item'] = {status_info['equipment'][1]['name']: status_info['equipment'][1]['count']}
    else:
        status_info['I_held_item'] = {}
    status_info['equipment'] = "hidden"
    items_ = bot.inventory.items()
    if items_:
        status_info['inventory'] = [{item['name']: item['count']} for item in items_]
    else:
        status_info['inventory'] = []
    status_info['my_position'] = [int(status_info['position'].x + 0.5), int(status_info['position'].y + 0.5),
                                  int(status_info['position'].z + 0.5)]
    pos = status_info.pop('position')
    entities = []
    enitity_dict = {}
    for e in status_info['entities']:
        e = status_info['entities'][e]
        if e:
            s = {}
            if e.username is not None:
                if (bot.entity.username and e.username == bot.entity.username) or "judge" in e.username:
                    continue
                s['other_entity'] = e.username

            if e.position:
                if distanceTo(e.position, status_info['my_position']) > RENDER_DISTANCE:
                    continue

                if e.username:
                    s[f'{e.username}'] = [int(e.position.x + 0.5), int(e.position.y + 0.5), int(e.position.z + 0.5)]
                else:
                    s[f'{e.name}'] = [int(e.position.x + 0.5), int(e.position.y + 0.5), int(e.position.z + 0.5)]
            if e.heldItem:
                if e.username:
                    s[f'heldItem'] = e.heldItem.name
                else:
                    s[f'heldItem'] = e.heldItem.name
            if not enitity_dict.get(e.type):
                enitity_dict[e.type] = 1
            elif enitity_dict.get(e.type) < same_entity_num:
                enitity_dict[e.type] += 1
            else:
                continue
            entities.append(s)
    status_info['entities'] = entities

    status_info['nearby_entities'] = status_info.pop('entities')

    if status_info['oxygen'] is None:
        status_info['oxygen'] = 20  # 不在水下时，oxygen为None，这里设置为最大值20

    return status_info


def get_envs_info2str(bot, RENDER_DISTANCE=32, same_entity_num=2):
    """
    环境信息转字符串表示
    """
    status_info = get_envs_info_dict(bot, RENDER_DISTANCE, same_entity_num)

    # #[DEBUG] print(status_info)
    return str(status_info).replace("},", "},\n")


def get_agent_info2str(bot, RENDER_DISTANCE=32, idle=False, with_humans=False, name=""):
    '''
    获取agent的信息 可以包含human player的信息
    转换成字符串
    '''
    if idle:
        agent_status = load_agent_status()

    status_info = get_envs_info(bot, RENDER_DISTANCE)
    if name != "":
        search_info = []
        for e in status_info['entities']:
            e = status_info['entities'][e]
            if e:
                if e.username == name or e.name == name:
                    search_info.append(e)
        if len(search_info) == 0:
            return f"cannot find {name}.", 0
        else:
            return str(search_info[0]).replace("},", "},\n"), 1

    if status_info['equipment'][1]:
        status_info['I_held_item'] = {status_info['equipment'][1]['name']: status_info['equipment'][1]['count']}
    else:
        status_info['I_held_item'] = "I have nothing in my hand."
    status_info['equipment'] = "hidden"
    status_info['position'].x = int(status_info['position'].x + 0.5)
    status_info['position'].y = int(status_info['position'].y + 0.5)
    status_info['position'].z = int(status_info['position'].z + 0.5)
    pos = status_info.pop('position')
    status_info['my_position'] = [pos.x, pos.y, pos.z]
    entities = []
    for e in status_info['entities']:
        e = status_info['entities'][e]
        if e:
            if e.username:
                if e.username == bot.entity.username or "judge" in e.username:
                    continue
            else:
                continue
        else:
            continue

        if e and idle:
            if e.username not in agent_status.keys() and with_humans:  # this means the agent is a human player
                entities.append(e)
            elif e.username in agent_status.keys() and agent_status[e.username]['state'] == 'idle':
                entities.append(e)
        else:
            entities.append(e)

    entities_str = "nearby agents:\n"
    for e in entities:

        if e.heldItem:
            entities_str += f'{e.username} at {int(e.position.x + .5)} {int(e.position.y + .5)} {int(e.position.z + .5)} holding {e.heldItem.name}\n'
        else:
            entities_str += f'{e.username} at {int(e.position.x + .5)} {int(e.position.y + .5)} {int(e.position.z + .5)}\n'

    return entities_str, len(entities)


def load_agent_status():
    # get the num of json files
    num = 0
    for file in os.listdir('./agent_card'):
        if file.endswith('.json'):
            num += 1
    agent_status = {}
    for i in range(num):
        with open(f'./agent_card/{i}.json', 'r') as f:
            agent_card = json.load(f)
            agent_status[agent_card['name']] = agent_card
    return agent_status


def lookAtPlayer(bot, positon):
    bot.lookAt(positon.offset(0, 1.6, 0))


def findBlocks(bot, mcData, name, distance, count):
    blocks = bot.findBlocks(
        {
            "point": bot.entity.position,
            "matching": findSomething(bot, mcData, name, 'block'),
            "maxDistance": distance,
            "count": count,
        }
    )
    # #[DEBUG] print(blocks)
    return blocks


def random_walk(bot, Vec3, pathfinder, RANGE_GOAL):
    if bot.entity.velocity.x == 0 and bot.entity.velocity.z == 0 and abs(bot.entity.velocity.y) < 0.1:
        bot.pathfinder.setMovements(pathfinder.Movements(bot))
        goal_x = bot.entity.position.x + random.randint(-RANGE_GOAL, RANGE_GOAL)
        goal_z = bot.entity.position.z
        goal_y = bot.entity.position.y + random.randint(-RANGE_GOAL, RANGE_GOAL)
        flag, msg = move_to(pathfinder, bot, Vec3, RANGE_GOAL, Vec3(goal_x, goal_y, goal_z))
        if not flag:
            return f"random_walk walk failed, cannot reach random position ({goal_x}, {goal_y}, {goal_z})"
        else:
            return f" reach to random position ({goal_x}, {goal_y}, {goal_z})"


def get_entity_by(qtype, env_info, name, username=""):
    name = name.lower()
    get_entities = []
    assert qtype in ['name', 'uuid', 'type', 'username']
    for id in env_info['entities']:
        if env_info['entities'][int(id)] and env_info['entities'][int(id)][qtype]:
            pass
        else:
            continue
        if env_info['entities'][int(id)] == None or env_info['entities'][int(id)]['username'] == username:
            continue
        elif name.lower() == env_info['entities'][int(id)][qtype].split("_")[-1].lower() or name.lower() == env_info['entities'][int(id)][
            qtype].lower():
            # #[DEBUG] print(env_info['entities'][int(id)][qtype],name)
            get_entities.append(env_info['entities'][int(id)])
    # sort by position
    get_entities.sort(key=lambda x: distanceTo(x['position'], env_info['position']))
    return get_entities


def move_to(pathfinder, bot, Vec3, RANGE_GOAL, pos):  # √
    if pos is None:
        return False, "move failed, no target position"
    mv_ = pathfinder.Movements(bot)
    # #[DEBUG] print("Movements1",mv_)
    mv_.allow1by1towers = False
    mv_.canDig = False
    # #[DEBUG] print("Movements2",mv_)
    try_num = 3
    while try_num > 0:
        try:
            bot.pathfinder.setMovements(mv_)
            bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))
            break
        except Exception as e:
            # #[DEBUG] print(e)
            try_num -= 1
            time.sleep(1)

    if int(distanceTo(bot.entity.position, Vec3(pos.x, pos.y, pos.z))) >= 50:
        return False, f"move failed, can not reach position {pos.x} {pos.y} {pos.z} your pos: {bot.entity.position.x} {bot.entity.position.y} {bot.entity.position.z}, the position is too far away"

    max_steps = int(distanceTo(bot.entity.position, Vec3(pos.x, pos.y, pos.z)))
    while distanceTo(bot.entity.position, Vec3(pos.x, pos.y, pos.z)) >= RANGE_GOAL and max_steps > 0 and distanceTo(
            bot.entity.position, Vec3(pos.x, pos.y, pos.z)) > 1:
        try_num = 3
        while try_num > 0:
            try:
                bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 0.0))
                break
            except Exception as e:
                # #[DEBUG] print(e)
                try_num -= 1
                time.sleep(1)

        # time.sleep(1)
        # bot.chat('moving')
        max_steps -= 1

    if max_steps <= 0 and distanceTo(bot.entity.position, Vec3(pos.x, pos.y, pos.z)) >= RANGE_GOAL + 1.4:
        # # bot.chat('can not reach the position')
        if bot.blockAt(pos)['name'] == 'air':
            return False, f"move failed, can not reach position {pos.x} {pos.y} {pos.z}, the position is in the air, check the environment"
        else:
            return False, f"move failed, can not reach position {pos.x} {pos.y} {pos.z}, the position is blocked, check the environment"

    # bot.lookAt(pos.offset(0, 0, 0))

    return True, f" move to {pos.x} {pos.y} {pos.z}"


def find_nearest_(bot, Vec3, envs_info, mcData, name):  # X
    name, pos_list = find_everything_(bot, Vec3, envs_info, mcData, name, distance=128, count=10)
    # sort by distance
    pos_list.sort(key=lambda x: distanceTo(x, bot.entity.position))
    if len(pos_list) > 0:
        return pos_list[0]
    else:
        return None
    
def is_entity_or_item(name):
    # 已经确定是合法的名字但是不知道是实体还是方块
    with open('data/mcData.json', 'r', encoding='utf-8') as f:
        mc_data_json = json.load(f)
    for item in mc_data_json['entities']:
        if name == item[0]:
            return 'entity'
    for item in mc_data_json['items']:
        if name == item[0]:
            return 'item'

    return 'error'

def find_everything_(bot, Vec3, envs_info, mcData, name="", distance=32, count=1, optimize=False, visible_only=True):
    # 第一步判断name是否存在，如果不存在或者all, everything,则直接返回数量允许的所有物体
    # 第二步进行文本匹配，找到最相似的name
    # 第三步如果是entity,则直接返回entity的位置
    # 第四步如果是block,则进行搜索

    if name == "everything" or name == "all" or name == "":
        # 返回所有物体
        block_list = []
        try:
            blocks = bot.findBlocks(
                {
                    "point": bot.entity.position,
                    "matching": findSomething(bot, mcData, name, 'block')[0],
                    "maxDistance": distance,
                }
            )
            for block in blocks:
                block_list.append(block)

            # 去除相同名字超过三个的方块
            new_blocks = []
            block_dict = {}
            for block in block_list:
                if block["name"] in block_dict:
                    block_dict[block["name"]] += 1
                    if block_dict[block["name"]] > 3:
                        continue
                else:
                    block_dict[block["name"]] = 1
                new_blocks.append(block)
        except Exception as e:
            # [DEBUG] print(f'findBlocks block error: {e}')
            ...
        return "nearby blocks", block_list[:count]
    
    name_find, tag = findSimilarName(name)
    type_ = is_entity_or_item(name_find)
    # 有可能是entity的名字
    entities_pos = []
    # 直接返回entity的位置
    entities = get_entity_by('username', envs_info, name, bot.entity.username)
    if len(entities) > 0:
        pos = entities[0]['position']
        entities_pos.append(pos)
        return name, entities_pos
    if type_ == "error":
        return "Cannot find anything named " + name, []

    if type_ == "entity":
        entities_pos = []
        try:
            entities = get_entity_by('name', envs_info, name_find, bot.entity.username)
            for entity in entities:
                entities_pos.append(entity['position'])
            return name_find, entities_pos
        except Exception as e:
            # [DEBUG] print(f'find_everything_ name error: {e}')
            pos = None
        return "Cannot find any entity named " + name, []
    
    if type_ == "item":
        # 直接返回item的位置
        block_list = []
        try:
            blocks = bot.findBlocks(
                {
                    "point": bot.entity.position,
                    "matching": findSomething(bot, mcData, name_find, 'block')[0],
                    "maxDistance": distance,
                }
            )
            for block in blocks:
                block_list.append(block)

            new_blocks = []
            block_dict = {}
            for block in block_list:
                if block["name"] in block_dict:
                    block_dict[block["name"]] += 1
                    if block_dict[block["name"]] > 5:
                        continue
                else:
                    block_dict[block["name"]] = 1
                new_blocks.append(block)
            return name_find, new_blocks
        except Exception as e:
            return "Cannot find any block named " + name, []

def move_to_nearest_(pathfinder, bot, Vec3, envs_info, mcData, RANGE_GOAL, name):  # √
    pos = find_nearest_(bot,  Vec3, envs_info, mcData, name)

    if pos is None:
        return False, f"can not find anything named {name} nearby"

    return move_to(pathfinder, bot, Vec3, RANGE_GOAL, pos)


async def place_block(bot, Vec3, referencePos, faceVector, jump=False):
    referenceBlock = bot.blockAt(Vec3(referencePos[0], referencePos[1], referencePos[2]))
    if referenceBlock['name'] == 'air':
        # bot.chat('can not place block, the referenceBlock is air')
        return False
    max_try = 1
    if jump:
        bot.setControlState('jump', True)
    while max_try:
        try:
            if jump:
                time.sleep(0.1)
            await bot.placeBlock(referenceBlock, Vec3(faceVector[0], faceVector[1], faceVector[2]))
            break
        except:
            max_try -= 1
    # time.sleep(max_try)
    if jump:
        bot.setControlState('jump', False)

    if max_try <= 0:
        # bot.chat('can not place block')
        return False
    return True


async def place_axis(bot, mcData, pathfinder, Vec3, item_name, pos, axis=None):
    # [DEBUG] print('#place block axis {}'.format(axis))
    '''
    This function is used to place a block on the ground at the given position.
    '''
    # entity_near = bot.nearestEntity()
    # if entity_near:
    #     if distanceTo(entity_near.position, Vec3(pos[0], pos[1], pos[2])) < 1.5:
    #         return False, "can not place block, the position is too close to the entity who is at the position"
        
    if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] == item_name:
        return True, "the block is  placed there"
    
    if axis not in ['x', 'y', 'z', 'A', 'W', 'E', 'S', 'N', None]:
        return False, f"can not place block, the axis {axis} is not valid"
    
    # if bot.heldItem:
    #     bot.chat(f"I have {bot.heldItem.name} in my hand")
    # bot.chat('#equip item_name slot(hand,head,torso,legs,feet,off-hand)')
    done = True
    if bot.heldItem is None or bot.heldItem.name != item_name:
        msg, done = equip(bot, item_name, 'hand')
    
    if not done:
        # bot.chat('#can not place block, no item in hand')
        return False, f"can not place block, no {item_name} in hand, you need to interact chest or other container to get item first"
    hit = False
    if (bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] == 'dirt'):
        bot.dig(bot.blockAt(Vec3(pos[0], pos[1], pos[2])))
    # #[DEBUG] print(bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'])
    if (bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] == 'air' or bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] == 'flower_pot'):
        hit = True
    # elif bot.heldItem.name == 'scaffolding' and bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] == 'scaffolding':
    #     hit = True  # special case for scaffolding
    elif bot.heldItem.name == bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name']:
        return True, "the block is already there"
    if not hit:
        # bot.chat('#can not place block, the position is not air')
        return False, f"can not place block, the position is occupied by {bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name']}, you need to mine it first"
    done_msg = f" place block at {pos}"
    # bot.chat('#place block at {}'.format(pos))
    if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] == 'dirt' and 'dirt' != item_name:
        bot.dig(bot.blockAt(Vec3(pos[0], pos[1], pos[2])))
    GoalRange = 0.0
    MAX_STEPS = 50
    T_RANGE = 2
    origin_block_name = bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name']
    if origin_block_name != 'air' and origin_block_name != 'scaffolding':
        tag, flag, data = asyncio.run(interact_nearest(pathfinder, bot, Vec3, get_envs_info(bot), mcData, 2.0, origin_block_name))
        if flag:
            return True, done_msg
        else:
            return False, "cannot place flower"

    # 检查 6 方位是否有可能的参考块
    has_reference_block = False
    for offset in [[0, -1, 0], [0, 1, 0], [-1, 0, 0], [1, 0, 0], [0, 0, -1], [0, 0, 1]]:
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] != 'air':
            has_reference_block = True
            break
    if axis == 'N':
        offset = [0, 0, -1]
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] == 'air':
            return False, f"cannot place the block at this position facing {axis}, no valid other block at {pos[0] + offset[0]} {pos[1] + offset[1]} {pos[2] + offset[2]}, maybe some other blocks are needed to be placed first?"
    elif axis == 'S':
        offset = [0, 0, 1]
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] == 'air':
            return False, f"cannot place the block at this position facing {axis}, no valid other block at {pos[0] + offset[0]} {pos[1] + offset[1]} {pos[2] + offset[2]}, maybe some other blocks are needed to be placed first?"
    elif axis == 'W':
        offset = [-1, 0, 0]
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] == 'air':
            return False, f"cannot place the block at this position facing {axis}, no valid other block at {pos[0] + offset[0]} {pos[1] + offset[1]} {pos[2] + offset[2]}, maybe some other blocks are needed to be placed first?"
    elif axis == 'E':
        offset = [1, 0, 0]
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] == 'air':
            return False, f"cannot place the block at this position facing {axis}, no valid other block at {pos[0] + offset[0]} {pos[1] + offset[1]} {pos[2] + offset[2]}, maybe some other blocks are needed to be placed first?"

    elif axis == 'y':
        offset = [0, 1, 0]
        ground_y = pos[1]
        while bot.blockAt(Vec3(pos[0], ground_y - 1, pos[2]))['name'] == 'air':
            ground_y -= 1
        has_reference_block = False
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] != 'air':
            has_reference_block = True
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] - offset[1], pos[2] + offset[2]))['name'] != 'air':
            has_reference_block = True
        
        if not has_reference_block:
            return False, f"cannot place the block at this position facing {axis}, no valid other block at {pos[0] + offset[0]} {pos[1] + offset[1]} {pos[2] + offset[2]} or {pos[0] + offset[0]} {pos[1] - offset[1]} {pos[2] + offset[2]}. The ground block is at {pos[0]} {ground_y-1} {pos[2]}, maybe some other blocks are needed to be placed first?"   
    elif axis == 'x':
        offset = [1, 0, 0]
        has_reference_block = False
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] != 'air':
            has_reference_block = True
        if bot.blockAt(Vec3(pos[0] - offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] != 'air':
            has_reference_block = True
        
        if not has_reference_block:
            return False, f"cannot place the block at this position facing {axis}, no valid other block at {pos[0] + offset[0]} {pos[1] + offset[1]} {pos[2] + offset[2]} or {pos[0] - offset[0]} {pos[1] + offset[1]} {pos[2] + offset[2]}, maybe some other blocks are needed to be placed first?"
    elif axis == 'z':
        offset = [0, 0, 1]
        has_reference_block = False
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]))['name'] != 'air':
            has_reference_block = True
        if bot.blockAt(Vec3(pos[0] + offset[0], pos[1] + offset[1], pos[2] - offset[2]))['name'] != 'air':
            has_reference_block = True
        
        if not has_reference_block:
            return False, f"cannot place the block at this position facing {axis}, no valid other block at {pos[0] + offset[0]} {pos[1] + offset[1]} {pos[2] + offset[2]} or {pos[0] + offset[0]} {pos[1] + offset[1]} {pos[2] - offset[2]}, maybe some other blocks are needed to be placed first?"
        
    if not has_reference_block:
        # 找到正下方地面位置
        ground_y = pos[1]
        while bot.blockAt(Vec3(pos[0], ground_y - 1, pos[2]))['name'] == 'air':
            ground_y -= 1
        return False, f"cannot place the block at this position, no valid other block can be found, the ground block is at {pos[0]} {ground_y-1} {pos[2]}, maybe some other blocks are needed to be placed first?"

    flag = False
    offsets = {"y": [[0, -1, 0], [0, 1, 0]], "x": [[-1, 0, 0], [1, 0, 0]], "z": [[0, 0, -1], [0, 0, 1]]}  # 参考方块的位置偏移
    if axis == 'A' or axis is None or axis in ['x', 'y', 'z']:
        for x in range(0, T_RANGE * 2 + 1):
            if x % 2 == 0:
                x = - x // 2
            else:
                x = x // 2

            for z in range(0, T_RANGE * 2 + 1):
                if z % 2 == 0:
                    z = - z // 2
                else:
                    z = z // 2

                for y in range(0, T_RANGE * 2 + 1):
                    if y % 2 == 0:
                        y = - y // 2
                    else:
                        y = y // 2
                    if x == 0 and y == 0 and z == 0:
                        continue
                    # if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                    #    return True, done_msg
                    try:
                        if bot.blockAt(Vec3(pos[0] + x, pos[1] + y - 1, pos[2] + z))['name'] == 'air' or \
                                bot.blockAt(Vec3(pos[0] + x, pos[1] + y, pos[2] + z))['name'] != 'air':
                            # # bot.chat('#can not move to the position is not air')
                            continue
                        move_success = move_to(pathfinder, bot, Vec3, GoalRange,
                                               Vec3(pos[0] + x, pos[1] + y, pos[2] + z))
                        msg, done = equip(bot, item_name, 'hand')
                        if not move_success:
                            # # bot.chat('can not reach the position')
                            continue
                        
                        if axis == 'A' or axis is None:
                            offset_list = []
                            for offset in offsets.values():
                                offset_list += offset
                            for offset in offset_list:
                                putPos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])
                                faceVector = mulList(offset, -1)
                                if not flag and (bot.blockAt(Vec3(putPos[0], putPos[1], putPos[2])))['name'] != 'air':
                                    flag = await place_block(bot, Vec3, putPos, faceVector)
                                    if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                                        return True, done_msg
                        else:
                            for offset in offsets[axis]:
                                putPos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])
                                faceVector = mulList(offset, -1)
                                if not flag and (bot.blockAt(Vec3(putPos[0], putPos[1], putPos[2])))['name'] != 'air':
                                    flag = await place_block(bot, Vec3, putPos, faceVector)
                                    if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                                        return True, done_msg

                        if not flag:
                            # # bot.chat('can not place block')
                            continue
                    except Exception as e:
                        # bot.chat(f'can not place block: {e}')
                        continue
                    # return False, "can not place block"
        return False, f"cannot place the block at this position, no valid reference block can be found or just to high to reach, you might need to place some support blocks first, and mine them after the block is placed"
    if axis == 'W' or axis == 'A' or axis is None:
        for x in range(1, T_RANGE + 1):
            for z in range(0, abs(x) * 2 + 1):
                if z % 2 == 0:
                    z = - z // 2
                else:
                    z = z // 2
                for y in range(0, T_RANGE * 2 + 1):
                    if y % 2 == 0:
                        y = - y // 2
                    else:
                        y = y // 2

                    # if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                    #    return True, done_msg
                    try:
                        if bot.blockAt(Vec3(pos[0] + x, pos[1] + y - 1, pos[2] + z))['name'] == 'air' or \
                                bot.blockAt(Vec3(pos[0] + x, pos[1] + y, pos[2] + z))['name'] != 'air':
                            # # bot.chat('#can not move to the position is not air') 机器人身高是2
                            continue
                        move_success = move_to(pathfinder, bot, Vec3, GoalRange,
                                               Vec3(pos[0] + x, pos[1] + y, pos[2] + z))
                        msg, done = equip(bot, item_name, 'hand')
                        if not move_success:
                            # # bot.chat('can not reach the position')
                            continue
                        for item in offsets.values():
                            for offset in item:
                                putPos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])  # putpos 参考方块
                                faceVector = mulList(offset, -1)  # 放置朝向
                                if not flag and (bot.blockAt(Vec3(putPos[0], putPos[1], putPos[2])))['name'] != 'air':
                                    flag = await place_block(bot, Vec3, putPos, faceVector)
                                    if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                                        return True, done_msg

                        if not flag:
                            # # bot.chat('can not place block')
                            continue
                    except Exception as e:
                        # # bot.chat(f'can not place block: {e}')
                        continue
        return False, f"cannot place the block at {pos}, no valid reference block can be found"
    elif axis == 'E' or axis == 'A' or axis is None:
        for x in range(1, T_RANGE + 1):
            x = -x
            for z in range(0, abs(x) * 2 + 1):
                if z % 2 == 0:
                    z = - z // 2
                else:
                    z = z // 2
                for y in range(0, T_RANGE * 2 + 1):
                    if y % 2 == 0:
                        y = - y // 2
                    else:
                        y = y // 2

                    # if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                    #    return True, done_msg
                    try:
                        if bot.blockAt(Vec3(pos[0] + x, pos[1] + y - 1, pos[2] + z))['name'] == 'air' or \
                                bot.blockAt(Vec3(pos[0] + x, pos[1] + y, pos[2] + z))['name'] != 'air':
                            # # bot.chat('#can not move to the position is not air')
                            continue
                        move_success = move_to(pathfinder, bot, Vec3, GoalRange,
                                               Vec3(pos[0] + x, pos[1] + y, pos[2] + z))
                        msg, done = equip(bot, item_name, 'hand')
                        if not move_success:
                            # # bot.chat('can not reach the position')
                            continue
                        for item in offsets.values():
                            for offset in item:
                                putPos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])
                                faceVector = mulList(offset, -1)
                                if not flag and (bot.blockAt(Vec3(putPos[0], putPos[1], putPos[2])))['name'] != 'air':
                                    flag = await place_block(bot, Vec3, putPos, faceVector)
                                    if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                                        return True, done_msg
                        if not flag:
                            # # bot.chat('can not place block')
                            continue
                    except Exception as e:
                        # # bot.chat(f'can not place block: {e}')
                        continue
        return False, f"cannot place the block at this position, no valid reference block can be found, maybe you should place reference block first"
    elif axis == 'N' or axis == 'A' or axis is None:
        for z in range(1, T_RANGE + 1):
            for x in range(0, abs(z) * 2 + 1):
                if x % 2 == 0:
                    x = - x // 2
                else:
                    x = x // 2
                for y in range(0, T_RANGE * 2 + 1):
                    if y % 2 == 0:
                        y = - y // 2
                    else:
                        y = y // 2

                    # if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                    #    return True, done_msg
                    try:
                        if bot.blockAt(Vec3(pos[0] + x, pos[1] + y - 1, pos[2] + z))['name'] == 'air' or \
                                bot.blockAt(Vec3(pos[0] + x, pos[1] + y, pos[2] + z))['name'] != 'air':
                            # # bot.chat('#can not move to the position is not air')
                            continue
                        move_success = move_to(pathfinder, bot, Vec3, GoalRange,
                                               Vec3(pos[0] + x, pos[1] + y, pos[2] + z))
                        msg, done = equip(bot, item_name, 'hand')
                        if not move_success:
                            # # bot.chat('can not reach the position')
                            continue
                        for item in offsets.values():
                            for offset in item:
                                putPos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])
                                faceVector = mulList(offset, -1)
                                if not flag and (bot.blockAt(Vec3(putPos[0], putPos[1], putPos[2])))['name'] != 'air':
                                    flag = await place_block(bot, Vec3, putPos, faceVector)
                                    if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                                        return True, done_msg
                        if not flag:
                            # # bot.chat('can not place block')
                            continue
                    except Exception as e:
                        # # bot.chat(f'can not place block: {e}')
                        continue
        return False, f"cannot place the block at this position, no valid reference block can be found"
    elif axis == 'S' or axis == 'A' or axis is None:
        for z in range(1, T_RANGE + 1):
            z = -z
            for x in range(0, abs(z) * 2 + 1):
                if x % 2 == 0:
                    x = - x // 2
                else:
                    x = x // 2
                for y in range(0, T_RANGE * 2 + 1):
                    if y % 2 == 0:
                        y = - y // 2
                    else:
                        y = y // 2

                    # if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                    #    return True, done_msg
                    try:
                        if bot.blockAt(Vec3(pos[0] + x, pos[1] + y - 1, pos[2] + z))['name'] == 'air' or \
                                bot.blockAt(Vec3(pos[0] + x, pos[1] + y, pos[2] + z))['name'] != 'air':
                            # # bot.chat('#can not move to the position is not air')
                            continue
                        move_success = move_to(pathfinder, bot, Vec3, GoalRange,
                                               Vec3(pos[0] + x, pos[1] + y, pos[2] + z))
                        msg, done = equip(bot, item_name, 'hand')
                        if not move_success:
                            # # bot.chat('can not reach the position')
                            continue
                        for item in offsets.values():
                            for offset in item:
                                putPos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])
                                faceVector = mulList(offset, -1)
                                if not flag and (bot.blockAt(Vec3(putPos[0], putPos[1], putPos[2])))['name'] != 'air':
                                    flag = await place_block(bot, Vec3, putPos, faceVector)
                                    if bot.blockAt(Vec3(pos[0], pos[1], pos[2]))['name'] != origin_block_name:
                                        return True, done_msg
                        if not flag:
                            # # bot.chat('can not place block')
                            continue
                    except Exception as e:
                        # # bot.chat(f'can not place block: {e}')
                        continue
        return False, f"cannot place the block at this position, no valid reference block can be found"

dig_file = "data/dig_item.json"
dig_data = json.load(open(dig_file, "r"))

def dig_check(bot,item_name):
    for item in dig_data:
        if item_name == item["name"]:
            if not item["diggable"]:
                return False, "this block cannot dig"
            # 确定手持物品
            held_item = bot.heldItem
            if held_item is None and "tools" in item:
                return False, "you need to hold a tool to dig this block, tools can be built by crafting table or try find it in chest"
            elif held_item is not None and "tools" in item and held_item.name not in item["tools"]:
                return False, "you need to hold a tool to dig this block, tools can be built by crafting table or try find it in chest"
            return True, "this block can dig"
    return False, "this block cannot dig"

def dig_block(bot, offset):
    # [DEBUG] print('try dig')
    target = bot.blockAt(bot.entity.position.offset(offset[0], offset[1], offset[2]))
    tag, msg = dig_check(bot, target.name)
    if target and tag:
        try:
            bot.dig(target)
        except Exception as e:
            # bot.chat(f'{e}')
            print(f'{e}')
    elif not tag:
        return "dig failed because " + msg
    else:
        if target:
            return "this block cannot dig"
        else:
            return "dig failed because there is nothing"


def distanceTo(pos1, pos2):
    try:
        return ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2 + (pos1.z - pos2.z) ** 2) ** 0.5
    except Exception as e:
        # #[DEBUG] print(f'distanceTo warning: {e},{pos1},{pos2}')
        pass

    try:
        if type(pos1) == list and type(pos2) == list:
            _dis = ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5
        elif type(pos1) == list and type(pos2) != list:
            _dis = ((pos1[0] - pos2.x) ** 2 + (pos1[1] - pos2.y) ** 2 + (pos1[2] - pos2.z) ** 2) ** 0.5
        elif type(pos1) != list and type(pos2) == list:
            _dis = ((pos1.x - pos2[0]) ** 2 + (pos1.y - pos2[1]) ** 2 + (pos1.z - pos2[2]) ** 2) ** 0.5
        else:
            _dis = ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2 + (pos1.z - pos2.z) ** 2) ** 0.5
        # #[DEBUG] print(f'distance {pos1.x} {pos1.y} {pos1.z} - {pos2.x} {pos2.y} {pos2.z} {_dis}')

        return _dis
    # if pos1 is list and pos2 is list:

    except Exception as e:
        # [DEBUG] print(f'distanceTo error: {e},{pos1},{pos2}')
        return 1000


def dig_at(bot, pathfinder, Vec3, pos):
    max_retry = 2
    while max_retry > 0:
        flag, msg = move_to(pathfinder, bot, Vec3, 2, Vec3(pos[0], pos[1], pos[2]))
        if not flag:
            return f"dig failed, cannot reach to {pos}", False
        try:
            target = bot.blockAt(Vec3(pos[0], pos[1], pos[2]))
            tag, msg = dig_check(bot, target.name)
            if target and tag:
                bot.dig(target)
                return f" dig at {pos}", True
            elif not tag:
                # bot.chat(f'cannot dig because {msg}')
                return f"cannot dig {target.name} at position{pos}, because {msg}", False
            elif target:
                # bot.chat(f'can not dig')
                return f"cannot dig {target.name} at position{pos}", False
            else:
                # bot.chat(f'no target')
                return f"cannot dig, no block at {pos}", False

        except Exception as e:
            bot.chat(f'dig_at error: {e}')
            max_retry -= 1
            random_offset = [random.randint(-4, 4), random.randint(-4, 4)]
            move_to(pathfinder, bot, Vec3, 2, Vec3(pos[0] + random_offset[0], pos[1], pos[2] + random_offset[1]))
    return "dig failed, might be api wrong", False

async def attack(bot, envs_info, mcData, mobName=None):
    weaponsForShooting = [
        "bow",
        "crossbow",
        "snowball",
        "ender_pearl",
        "egg",
        "splash_potion",
        "trident",
    ]
    try:
        # [DEBUG] 
        # bot.chat("attack")
        entity = bot.nearestEntity()
        if mobName == None:
            pass
        else:
            # try:
            #     entities = get_entity_by('username', envs_info, mobName, bot.entity.username)
            #     if len(entities) > 0:
            #         entity = entities[0]
            # except Exception as e:
            #     bot.chat(f'find_everything_ username error: {e}')
            if entity == None:
                try:
                    entities = get_entity_by('name', envs_info, mobName, bot.entity.username)
                    if len(entities) > 0:
                        entity = entities[0]
                except Exception as e:
                    bot.chat(f'find_everything_ name error: {e}')
            if entity == None:
                try:
                    entities = get_entity_by('type', envs_info, mobName, bot.entity.username)
                    if len(entities) > 0:
                        entity = entities[0]
                except Exception as e:
                    bot.chat(f'find_everything_ name error: {e}')
                    entity = None
        if entity == None:
            # bot.chat("No nearby entities")
            return "entity cannot be found nearby", False
        if entity.name == "player":
            try:
                entities = get_entity_by('name', envs_info, mobName, bot.entity.username)
                if len(entities) > 0:
                    entity = entities[0]

            except Exception as e:
                bot.chat(f'find_everything_ name error: {e}')
                return "cannot attack player", False
        
        mainHandItem = bot.inventory.slots[bot.getEquipmentDestSlot("hand")]
        attack_creatures = [
            "rabbit",
            "bat",
            "cat",
            "chicken",
            "cod",
            "cow",
            "pig",
            "blaze",
            "cave_spider",
            "creeper",
            "drowned",
            "elder_guardian",
            "ender_dragon",
            "enderman",
            "endermite",
            "evoker",
            "ghast",
            "guardian",
            "hoglin",
            "husk",
            "illusioner",
            "magma_cube",
            "phantom",
            "piglin",
            "piglin_brute",
            "pillager",
            "ravager",
            "shulker",
            "silverfish",
            "skeleton",
            "slime",
            "spider",
            "stray",
            "vex",
            "vindicator",
            "witch",
            "wither",
            "wither_skeleton",
            "zoglin",
            "zombie",
            "zombie_villager",
            "zombified_piglin",
        ]
        if mainHandItem == None or mainHandItem['name'] not in weaponsForShooting and entity.name in attack_creatures:
            # bot.chat(f"Attacking {entity.name if entity.name else entity.username}")
            bot.pvp.attack(entity)
            time.sleep(1)
            bot.pvp.stop()
            if mainHandItem == None:
                return f" attack {entity.name if entity.name else entity.username}", True
            return f"held {mainHandItem['name']} and tried attack {entity.name if entity.name else entity.username} for 5 sec", True

        else:
            bot.hawkEye.autoAttack(entity, mainHandItem.name)
            time.sleep(1)
            bot.hawkEye.stop()
            return f" used {mainHandItem['name']} and tried attack {entity.name if entity.name else entity.username} for 5 sec", True
    except Exception as e:
        # [DEBUG] 
        bot.pvp.stop()
        bot.hawkEye.stop()
        return "failed to attack.", False


async def interact_nearest(pathfinder, bot,  Vec3, envs_info, mcData, RANGE_GOAL, name, get_item_name=None, count=1,
                           repair_item_name=None, fuel_item_name=None, target_position=None):
    # [DEBUG] print('interact nearest',name,bot.heldItem)
    if bot.heldItem and name == bot.heldItem.name:
        # [DEBUG] print('interact with held item')
        msg, tag = interactItem(bot, name)
        return msg, tag, []
    if target_position is not None:
        pos = target_position
    else:
        pos = find_nearest_(bot, Vec3, envs_info, mcData, name)
    if pos is None:
        return f"cannot find anything named {name}, try to get more infos or help", False, []

    # 用 findSimilarName 处理一下 name get_item_name repair_item_name fuel_item_name
    if get_item_name is not None:
        raw_get_item_name = get_item_name
        get_item_name = findSimilarName(get_item_name)[0]
        if get_item_name == "":
            get_item_name = raw_get_item_name
    if repair_item_name is not None:
        raw_repair_item_name = repair_item_name
        repair_item_name = findSimilarName(repair_item_name)[0]
        if repair_item_name == "":
            repair_item_name = raw_repair_item_name
    if fuel_item_name is not None:
        raw_fuel_item_name = fuel_item_name
        fuel_item_name = findSimilarName(fuel_item_name)[0]
        if fuel_item_name == "":
            fuel_item_name = raw_fuel_item_name
    if name is not None:
        raw_name = name
        name = findSimilarName(name)[0]
        if name == "" or "crafting" in raw_name or "container" in raw_name or "chest" in raw_name or "furnace" in raw_name:
            name = raw_name

    mv_config = pathfinder.Movements(bot)
    mv_config.canDig = False # 决定是否可以挖掘
    mv_config.allow1by1towers = False 
    max_tries = 3
    while max_tries > 0:
        try:
            bot.pathfinder.setMovements(mv_config)
            bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))
            break
        except Exception as e:
            max_tries -= 1
            pass
    max_steps = int(distanceTo(bot.entity.position, pos))
    if max_steps > 20:
        return f"cannot reach {name}, it is too far away", False, []
    
    while distanceTo(bot.entity.position, pos) > RANGE_GOAL and max_steps > 0:
        # bot.chat(f'#distance to {name} {distanceTo(bot.entity.position,pos)}')
        try:
            bot.pathfinder.setMovements(mv_config)
            bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 1))
        except Exception as e:
            pass
        time.sleep(1)
        max_steps -= 1

    if max_steps <= 0 and distanceTo(bot.entity.position, pos) > RANGE_GOAL:
        # bot.chat(f'can not reach {pos}')
        return f'can not reach {pos.x} {pos.y} {pos.z}', False, []

    if 'crafting' in name:
        recipe_data = []
        try:
            craftingTable = bot.findBlock({
                "matching": mcData.blocksByName.crafting_table.id,
            })
            # bot.chat(f'#opened crafting table {name}')
            if not get_item_name:
                return f" open crafting table {name}, what do you want to craft?", True, recipe_data
            recipe = bot.recipesFor(mcData.itemsByName[get_item_name].id, None, count, craftingTable)[0]
            _recipes = []
            for r in bot.recipesAll(mcData.itemsByName[get_item_name].id, None, craftingTable):
                _recipes.append(r)
            _recipe = random.choice(_recipes)
            # [DEBUG] print(_recipe)
            # input()
            if _recipe is None:
                return f"There is no recipe for {get_item_name} in crafting table, what do you want to craft?", False, recipe_data
            try:
                result_id = _recipe['result']['id']
                recipe_str = "one example recipe is:"
                for item in _recipe['delta']:
                    # id to name
                    if item['id'] == result_id:
                        continue
                    # [DEBUG] print(item)
                    recipe_str += f" {mcData.items[item['id']]['name']} X {abs(item['count'])},"
                    recipe_data.append({'name': mcData.items[item['id']]['name'], 'count': abs(item['count'])})

                if recipe is None:
                    return f'I cannot make {get_item_name} now, check your inventory. {recipe_str}', False, recipe_data

                bot.craft(recipe, count, craftingTable)
                return f"I made {get_item_name} X {count}.", True, recipe_data
            except Exception as e:
                # bot.chat(f'I cannot make {get_item_name}')
                # [DEBUG] print(f'I cannot make {get_item_name} {e}')
                return f'I cannot make {get_item_name}, maybe you should get more. {recipe_str}', False, recipe_data
        except Exception as e:
            # bot.chat(f'unable to open crafting table: {e}')
            return f'unable to open crafting table {name}', False, recipe_data

    if 'container' in name or 'chest' in name:
        chest = None
        chest_data = []
        if bot.blockAt(pos)['name'] != 'chest' and 'container' not in bot.blockAt(pos)['name']:
            return f"the block at {pos.x}  {pos.y} {pos.z} is not a chest or container, it is {bot.blockAt(pos)['name']}", False, chest_data
        try:
            chest = bot.openChest(bot.blockAt(pos))
            # bot.chat(f'#opened chest {name}')
            target_item = None
            # #[DEBUG] print(chest.containerItems())
            chest_str = "It contains:"
            for item in chest.containerItems():
                chest_str += item['name'] + " "
                chest_data.append({'name': item['name'], 'count': item['count']})
            if get_item_name == None or get_item_name == '' or get_item_name == 'all' or get_item_name == 'everything':
                chest.close()
                return f" open {name}, (didn't get them out)" + chest_str, True, chest_data
            if not get_item_name:
                chest.close()
                return f" open {name}, " + chest_str, True, chest_data
            if count < 0:
                for item in chest.containerItems():
                    if get_item_name in item['name']:
                        target_item = item
                        break
                if target_item is None:
                    chest.close()
                    return f"cannot find enough {get_item_name} in it, " + chest_str, False, chest_data

                chest.withdraw(target_item['type'], None, abs(count))
                chest.close()
                return f" open {name}, and withdraw {get_item_name} X {abs(count)} from it", True, chest_data

            else:
                items = getInventoryItemByName(bot, get_item_name)
                if len(items) < count:
                    for item in chest.containerItems():
                        if get_item_name in item['name']:
                            target_item = item
                            break
                    if target_item is None:
                        chest.close()
                        return f"No enough {get_item_name} in {name} or in my bag." + chest_str, False, chest_data

                    chest.withdraw(target_item['type'], None, abs(count))
                    chest.close()
                    return f"Warning I don't have {count} X {get_item_name} in my bag. Execute -{count} X {get_item_name} to get from {name}.", True, chest_data
                chest.deposit(mcData.itemsByName[get_item_name].id, None, count)
                chest.close()
                return f" open {name}, and deposit {get_item_name} X {count} to it", True, chest_data
        except Exception as e:
            bot.chat(f'unable to open it: {e}')
            if chest:
                chest.close()
            return f'unable to open {name}', False, chest_data

    if 'furnace' in name:
        fuel_data = []
        if fuel_item_name == None and get_item_name == None:
            furnaceBlock = bot.findBlock({
                "matching": mcData.blocksByName.furnace.id,
                "maxDistance": 16,
            })
            if not furnaceBlock:
                return f"No furnace nearby", False
            try:
                furnace = bot.openFurnace(furnaceBlock)
                if furnace.inputItem() and furnace.fuelSeconds and furnace.fuelSeconds > 1:
                    fuel_data.append({'name': furnace.inputItem()['name'], 'count': furnace.inputItem()['count']})
                    furnace.close()
                    if furnace.fuelItem():
                        fuel_data.append({'name': furnace.fuelItem()['name'], 'count': furnace.fuelItem()['count']})
                        return f"the furnace is still working for {furnace.inputItem()['name']}({furnace.inputItem()['count']}) use {furnace.fuelItem()['name']}({furnace.fuelItem()['count']})", True, {"furnace_info":fuel_data}
                    return f"the furnace is still working for {furnace.inputItem()['name']}({furnace.inputItem()['count']})", True, {"furnace_info":fuel_data}
                if furnace.outputItem():
                    max_tries = 3
                    while max_tries > 0:
                        try:
                            fuel_data.append({'name': furnace.outputItem()['name'], 'count': furnace.outputItem()['count']})
                            furnace.takeOutput()
                            furnace.close()
                            return f"the furnace is empty and I took {furnace.outputItem()['name']} X {furnace.outputItem()['count']} from furnace.", True, {"furnace_info":fuel_data}
                        except Exception as e:
                            max_tries -= 1
                            pass
                furnace.close()
                return f"the furnace is empty", True, {"furnace_info":fuel_data}
            except Exception as e:
                # bot.chat(f'unable to open furnace {name}')
                # [DEBUG] print(f'unable to open furnace {name} {e}')
                return f'your action is executed, but system check furnace failed for several reasons, please retry', False, {"furnace_info":fuel_data}

        furnaceBlock = bot.findBlock({
            "matching": mcData.blocksByName.furnace.id,
            "maxDistance": 16,
        })
        if not furnaceBlock:
            return f"No furnace nearby", False, {"furnace_info":fuel_data}
        fuel_data = []
        try:
            furnace = bot.openFurnace(furnaceBlock)
            # [DEBUG] print(furnace)
            # bot.chat(f'#opened furnace {name}')
            if furnace.inputItem():
                fuel_data.append({'name': furnace.inputItem()['name'], 'count': furnace.inputItem()['count']})
            if furnace.fuelItem():
                fuel_data.append({'name': furnace.fuelItem()['name'], 'count': furnace.fuelItem()['count']})
            if furnace.outputItem():
                fuel_data.append({'name': furnace.outputItem()['name'], 'count': furnace.outputItem()['count']})
                
            if not get_item_name:
                furnace.close()
                return f" open furnace {name}", True, {"furnace_info":fuel_data}
            if furnace.fuelSeconds and furnace.fuelSeconds > 1:
                furnace.close()
                return f"the furnace is still working for {furnace.inputItem()['name']}", False, {"furnace_info":fuel_data}
            if not furnace.inputItem():
                item = mcData.itemsByName[get_item_name]
                if not item:
                    return f"No item named {get_item_name}", False, {"furnace_info":fuel_data}
                bot.updateHeldItem()
                time.sleep(1)
                if countInventoryItems(bot,get_item_name)[1] < count:
                    return f"No enough {get_item_name}", False, {"furnace_info":fuel_data}
                furnace.putInput(item.id, None, count)
                time.sleep(.1)
            if fuel_item_name:
                fuel = mcData.itemsByName[fuel_item_name]
                if not fuel:
                    return f"No item named {fuel_item_name}", False, {"furnace_info":fuel_data}
                if len(getInventoryItemByName(bot, fuel_item_name)) < 1 and furnace.fuelItem()['count'] < 1:
                    furnace.close()
                    return f"No {fuel_item_name} as fuel in inventory", False, {"furnace_info":fuel_data}
                furnace.putFuel(fuel.id, None, 1)
                time.sleep(.1)
                if furnace.fuelItem() and furnace.fuelItem()['name'] != fuel_item_name:
                    furnace.close()
                    return f"{fuel_item_name} is not a valid fuel", False, {"furnace_info":fuel_data}
            
                max_wait = 30
                while not furnace.outputItem() and max_wait > 0:
                    max_wait -= 1
                    time.sleep(1)
                    bot.chat(f'waiting for {get_item_name} to be produced')
                    
                furnace.takeOutput()
                time.sleep(.2)
                furnace.close()
                return f"I put {fuel_item_name} as fuel in furnace and get {name}", True, {"furnace_info":fuel_data}

        except Exception as e:
            # bot.chat(f'unable to open furnace {name}')
            # [DEBUG] print(f'unable to open furnace {name} {e}')
            return f'you action is executed, but system check furnace failed for several reasons, mostly because material is not enough', False, {"furnace_info":fuel_data}

    if 'enchanting_table' in name:  # TODO Not Supported yet
        enchantTableBlock = bot.findBlock({
            "matching": mcData.blocksByName.enchanting_table.id,
            "maxDistance": 16,
        })
        if not enchantTableBlock:
            return f"No enchantment nearby", False
        table = bot.openEnchantmentTable(enchantTableBlock)
        try:
            items = getInventoryItemByName(bot, get_item_name)
            if len(items) == 0:
                return f"No {get_item_name} in my bag", False
            table.putTargetItem(items[0])
            # while table.enchantments[0].level < 0:
            #     #[DEBUG] print(table.enchantments)
            #     time.sleep(1)

            items = getInventoryItemByName(bot, "dye")
            items += getInventoryItemByName(bot, "lapis_lazuli")
            if len(items) == 0:
                return f"I don't have any lapis", False
            try:
                table.putLapis(items[0])
            except Exception as e:
                # [DEBUG] print(e)
                pass

            table.enchant(random.randint(0, 3), timeout=3)
            table.takeTargetItem()

            return f' enchant the {get_item_name}', True
        except Exception as e:
            # [DEBUG] print(e)
            # # bot.chat(f'unable to open enchantment table {name}')
            return f"I don't have enough exp and lapis.", False

    if 'anvil' in name:  # TODO check issue
        try:
            anvilBlock = bot.findBlock({
                "matching": mcData.blocksByName.anvil.id,
            })
            anvil = bot.openAnvil(anvilBlock)
            # bot.chat(f'#opened anvil {name}')
            try:
                # bot.chat('Using the anvil...')
                anvil.combine(getInventoryItemByName(bot, repair_item_name)[0],
                              getInventoryItemByName(bot, get_item_name)[0], repair_item_name)
                # bot.chat('Anvil used .')
                return f" open anvil {name}", True
            except Exception as e:
                # bot.chat(f'unable to open anvil {name}')
                # [DEBUG] print(e)
                return f'unable to open anvil {name} ', False
        except Exception as e:
            # bot.chat(f'unable to open anvil {name}')
            return f'unable to open anvil {name} {e}', False

    if 'villager' in name or 'trader' in name:
        villager_data = []
        try:
            entities = get_entity_by('name', envs_info, name, bot.entity.username)
            entity = entities[0]
            if entity.entityType != bot.registry.entitiesByName.villager.id:
                # bot.chat(f'entity {name} {entity.entityType} is not a villager {bot.registry.entitiesByName.villager.id}')
                pass
            villager = bot.openVillager(entity)
            # [DEBUG] print(villager.trades)
            trade_str = "the villager trades:"
            for trade in villager.trades:
                if trade['inputItem2']:
                    villager_data.append({'inputItem1': trade['inputItem1']['name'], 'inputCount1': trade['inputItem1']['count'], 'inputItem2': trade['inputItem2']['name'], 'inputCount2': trade['inputItem2']['count'], 'outputItem': trade['outputItem']['name'], 'outputCount': trade['outputItem']['count']})
                    trade_str += f"use {trade['inputItem1']['name']} X {trade['inputItem1']['count']} + {trade['inputItem2']['name']} X {trade['inputItem2']['count']} for {trade['outputItem']['name']} X {trade['outputItem']['count']} "
                else:
                    villager_data.append({'inputItem1': trade['inputItem1']['name'], 'inputCount1': trade['inputItem1']['count'], 'inputItem2': 'empty', 'inputCount2': 0, 'outputItem': trade['outputItem']['name'], 'outputCount': trade['outputItem']['count']})
                    trade_str += f"use {trade['inputItem1']['name']} X {trade['inputItem1']['count']} for {trade['outputItem']['name']} X {trade['outputItem']['count']} "
            # bot.chat(f'#opened villager {name}')
            if not get_item_name:
                villager.close()
                return f" open villager {name}, " + trade_str, True, villager_data

            target_trade = None
            for idx, trade in enumerate(villager.trades):
                if get_item_name in trade['outputItem']['name']:
                    target_trade = idx
                    break
            if target_trade is None:
                villager.close()
                return f"cannot find {get_item_name} in villager, " + trade_str, False, villager_data
            bot.trade(villager, target_trade, count)
            villager.close()
            return f" open villager {name}, " + trade_str, True, villager_data
        except Exception as e:
            # bot.chat(f'unable to open villager {name}')
            # [DEBUG] print(f'unable to open villager {name} {e}')
            return f'unable to open villager {name}', False, villager_data

    try:
        bot.activateEntityAt(bot.entity, pos)
        # bot.chat(f'activated entity {name}')

        bot.activateBlock(bot.blockAt(pos))
        # bot.chat(f'#activated block {name}')
        return f" activate {name}", True, []
    except Exception as e:
        bot.chat(f'unable to activate {name}')

    return f'unable to activate {name}', False, []


def getInventoryItemByName(bot, item_name, count=1):
    try:
        items = bot.inventory.items()
        getItems = []
        for item in items:
            if item_name in item['name']:
                getItems.append(item)
        # #[DEBUG] print(getItems)
        return getItems[:count]
    except Exception as e:
        # bot.chat(f'unable to get inventory: {e}')
        return []


def sleep(bot, Vec3, mcData):
    # bot.chat('/time set night')
    try:
        bedBlock = BlocksSearch(bot, Vec3, mcData, 16, 'bed', count=1)
        if bedBlock is None:
            return "failed to sleep because no bed found"
        bedBlock = bedBlock[0]
        if bot.isABed(bedBlock):
            bot.sleep(bedBlock)
            return " sleep"
        else:
            # bot.chat("#No nearby bed")
            return "failed to sleep because no bed found"
    except Exception as e:
        # bot.chat(f'unable to sleep: {e}')
        return "failed to sleep"


def wake(bot):
    # bot.chat('/time set day')
    bot.wake()
    return " wake up"


def getInventoryItems(bot):
    try:
        items = bot.inventory.items()
        for item in items:
            bot.chat(item['name'])
            bot.chat(item['count'])
        return items
    except Exception as e:
        # bot.chat(f'unable to get inventory: {e}')
        return None


def findInventoryItems(bot, name):
    try:
        items = bot.inventory.items()
        for item in items:
            if name in item['name']:
                return True

        return False
    except Exception as e:
        # bot.chat(f'unable to get inventory: {e}')
        return False

def countInventoryItems(bot, name):
    try:
        count = 0
        items = bot.inventory.items()
        for item in items:
            if name in item['name']:
                count += item['count']

        try:
            if bot.heldItem.name:
                count += 1
        except Exception as e:
            pass

        if count == 0:
            return False, 0
        return True, count
    except Exception as e:
        # bot.chat(f'unable to get inventory: {e}')
        return False, 0

def equip(bot, item_name, destination='hand'):
    item_name = item_name.lower()
    item_name = findSimilarName(item_name)[0]
    if destination not in ['hand', "head", "torso", "legs", "feet", "off-hand"]:
        return f"invalid destination {destination}, should be one of ['hand', 'head', 'torso', 'legs', 'feet', 'off-hand']", False
    try:
        items = bot.inventory.items()
        equip_item = None
        for item in items:
            if item_name in item['name']:
                equip_item = item
                break
        if equip_item is None and (not bot.heldItem or bot.heldItem.name != item_name):
            # bot.chat(f'can not find {item_name}')
            return f"I don't have {item_name} in inventory", False
        bot.equip(equip_item, destination)
        # bot.chat('equipped')
        return f" equip {item_name}", True

    except Exception as e:
        # bot.chat(f'unable to equip: {e}')
        return f"unable to equip {item_name}", False


def unequip(bot, destination='hand'):
    assert destination in ['hand', "head", "torso", "legs", "feet", "off-hand"]

    try:
        bot.unequip(destination)
        # bot.chat('unequip')
        return f" unequip", True

    except Exception as e:
        # bot.chat(f'unable to unequip: {e}')
        return "unable to unequip", False


def mount(bot, name):
    try:
        entities = get_entity_by('name', get_envs_info(bot), name, bot.entity.username)
        entity = entities[0]
        bot.mount(entity)
        # bot.chat(f'#mounted {name}')
        return f" mount {name}", True
    except Exception as e:
        # bot.chat(f'unable to mount: {e}')
        return f"unable to mount {name}", False


def dismount(bot):
    try:
        bot.dismount()
        # bot.chat(f'#dismounted')
        return f" dismount", True
    except Exception as e:
        # bot.chat(f'unable to dismount: {e}')
        return f"unable to dismount", False


def toss(bot, mcData, item_name, amount=-1):  # need test
    if amount == -1:
        amount = 1
    try:
        items = getInventoryItemByName(bot, item_name, amount)
        if len(items) == 0:
            return f"I don't have {item_name}.", False
        # [DEBUG] 
        # print(items)
        bot.chat(f'toss {item_name} X {amount}')
        if items[0]["id"] is not None:
            bot.toss(items[0]['id'], None, amount)
        elif items[0]["type"] is not None:
            bot.toss(items[0]['type'], None, amount)
        else:
            bot.chat("minecraft version not supported maybe")
            return "minecraft version not supported maybe", False
        bot.chat('tossed')
        return f" tossed {item_name}", True
    except Exception as e:
        bot.chat(f'unable to toss: {e}')
        return f"unable to toss {item_name}", False


def useOnNearest(bot, Vec3, pathfinder, envs_info, mcData, item_name, name):
    msg, tag = equip(bot, item_name)
    # #[DEBUG] print(msg,tag)
    if not tag and (not bot.heldItem or bot.heldItem.name != item_name):
        return msg, tag
    try:
        entities = get_entity_by('name', envs_info, name, bot.entity.username)
        if len(entities) == 0:
            entity = bot.nearestEntity()
        else:
            entity = entities[0]
        bot.chat(f'#used {item_name} on {entity.name}')
        move_to(pathfinder=pathfinder, bot=bot, Vec3=Vec3, RANGE_GOAL=2, pos=entity["position"])
        bot.useOn(entity)
        bot.activateEntity(entity)
        
        pos = bot.entity.position
        bot.activateEntityAt(entity, pos)
        # bot.chat(f'activated entity {name}')
        bot.activateBlock(bot.blockAt(pos))
        # bot.chat(f'#used {item_name} on {name}')
        return f" use {item_name} on {name}", True
    except Exception as e:
        # bot.chat(f'unable to use: {e}')
        return f"unable to use {item_name}", tag
    
def interactItem(bot, item_name):
    try:
        bot.consume()
        return f" consume {item_name}", True
    except Exception as e:
        bot.chat(f'unable to consume: {e}')
        # return f"unable to consume {item_name}", False
    # try: # TODO
    #     bot.activateItem()
    #     return f" activate {item_name}", True
    # except Exception as e:
    #     # bot.chat(f'unable to activate: {e}')

    # bot.chat(f'unable to activate: {e}')
    return f"unable to activate {item_name}", False


def findSomething(bot, mcData, name, type='None'):
    ID = None
    if type == 'block':
        ID = mcData.blocksByName[name].id
        # bot.chat(f'#find {name} -- {ID}')
        return ID, f" find {name}"
    elif type == 'item':
        ID = mcData.itemsByName[name].id
        # bot.chat(f'#find {name} -- {ID}')
        return ID, f" find {name}"

    try:
        ID = mcData.itemsByName[name].id
        # bot.chat(f'#find {name} -- {ID}')
        return ID, " find {name}"
    except:
        ID = None, f"cannot find {name}"
    try:
        ID = mcData.blocksByName[name].id
        # bot.chat(f'#find {name} -- {ID}')
        return ID, " find {name}"
    except:
        ID = None, f"cannot find {name}"
    try:
        ID = mcData.entitiesByName[name].id
        # bot.chat(f'#find {name} -- {ID}')
        return ID, f" find {name}"
    except:
        ID = None
    try:
        ID = mcData.biomesByName[name].id
        # bot.chat(f'#find {name} -- {ID}')
        return ID, f" find {name}"
    except:
        ID = None
    try:
        ID = mcData.foodsByName[name].id
        # bot.chat(f'#find {name} -- {ID}')A
        return ID, f" find {name}"
    except:
        ID = None
    if ID is None:
        return None, f"cannot find {name}, try to get more infos or help"
    return ID, f" find {name}"

import Levenshtein

def findSimilarName(name):
    max_similar = 0
    similar_name = ""

    # 预处理输入名称，分割成子字符串
    name_parts = name.split('_')

    # 加载数据
    with open('data/mcData.json', 'r', encoding='utf-8') as f:
        mc_data_json = json.load(f)

    # 如果本身就是一个合法的名字，直接返回
    if is_entity_or_item(name) != 'error':
        return name, f"find {name}"
    
    # 遍历实体和物品
    for item in mc_data_json['entities'] + mc_data_json['items']:
        try:
            item_name = item[0]
            item_parts = item_name.split('_')

            # 计算所有子字符串的平均Levenshtein相似度
            total_similar = 0
            for part in name_parts:
                part_similar = max([1 - Levenshtein.distance(part, item_part) / max(len(part), len(item_part)) for item_part in item_parts])
                total_similar += part_similar

            avg_similar = total_similar / len(name_parts)

            if avg_similar > max_similar:
                max_similar = avg_similar
                similar_name = item_name
        except Exception as e:
            # 错误处理，这里简单忽略
            pass

    # 设置一个合理的相似度阈值
    if max_similar > 0.55:
        return similar_name, f"find {similar_name}"

    else:
        return "", f"cannot find {name} this is not a valid name, try to get more infos or help"



def read_mcData():
    import json
    entity_path = 'minecraft/mc_entities.txt'
    mc_entities = []
    with open(entity_path, 'r', encoding='utf-8') as f:
        mc_entities_raw = f.readlines()
    for item in mc_entities_raw:
        triple = item.strip().split()
        mc_entities.append([triple[1], triple[0]])
    item_path = 'minecraft/mc_items.txt'
    mc_items = []
    with open(item_path, 'r', encoding='utf-8') as f:
        mc_items_raw = f.readlines()
    for item in mc_items_raw:
        triple = item.strip().split()
        mc_items.append([triple[-2], triple[-3]])

    # save as json
    _mcData = {"entities": mc_entities, "items": mc_items}
    with open('../minecraft/mcData.json', 'w', encoding='utf-8') as f:
        json.dump(_mcData, f, ensure_ascii=False, indent=4)


 

def collect(bot, pathfinder, Vec3, mcData, block_name, distance=5, count=1):
    for _ in range(count):
        try:
            # blocks = findBlocks(bot,mcData,block_name,distance,count)
            block = bot.findBlock({
                "matching": findSomething(bot, mcData, block_name, 'block')[0],
                "maxDistance": distance
            })
            if block is None:
                return f"cannot find {block_name} nearby", False

            # bot.chat(f'collecting {block_name} ...')
            bot.collectBlock.collect(block)
            # bot.chat(f'collected {block_name} ...')
        except Exception as e:
            bot.chat(f'unable to collect {block_name}: {e}')
            return f"unable to collect {block_name}", False
    return f" collected {block_name}", True


def startFishing(bot, Vec3, envs_info, mcData):
    try:
        pos = find_nearest_(bot, Vec3, envs_info, mcData, 'fish')
        # [DEBUG] print(pos)
        # input()
        if pos == None:
            return "Here is no fish. Try another position", False
        bot.lookAt(pos)
        bot.equip(bot.registry.itemsByName.fishing_rod.id, 'hand')
    except Exception as e:
        # [DEBUG] print(e)
        return "I need to get fishing_rod first.", False

    try:
        bot.fish()
        return "I am fishing now", True
    except:
        return "failed fish", False


def stopFishing(bot):
    bot.activateItem()
    return "I stop fishing", True


def write(bot, Vec3, envs_info, mcData, block_name, text):
    if block_name == "book" or block_name == "writable_book":
        books = getInventoryItemByName(bot, 'writable_book')
        if len(books) == 0:
            return "I don't have a book to write", True
        try:
            book = books[0]
            pages = text.split('---')
            bot.writeBook(book.slot, pages)
            # /give @p written_book{pages:['{"text":"Minecraft Tools book"}'],title:BookName,author:"http://minecraft.tools/",display:{Lore:["this is the content"]}}
            # /give @p written_book{pages:['{"text":"Minecraft Tools book"}']}
            return f" write {text[:10]}... to book", True
        except Exception as e:
            # [DEBUG] print(e)
            return "write failed", True
    else:
        try:
            pos = find_nearest_(bot, Vec3, envs_info, mcData, block_name)
            block = bot.blockAt(pos)
            bot.updateSign(block, text.split(' ').slice(1).join(' '))
            return "write done", True
        except Exception as e:
            # [DEBUG] print(e)
            return "write failed", True


def read(bot, Vec3, envs_info, mcData, block_name, page=1, world_type="flatten"):
    if block_name == "book" or block_name == "writable_book":
        books = getInventoryItemByName(bot, 'writable_book')
        if len(books) == 0:
            return "I don't have a book to read", True
        try:
            book = books[0]
            if book.nbt == None:
                return "the book is empty", True
            return f"the {block_name} said {book.nbt.value.pages.value.value}", True
        except Exception as e:
            # [DEBUG] print(e)
            return "read failed", False
    else:
        try:
            pos = find_nearest_(bot, Vec3, envs_info, mcData, block_name)
            block = bot.blockAt(pos)
            text = block.getSignText()
            # [DEBUG] print(text)
            if text == "":
                return f"the {block_name} is empty", True
            return f"the {block_name} said {text}", True
        except Exception as e:
            # [DEBUG] print(e)
            return "read failed", False


if __name__ == '__main__':
    read_mcData()

import datetime
import json
import os
import random
import subprocess
import threading
import time
from functools import wraps
from typing import List

import requests


class MinecraftClient:
    '''
    Agent is the basic class for the agent in the Minecraft environment.
    Agent supports high-level and low-level functions for the agent to interact with the Minecraft environment.
    It works as a bridge between the Minecraft environment and the AI model.
    '''
    headers = {'Content-Type': 'application/json'}
    verbose = True

    name2port = {}
    agent_process = {}
    url_prefix = {}


    @staticmethod
    def get_url_prefix() -> dict:
        if os.path.exists("../data/url_prefix.json"):
            with open("../data/url_prefix.json", "r") as f:
                url_prefix = json.load(f)
        else:
            url_prefix = {}
        return url_prefix

    def __init__(self, name, local_port=5000):
        self.name = name
        self.local_port = local_port
        self.basic_tools = [
            MinecraftClient.scanNearbyEntities, MinecraftClient.navigateTo, MinecraftClient.attackTarget,
            MinecraftClient.UseItemOnEntity, MinecraftClient.sleep, MinecraftClient.wake,
            MinecraftClient.MineBlock, MinecraftClient.placeBlock, MinecraftClient.equipItem,
            MinecraftClient.handoverBlock, MinecraftClient.SmeltingCooking,
            MinecraftClient.withdrawItem, MinecraftClient.storeItem, MinecraftClient.craftBlock,
            MinecraftClient.enchantItem, MinecraftClient.trade, MinecraftClient.repairItem, MinecraftClient.eat,
            MinecraftClient.fetchContainerContents, MinecraftClient.toggleAction
        ]
        self.all_tools = [
            MinecraftClient.scanNearbyEntities, MinecraftClient.navigateTo, MinecraftClient.attackTarget,
            MinecraftClient.navigateToBuilding, MinecraftClient.navigateToAnimal, MinecraftClient.navigateToPlayer,
            MinecraftClient.UseItemOnEntity, MinecraftClient.sleep, MinecraftClient.wake,
            MinecraftClient.MineBlock, MinecraftClient.placeBlock, MinecraftClient.equipItem,
            MinecraftClient.tossItem, MinecraftClient.talkTo, MinecraftClient.handoverBlock,
            MinecraftClient.withdrawItem, MinecraftClient.storeItem, MinecraftClient.craftBlock,
            MinecraftClient.SmeltingCooking, MinecraftClient.erectDirtLadder, MinecraftClient.dismantleDirtLadder,
            MinecraftClient.enchantItem, MinecraftClient.trade, MinecraftClient.repairItem, MinecraftClient.eat,
            MinecraftClient.drink, MinecraftClient.wear, MinecraftClient.layDirtBeam, MinecraftClient.removeDirtBeam,
            MinecraftClient.openContainer, MinecraftClient.closeContainer,
            MinecraftClient.fetchContainerContents, MinecraftClient.toggleAction,
            MinecraftClient.get_entity_info, MinecraftClient.get_environment_info, 
            MinecraftClient.performMovement, MinecraftClient.lookAt, MinecraftClient.startFishing,
            MinecraftClient.stopFishing, MinecraftClient.read, MinecraftClient.readPage, MinecraftClient.write,
            MinecraftClient.mountEntity, MinecraftClient.dismountEntity, MinecraftClient.rideEntity, MinecraftClient.disrideEntity,
        ]

        if name == "nobody":
            return
        url_prefix = MinecraftClient.get_url_prefix()
        url_prefix[name] = f"http://localhost:{local_port}"
        with open("../data/url_prefix.json", "w") as f:
            json.dump(url_prefix, f)

        MinecraftClient.name2port[name] = local_port

    def render(self, structure_idx, center_pos):
        url = MinecraftClient.get_url_prefix()[self.name] + "/post_render"
        data = {
            "id": structure_idx,
            "center_pos": center_pos,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    def env(self):
        """Get the Environment Information"""
        url = MinecraftClient.get_url_prefix()[self.name] + "/post_environment"
        response = requests.post(url, headers=MinecraftClient.headers)
        return str(response.json())

    @staticmethod
    def launch(host="localhost", port=25565, world="world", verbose=False, ignore_name=[], debug=False):
        MinecraftClient.port = port
        if verbose:
            print("launch ...")
        for key, value in MinecraftClient.name2port.items():
            if key in ignore_name:
                continue
            MinecraftClient.agent_process[key] = subprocess.Popen(
                ["python", "environments/minecraft_utils/minecraft_server.py", "-H", host, "-P", str(port), "-LP", str(value), "-U", key, "-W",
                world, "-D", str(debug)], shell=False)
            print(f"python environments/minecraft_utils/minecraft_server.py -H \"{host}\" -P {port} -LP {value} -U \"{key}\" -W \"{world}\" -D {debug}")
            time.sleep(3)
        if verbose:
            print("launch done.")

    @staticmethod
    def kill():
        for value in MinecraftClient.agent_process.values():
            value.terminate()

    @staticmethod
    def getMsg(player_name: str):
        """Get the Message from the Server"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_msg"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def erectDirtLadder(player_name: str, top_x: int, top_y: int, top_z: int):
        """Helpful to place item at higher place Erect a Dirt Ladder Structure at Specific Position x y z, remember to dismantle it after use"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_erect"
        data = {
            "top_x": top_x,
            "top_y": top_y,
            "top_z": top_z,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()
    
    @staticmethod
    def dismantleDirtLadder(player_name: str, top_x: int, top_y: int, top_z: int):
        """Dismantle a Dirt Ladder Structure from ground to top at Specific Position x y z"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_dismantle"
        data = {
            "top_x": top_x,
            "top_y": top_y,
            "top_z": top_z,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def layDirtBeam(player_name: str, x_1: int, y_1: int, z_1: int, x_2: int, y_2: int, z_2: int):
        """Lay a Dirt Beam from Position x1 y1 z1 to Position x2 y2 z2"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_lay"
        data = {
            "x_1": x_1,
            "y_1": y_1,
            "z_1": z_1,
            "x_2": x_2,
            "y_2": y_2,
            "z_2": z_2,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()
    
    @staticmethod
    def removeDirtBeam(player_name: str, x_1: int, y_1: int, z_1: int, x_2: int, y_2: int, z_2: int):
        """Remove a Dirt Beam from Position x1 y1 z1 to Position x2 y2 z2"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_remove"
        data = {
            "x_1": x_1,
            "y_1": y_1,
            "z_1": z_1,
            "x_2": x_2,
            "y_2": y_2,
            "z_2": z_2,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()


    @staticmethod
    def scanNearbyEntities(player_name: str, item_name: str, radius: int = 10, item_num: int = -1):
        """Find minecraft item blocks creatures in a radius, return ('message': msg, 'status': True/False, 'data':[('x':x,'y':y,'z':z),...]) This function can not find items in the chest, container,or player's inventory."""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_find"
        data = {
            "name": item_name.lower().replace(" ", "_"),
            "distance": radius,
            "count": item_num,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def handoverBlock(player_name: str, target_player_name: str, item_name: str, item_count: int):
        """Hand Item to a target player you work with, return ('message': msg, 'status': True/False), item num will be automatically checked and player will automatically move to the target player"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_hand"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "from_name": player_name, 
            "target_name": target_player_name,
            "item_count": item_count,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def navigateToPlayer(player_name: str, target_name: str):
        """Move to a target Player,return ('message': msg, 'status': True/False)"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_move_to"
        data = {
            "name": target_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def navigateToBuilding(player_name: str, building_name: str):
        """Move to a building by name, return string result"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_move_to"
        data = {
            "name": building_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def navigateToAnimal(player_name: str, animal_name: str):
        """Move to an animal by name, return string result"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_move_to"
        data = {
            "name": animal_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def navigateTo(player_name: str, x: int, y: int, z: int):
        """Move to a Specific Position x y z, return string result"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_move_to_pos"
        data = {
            "x": x,
            "y": y,
            "z": z,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def UseItemOnEntity(player_name: str, item_name: str, entity_name: str):
        """Use a Specific Item on a Specific Entity, return string result"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_use_on"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "entity_name": entity_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def sleep(player_name: str):
        """Go to Sleep"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_sleep"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def wake(player_name: str):
        """Wake Up"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_wake"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def MineBlock(player_name: str, x: int, y: int, z: int):
        """Dig Block at Specific Position x y z"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_dig"
        data = {
            "x": x,
            "y": y,
            "z": z,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def placeBlock(player_name: str, item_name: str, x: int, y: int, z: int, facing: str):
        """Place a Specific Item at Specific Position x y z with Specific facing in one of [W, E, S, N, x, y, z, A] default is 'A'., return ('message': msg, 'status': True/False)"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_place"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "x": x,
            "y": y,
            "z": z,
            "facing": facing,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def attackTarget(player_name: str, target_name: str):
        """Attack the Nearest Entity with a Specific Name"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_attack"
        data = {
            "name": target_name.lower().replace(" ", "_"),
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def equipItem(player_name: str, slot: str, item_name: str):
        """Equip a Specific Item on a Specific Slot | to equip item on hand,head,torso,legs,feet,off-hand."""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_equip"
        data = {
            "slot": slot,
            "item_name": item_name.lower().replace(" ", "_"),
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def tossItem(player_name: str, item_name: str, count: int = 1):
        """Throw a Specific Item Out with a Specific Count"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_toss"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "count": count,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def get_environment_info(player_name: str):
        """Get the Environment Information, return string contains time of day, weather"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_environment"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()
    
    @staticmethod
    def get_environment_dict_info(player_name: str):
        """Get the Environment Information, return string contains time of day, weather"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_environment_dict"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def get_entity_info(player_name: str, target_name: str = ""):
        """Get the Entity Information, return string contains entity name, entity pos x y z, entity held item"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_entity"
        data = {
            "name": target_name.lower().replace(" ", "_"),
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def withdrawItem(player_name: str, item_name: str, from_name: str, item_count: int):
        """Take out Item from nearest 'chest' | 'container' | 'furnace' return string result"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_get"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "from_name": from_name.lower().replace(" ", "_"),
            "item_count": item_count,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def storeItem(player_name: str, item_name: str, to_name: str, item_count: int):
        """Put in Item to One Chest, Container, etc, return string result"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_put"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "to_name": to_name.lower().replace(" ", "_"),
            "item_count": item_count,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def SmeltingCooking(player_name: str, item_name: str, item_count: int, fuel_item_name: str):
        """Smelt or Cook Item in the Furnace"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_smelt"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "item_count": item_count,
            "fuel_item_name": fuel_item_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def craftBlock(player_name: str, item_name: str, count: int):
        """Craft Item in the Crafting Table"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_craft"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "count": count,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def enchantItem(player_name: str, item_name: str, count: int):
        """Enchant Item in the Enchanting Table"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_enchant"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "count": count,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def trade(player_name: str, item_name: str, with_name: str, count: int):
        """Trade Item with the villager npc, return the details of trade items and num."""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_trade"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "with_name": with_name,
            "count": count,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def repairItem(player_name: str, item_name: str, material: str):
        """Repair Item in the Anvil"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_repair"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "material": material.lower().replace(" ", "_"),
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def eat(player_name: str, item_name: str):
        """Eat Item"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_eat"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def drink(player_name: str, item_name: str, count: int):
        """Drink Item"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_drink"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "count": count,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def wear(player_name: str, slot: str, item_name: str):
        """Wear Item on Specific Slot"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_wear"
        data = {
            "slot": slot,
            "item_name": item_name.lower().replace(" ", "_"),
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def openContainer(player_name: str, container_name: str, position: List[int] = [0, 0, 0]):
        """Open the nearest but might not the correct 'chest' | 'container' | 'furnace' position is optional, return ('message': msg, 'status': True/False, 'data':[('name':name, 'count':count),...])"""
        if position != [0, 0, 0]:
            response = MinecraftClient.navigateTo(player_name, position[0], position[1], position[2])
            if response["status"] == False:
                return response
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_open"
        data = {
            "item_name": container_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def fetchContainerContents(player_name: str, item_name: str, position: List[int] = [0, 0, 0]):
        """Get the details of item_name 'chest' | 'container' | 'furnace' position is optional, return ('message': msg, 'status': True/False, 'data':[('name':name, 'count':count),...])"""
        if item_name not in ["chest", "inventory", "furnace", "container"]:
            return {'data': [], 'message': 'Failed item name not in ["chest", "inventory", "furnace", "container"]', 'status': False}
        if position != [0, 0, 0]:
            response = MinecraftClient.navigateTo(player_name, position[0], position[1], position[2])
            if response["status"] == False:
                return response
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_open"
        data = {
            "item_name": item_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def closeContainer(player_name: str, item_name: str, position: List[int] = [0, 0, 0]):
        """Close 'chest' | 'container' | 'furnace' position is optional."""
        if position != [0, 0, 0]:
            response = MinecraftClient.navigateTo(player_name, position[0], position[1], position[2])
            if response["status"] == False:
                return response
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_close"
        data = {
            "item_name": item_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def toggleAction(player_name: str, item_name: str, x: int, y: int, z: int):
        """open/close Gate, Lever, Press Button (pressure_plate need to stand on it, iron door need to be powered, they are not included), at Specific Position x y z"""
        if "plate" in item_name:
            return {'message': "pressure_plate need to stand on it", 'status': False}
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_activate"
        data = {
            "item_name": item_name.lower().replace(" ", "_"),
            "x": x,
            "y": y,
            "z": z,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def mountEntity(player_name: str, entity_name: str):
        """Mount the Entity"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_mount"
        data = {
            "entity_name": entity_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def dismountEntity(player_name: str):
        """Dismount the Entity"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_dismount"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def rideEntity(player_name: str, entity_name: str):
        """Ride the Entity"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_ride"
        data = {
            "entity_name": entity_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def disrideEntity(player_name: str):
        """Disride the Entity"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_disride"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def talkTo(player_name: str, entity_name: str, message: str):
        """Talk to the Entity"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_talk_to"
        data = {
            "entity_name": entity_name,
            "message": message,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def performMovement(player_name: str, action_name: str, seconds: int):
        """Perform Action jump forward back left right for Seconds"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_action"
        data = {
            "action_name": action_name,
            "seconds": seconds,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def lookAt(player_name: str, name: str):
        """Look at Someone or Something"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_look_at"
        data = {
            "name": name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def startFishing(player_name: str):
        """Start Fishing"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_start_fishing"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def stopFishing(player_name: str):
        """Stop Fishing"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_stop_fishing"
        response = requests.post(url, headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def read(player_name: str, item_name: str):
        """Read Book or Sign neaby, return string details"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_read"
        data = {
            "name": item_name,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def readPage(player_name: str, item_name: str, page: int):
        """Read Content from Book Page"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_read_page"
        data = {
            "name": item_name,
            "page": page,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    @staticmethod
    def write(player_name: str, item_name: str, content: str):
        """Write Content on Writable Book or Sign"""
        url = MinecraftClient.get_url_prefix()[player_name] + "/post_write"
        data = {
            "name": item_name,
            "content": content,
        }
        response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
        return response.json()

    def chat(self, msg, async_tag=False):
        url = MinecraftClient.get_url_prefix()[self.name] + "/post_chat"
        data = {
            "msg": msg,
        }
        if async_tag:
            threading.Thread(target=requests.post, args=(url,),
                             kwargs={"data": json.dumps(data), "headers": MinecraftClient.headers}).start()
            return {}
        else:
            time.sleep(.05)
            response = requests.post(url, data=json.dumps(data), headers=MinecraftClient.headers)
            return response.json()


if __name__ == "__main__":
    client = MinecraftClient(name="player1")
    MinecraftClient.launch()
    print(MinecraftClient.get_entity_info("player1"))
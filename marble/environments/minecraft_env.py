"""
MineCraft environment module.
"""

import os
import subprocess
import time
from typing import Any, Callable, Dict, List, Union

from marble.environments.base_env import BaseEnvironment
from marble.environments.minecraft_utils.minecraft_client import MinecraftClient
from marble.environments.minecraft_utils.minecraft_tool_description import *
from marble.utils.logger import get_logger


class MinecraftEnvironment(BaseEnvironment):
    def __init__(self, name: str, config: Dict[str, Any] = dict()):
        """
        Initialize the environment.

        Args:
            name (str): The name of the environment.
            config (Dict[str, Any]): Configuration for the environment.
        """
        super().__init__(name, config)
        # Minecraft client configuration
        self.host: str = config.get("host", "localhost")
        self.port: int = config.get("port", 25565)
        self.clients: Dict[str, MinecraftClient] = dict()
        self.judge: Union[subprocess.Popen, None] = None
        self.task_id: int = config.get("task_id", 0)
        self.task_name: str = config.get("task_name", "test")
        self.logger = get_logger(self.__class__.__name__)

        # Register tons of actions.
        self.register_action("scanNearbyEntities", handler=self._scanNearbyEntities_handler, description=scanNearbyEntities_description)
        self.register_action("navigateTo", handler=self._navigateTo_handler, description=navigateTo_description)
        # self.register_action("attackTarget", handler=self._attackTarget_handler, description=attackTarget_description)
        # self.register_action("navigateToBuilding", handler=self._navigateToBuilding_handler, description=navigateToBuilding_description)
        # self.register_action("navigateToAnimal", handler=self._navigateToAnimal_handler, description=navigateToAnimal_description)
        # self.register_action("navigateToPlayer", handler=self._navigateToPlayer_handler, description=navigateToPlayer_description)
        # self.register_action("UseItemOnEntity", handler=self._UseItemOnEntity_handler, description=UseItemOnEntity_description)
        # self.register_action("sleep", handler=self._sleep_handler, description=sleep_description)
        # self.register_action("wake", handler=self._wake_handler, description=wake_description)
        self.register_action("MineBlock", handler=self._MineBlock_handler, description=MineBlock_description)
        self.register_action("placeBlock", handler=self._placeBlock_handler, description=placeBlock_description)
        self.register_action("equipItem", handler=self._equipItem_handler, description=equipItem_description)
        # self.register_action("tossItem", handler=self._tossItem_handler, description=tossItem_description)
        # self.register_action("talkTo", handler=self._talkTo_handler, description=talkTo_description)
        self.register_action("handoverBlock", handler=self._handoverBlock_handler, description=handoverBlock_description)
        self.register_action("withdrawItem", handler=self._withdrawItem_handler, description=withdrawItem_description)
        # self.register_action("storeItem", handler=self._storeItem_handler, description=storeItem_description)
        # self.register_action("craftBlock", handler=self._craftBlock_handler, description=craftBlock_description)
        # self.register_action("SmeltingCooking", handler=self._SmeltingCooking_handler, description=SmeltingCooking_description)
        self.register_action("erectDirtLadder", handler=self._erectDirtLadder_handler, description=erectDirtLadder_description)
        self.register_action("dismantleDirtLadder", handler=self._dismantleDirtLadder_handler, description=dismantleDirtLadder_description)
        # self.register_action("enchantItem", handler=self._enchantItem_handler, description=enchantItem_description)
        # self.register_action("trade", handler=self._trade_handler, description=trade_description)
        # self.register_action("repairItem", handler=self._repairItem_handler, description=repairItem_description)
        # self.register_action("eat", handler=self._eat_handler, description=eat_description)
        # self.register_action("drink", handler=self._drink_handler, description=drink_description)
        # self.register_action("wear", handler=self._wear_handler, description=wear_description)
        # self.register_action("layDirtBeam", handler=self._layDirtBeam_handler, description=layDirtBeam_description)
        # self.register_action("removeDirtBeam", handler=self._removeDirtBeam_handler, description=removeDirtBeam_description)
        # self.register_action("openContainer", handler=self._openContainer_handler, description=openContainer_description)
        # self.register_action("closeContainer", handler=self._closeContainer_handler, description=closeContainer_description)
        self.register_action("fetchContainerContents", handler=self._fetchContainerContents_handler, description=fetchContainerContents_description)
        # self.register_action("toggleAction", handler=self._toggleAction_handler, description=toggleAction_description)
        # self.register_action("get_entity_info", handler=self._get_entity_info_handler, description=get_entity_info_description)
        self.register_action("get_environment_info", handler=self._get_environment_info_handler, description=get_environment_info_description)
        # self.register_action("performMovement", handler=self._performMovement_handler, description=performMovement_description)
        # self.register_action("lookAt", handler=self._lookAt_handler, description=lookAt_description)
        # self.register_action("startFishing", handler=self._startFishing_handler, description=startFishing_description)
        # self.register_action("stopFishing", handler=self._stopFishing_handler, description=stopFishing_description)
        # self.register_action("read", handler=self._read_handler, description=read_description)
        # self.register_action("readPage", handler=self._readPage_handler, description=readPage_description)
        # self.register_action("write", handler=self._write_handler, description=write_description)

    def register_agent(self, name: str, local_port: int):
        self.agents.append(name)
        self.clients[name] = MinecraftClient(name=name, local_port=local_port)
        self.logger.info(f"Agent {name} registered.")

    def launch(self):
        MinecraftClient.launch(host=self.host, port=self.port)
        self.logger.info(f"Minecraft environment launched.")
        self.judge = subprocess.Popen(["python", "environments/minecraft_utils/build_judger.py", "--idx", str(self.task_id), "--host", self.host, "--port" , str(self.port), "--agent_num", str(len(self.agents)), "--agent_names", ",".join(self.agents), "--task_name", self.task_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # print(f"""python environments/minecraft_utils/build_judger.py --idx {self.task_id} --host \"{self.host}\" --port {self.port} --agent_num {len(self.agents)} --agent_names \"{",".join(self.agents)}\" --task_name \"{self.task_name}\"""")
        self.logger.debug(f"Current working directory: {os.getcwd()}")
        self.logger.debug(f"""python environments/minecraft_utils/build_judger.py --idx {self.task_id} --host \"{self.host}\" --port {self.port} --agent_num {len(self.agents)} --agent_names \"{",".join(self.agents)}\" --task_name \"{self.task_name}\"""")
        time.sleep(40)

    def finish(self):
        MinecraftClient.kill()
        self.judge.terminate()

    def _scanNearbyEntities_handler(self, player_name: str, item_name: str, radius: int = 10, item_num: int = -1):
        return MinecraftClient.scanNearbyEntities(player_name, item_name, radius, item_num)
    
    def _navigateTo_handler(self, player_name: str, x: int, y: int, z: int):
        return MinecraftClient.navigateTo(player_name, x, y, z)
    
    def _attackTarget_handler(self, player_name: str, target_name: str):
        return MinecraftClient.attackTarget(player_name, target_name)
    
    def _navigateToBuilding_handler(self, player_name: str, building_name: str):
        return MinecraftClient.navigateToBuilding(player_name, building_name)
    
    def _navigateToAnimal_handler(self, player_name: str, animal_name: str):
        return MinecraftClient.navigateToAnimal(player_name, animal_name)
    
    def _navigateToPlayer_handler(self, player_name: str, target_name: str):
        return MinecraftClient.navigateToPlayer(player_name, target_name)
    
    def _UseItemOnEntity_handler(self, player_name: str, item_name: str, entity_name: str):
        return MinecraftClient.UseItemOnEntity(player_name, item_name, entity_name)
    
    def _sleep_handler(self, player_name: str):
        return MinecraftClient.sleep(player_name)
    
    def _wake_handler(self, player_name: str):
        return MinecraftClient.wake(player_name)
    
    def _MineBlock_handler(self, player_name: str, x: int, y: int, z: int):
        return MinecraftClient.MineBlock(player_name, x, y, z)
    
    def _placeBlock_handler(self, player_name: str, item_name: str, x: int, y: int, z: int, facing: str):
        return MinecraftClient.placeBlock(player_name, item_name, x, y, z, facing)
    
    def _equipItem_handler(self, player_name: str, slot: str, item_name: str):
        return MinecraftClient.equipItem(player_name, slot, item_name)
    
    def _tossItem_handler(self, player_name: str, item_name: str, count: int = 1):
        return MinecraftClient.tossItem(player_name, item_name, count)
    
    def _talkTo_handler(self, player_name: str, entity_name: str, message: str):
        return MinecraftClient.talkTo(player_name, entity_name, message)
    
    def _handoverBlock_handler(self, player_name: str, target_player_name: str, item_name: str, item_count: int):
        return MinecraftClient.handoverBlock(player_name, target_player_name, item_name, item_count)
    
    def _withdrawItem_handler(self, player_name: str, item_name: str, from_name: str, item_count: int):
        return MinecraftClient.withdrawItem(player_name, item_name, from_name, item_count)
    
    def _storeItem_handler(self, player_name: str, item_name: str, to_name: str, item_count: int):
        return MinecraftClient.storeItem(player_name, item_name, to_name, item_count)
    
    def _craftBlock_handler(self, player_name: str, item_name: str, count: int):
        return MinecraftClient.craftBlock(player_name, item_name, count)
    
    def _SmeltingCooking_handler(self, player_name: str, item_name: str, item_count: int, fuel_item_name: str):
        return MinecraftClient.SmeltingCooking(player_name, item_name, item_count, fuel_item_name)
    
    def _erectDirtLadder_handler(self, player_name: str, top_x: int, top_y: int, top_z: int):
        return MinecraftClient.erectDirtLadder(player_name, top_x, top_y, top_z)
    
    def _dismantleDirtLadder_handler(self, player_name: str, top_x: int, top_y: int, top_z: int):
        return MinecraftClient.dismantleDirtLadder(player_name, top_x, top_y, top_z)
    
    def _enchantItem_handler(self, player_name: str, item_name: str, count: int):
        return MinecraftClient.enchantItem(player_name, item_name, count)
    
    def _trade_handler(self, player_name: str, item_name: str, with_name: str, count: int):
        return MinecraftClient.trade(player_name, item_name, with_name, count)
    
    def _repairItem_handler(self, player_name: str, item_name: str, material: str):
        return MinecraftClient.repairItem(player_name, item_name, material)
    
    def _eat_handler(self, player_name: str, item_name: str):
        return MinecraftClient.eat(player_name, item_name)
    
    def _drink_handler(self, player_name: str, item_name: str, count: int):
        return MinecraftClient.drink(player_name, item_name, count)
    
    def _wear_handler(self, player_name: str, slot: str, item_name: str):
        return MinecraftClient.wear(player_name, slot, item_name)
    
    def _layDirtBeam_handler(self, player_name: str, x_1: int, y_1: int, z_1: int, x_2: int, y_2: int, z_2: int):
        return MinecraftClient.layDirtBeam(player_name, x_1, y_1, z_1, x_2, y_2, z_2)
    
    def _removeDirtBeam_handler(self, player_name: str, x_1: int, y_1: int, z_1: int, x_2: int, y_2: int, z_2: int):
        return MinecraftClient.removeDirtBeam(player_name, x_1, y_1, z_1, x_2, y_2, z_2)
    
    def _openContainer_handler(self, player_name: str, container_name: str, position: List[int] = [0, 0, 0]):
        return MinecraftClient.openContainer(player_name, container_name, position)
    
    def _closeContainer_handler(self, player_name: str, item_name: str, position: List[int] = [0, 0, 0]):
        return MinecraftClient.closeContainer(player_name, item_name, position)
    
    def _fetchContainerContents_handler(self, player_name: str, item_name: str, position: List[int] = [0, 0, 0]):
        return MinecraftClient.fetchContainerContents(player_name, item_name, position)
    
    def _toggleAction_handler(self, player_name: str, item_name: str, x: int, y: int, z: int):
        return MinecraftClient.toggleAction(player_name, item_name, x, y, z)
    
    def _get_entity_info_handler(self, player_name: str, target_name: str = ""):
        return MinecraftClient.get_entity_info(player_name, target_name)

    def _get_environment_info_handler(self, player_name: str):
        return MinecraftClient.get_environment_info(player_name)
    
    def _performMovement_handler(self, player_name, action_name, seconds):
        return MinecraftClient.performMovement(player_name, action_name, seconds)
    
    def _lookAt_handler(self, player_name: str, name: str):
        return MinecraftClient.lookAt(player_name, name)
    
    def _startFishing_handler(self, player_name: str):
        return MinecraftClient.startFishing(player_name)
    
    def _stopFishing_handler(self, player_name: str):
        return MinecraftClient.stopFishing(player_name)
    
    def _read_handler(self, player_name: str, item_name: str):
        return MinecraftClient.read(player_name, item_name)
    
    def _readPage_handler(self, player_name: str, item_name: str, page: int):
        return MinecraftClient.readPage(player_name, item_name, page)
    
    def _write_handler(self, player_name: str, item_name: str, content: str):
        return MinecraftClient.write(player_name, item_name, content)

    def apply_action(self, agent_id: Union[str, None], action_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an action in the environment.

        Args:
            agent_id (str): The ID of the agent performing the action.
            action_name (str): The action to execute. Action name is used to retrieve the handler.
            arguments (dict): Arguments for the action handler.
        """
        # Execution
        arguments["player_name"] = agent_id
        action_result = self._action_handlers[action_name](**arguments)

        # Update the state with the action result
        self.state['last_action_result'] = action_result

        # Increment iteration count
        self.current_iteration += 1
        if self.current_iteration >= self.max_iterations:
            self.done = True

        return action_result

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current environment state.

        Returns:
            Dict[str, Any]: The current environment state.
        """
        return MinecraftClient.get_environment_dict_info(self.agents[0])

if __name__ == "__main__":
    agent_id = "player1"
    agent_port = 5000
    mcenv = MinecraftEnvironment("minecraft")
    mcenv.register_agent(agent_id, agent_port)
    mcenv.launch()
    while True:
        command = input("Action:\n").strip()
        args = command.split(" ")
        action = args[0]
        arg_name, arg_value = None, None
        arg_dict = dict()
        for i in range(1, len(args)):
            if i % 2 == 1:
                arg_name = args[i]
            else:
                arg_value = args[i]
            if arg_name and arg_value:
                try:
                    arg_value = eval(arg_value)
                except:
                    pass
                arg_dict[arg_name] = arg_value
                arg_name, arg_value = None, None
        print(f"Log:\nAction: {action}, Args: {arg_dict}")
        try:
            ret = mcenv.apply_action(agent_id, action, arg_dict)
            print(f"Result:\n{ret}")
        except Exception as e:
            print(f"Error:\n{e}")
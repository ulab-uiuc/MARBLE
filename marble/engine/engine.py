"""
The core engine module that coordinates agents within the environment.
"""

from typing import List, Dict, Any, Union

from marble.agents.base_agent import BaseAgent
from marble.configs.config import Config
from marble.environments import BaseEnvironment, WebEnvironment
from marble.graphs.agent_graph import AgentGraph
from marble.metrics.evaluation import Evaluation
from marble.utils.logger import get_logger
from marble.memory.base_memory import BaseMemory
from marble.memory.shared_memory import SharedMemory

EnvType = Union[BaseEnvironment, WebEnvironment]

class Engine:
    """
    The Engine class orchestrates the simulation, coordinating agents and the environment.
    """

    def __init__(self, config: Config):
        """
        Initialize the Engine with the given configuration.

        Args:
            config (Config): Configuration parameters.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.config = config
        self.environment = self._initialize_environment(config.environment)
        self.agents = self._initialize_agents(config.agents)
        self.graph = AgentGraph(self.agents, config.graph)
        self.evaluator = Evaluation(metrics=config.metrics)
        self.memory = self._initialize_memory(config.memory)
        self.logger.info("Engine initialized.")

    def _initialize_environment(self, env_config: Dict[str, Any]) -> EnvType:
        """
        Initialize the environment.

        Args:
            env_config (dict): Environment configuration.

        Returns:
            BaseEnvironment: An instance of the environment.

        Raises:
            ValueError: If the environment type is not supported.
        """
        env_type = env_config.get("type")
        if env_type == "Web":
            environment = WebEnvironment(name="Web Environment", config=env_config)
        # elif env_type == "Minecraft":
        #     from environments.minecraft_env import MinecraftEnv
        #     environment = MinecraftEnv(config=env_config)
        # elif env_type == "ResearchTown":
        #     from environments.research_town_env import ResearchTownEnv
        #     environment = ResearchTownEnv(config=env_config)
        else:
            raise ValueError(f"Unsupported environment type: {env_type}")
        self.logger.debug(f"Environment '{env_type}' initialized.")
        return environment

    def _initialize_agents(self, agent_configs: List[Dict[str, Any]]) -> List[BaseAgent]:
        """
        Initialize agents based on configurations.

        Args:
            agent_configs (List[dict]): List of agent configurations.

        Returns:
            List[BaseAgent]: List of agent instances.
        """
        agents = []
        for agent_config in agent_configs:
            agent_type = agent_config.get("type")
            if agent_type == "ReasoningAgent":
                from agents.reasoning_agent import ReasoningAgent
                agent = ReasoningAgent(config=agent_config)
            else:
                raise ValueError(f"Unsupported agent type: {agent_type}")
            agents.append(agent)
            self.logger.debug(f"Agent '{agent.agent_id}' of type '{agent_type}' initialized.")
        return agents

    def _initialize_memory(self, memory_config: Dict[str, Any]) -> Union[SharedMemory, BaseMemory]:
        """
        Initialize the shared memory mechanism.

        Args:
            memory_config (dict): Memory configuration.

        Returns:
            BaseMemory: An instance of the memory module.
        """
        memory_type = memory_config.get("type", "SharedMemory")
        memory: Union[BaseMemory, SharedMemory, None] = None
        if memory_type == "SharedMemory":
            memory = SharedMemory()
        else:
            memory = BaseMemory()
        self.logger.debug(f"Memory of type '{memory_type}' initialized.")
        return memory

    def start(self) -> None:
        """
        Start the engine to run the simulation.
        """
        self.logger.info("Engine starting simulation.")
        try:
            execution_order = self.graph.traverse()
            while not self.environment.is_done():
                for agent in execution_order:
                    # Agents may need to share information; use shared memory if applicable
                    perception = agent.perceive(self.environment.get_state())
                    action = agent.act(perception)
                    self.environment.apply_action(agent.agent_id, action)
                self.evaluator.update(self.environment, self.agents)
        except Exception:
            self.logger.exception("An error occurred during simulation.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Simulation completed.")

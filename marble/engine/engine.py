"""
The core engine module that coordinates agents within the environment.
"""

import asyncio
from typing import Any, Dict, List, Union

from marble.agent import BaseAgent, ReasoningAgent
from marble.configs.config import Config
from marble.environments import BaseEnvironment, WebEnvironment
from marble.swarm.swarm_graph import SwarmGraph  # Updated import
from marble.memory.base_memory import BaseMemory
from marble.memory.shared_memory import SharedMemory
from marble.evaluator.evaluator import Evaluator
from marble.utils.logger import get_logger

EnvType = Union[BaseEnvironment, WebEnvironment]
AgentType = Union[BaseAgent, ReasoningAgent]

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
        self.swarm_graph = SwarmGraph(self.agents, config.graph)  # Use SwarmGraph
        self.evaluator = Evaluator(metrics_config=config.metrics)
        self.memory = self._initialize_memory(config.memory)
        self.max_iterations = config.simulation.get('max_iterations', 10)
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
            loop = asyncio.get_event_loop()
            iteration = 0
            while not self.environment.is_done():
                iteration += 1
                self.logger.info(f"Starting iteration {iteration}")
                # Run the swarm graph
                inputs = self.environment.get_state()
                outputs = loop.run_until_complete(self.swarm_graph.run(inputs))
                # Process outputs
                for output in outputs:
                    self.environment.apply_action(None, output)
                self.evaluator.update(self.environment, self.agents)
                # Check termination conditions
                if self.environment.is_task_completed():
                    self.logger.info("Task has been completed successfully.")
                    break
                if iteration >= self.max_iterations:
                    self.logger.info("Maximum iterations reached.")
                    break
            else:
                self.logger.info("Environment signaled done.")
        except Exception:
            self.logger.exception("An error occurred during simulation.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Simulation completed.")

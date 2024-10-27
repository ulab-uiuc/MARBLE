# marble/engine/engine.py

"""
The core engine module that coordinates agents within the environment.
"""
import os
from typing import Any, Dict, List, Union

from marble.agent import BaseAgent
from marble.configs.config import Config
from marble.engine.engine_planner import EnginePlanner
from marble.environments import BaseEnvironment, WebEnvironment, WerewolfEnv
from marble.evaluator.evaluator import Evaluator
from marble.graph.agent_graph import AgentGraph
from marble.memory.base_memory import BaseMemory
from marble.memory.shared_memory import SharedMemory
from marble.utils.logger import get_logger

EnvType = Union[BaseEnvironment, WebEnvironment]
AgentType = Union[BaseAgent]

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

        # Initialize Environment if it exists in config
        if hasattr(config, 'environment'):
            self.environment = self._initialize_environment(config.environment)
        else:
            self.environment = None

        # Initialize Agents if it exists in config
        if hasattr(config, 'agents'):
            self.agents = self._initialize_agents(config.agents)
        else:
            self.agents = []

        # Initialize AgentGraph if it exists in config
        if hasattr(config, 'graph'):
            self.graph = AgentGraph(self.agents, config.graph)
        else:
            self.graph = None

        # Initialize Memory if it exists in config
        if hasattr(config, 'memory'):
            self.memory = self._initialize_memory(config.memory)
        else:
            self.memory = None

        # Initialize Evaluator if metrics are defined in config
        if hasattr(config, 'metrics'):
            self.evaluator = Evaluator(metrics_config=config.metrics)
        else:
            self.evaluator = None

        # Get task content if it exists in config
        self.task = config.task.get('content', '') if hasattr(config, 'task') else ''

        # Initialize EnginePlanner if engine_planner config is provided
        if hasattr(config, 'engine_planner'):
            self.planner = EnginePlanner(agent_graph=self.graph, memory=self.memory, config=config.engine_planner, task=self.task)
        else:
            self.planner = None

        # Set max_iterations if it exists, default to 10 otherwise
        self.max_iterations = config.environment.get('max_iterations', 10) if hasattr(config, 'environment') else 10
        self.current_iteration = 0

        self.logger.info("Engine initialized.")


    def _initialize_environment(self, env_config: Dict[str, Any]) -> BaseEnvironment:
        """
        Initialize the environment based on configuration.

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
        
        elif env_type == "Werewolf":
            # Initialize Werewolf environment if type is 'Werewolf'
            config_path = env_config.get("config_path")
            if not config_path or not os.path.exists(config_path):
                raise FileNotFoundError(f"Werewolf environment config file '{config_path}' not found.")
            
            environment = WerewolfEnv(name="Werewolf Environment", config_path=config_path)
            self.logger.debug("Werewolf environment initialized.")
        
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
            agent = BaseAgent(config=agent_config, env=self.environment)
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
            while not self._should_terminate():
                self.current_iteration += 1
                self.logger.info(f"Starting iteration {self.current_iteration}")

                # Assign tasks to agents
                assignment = self.planner.assign_tasks()
                tasks = assignment.get("tasks", {})
                self.logger.info(f"Assigned tasks: {tasks}")

                # Assign tasks to agents
                agents_results = {}
                for agent_id, task in tasks.items():
                    try:
                        agent = self.graph.get_agent(agent_id)
                        self.logger.info(f"Assigning task to {agent_id}: {task}")
                        result = agent.act(task)
                        agents_results[agent_id] = result
                        self.logger.debug(f"Agent '{agent_id}' completed task with result: {result}")
                    except KeyError:
                        self.logger.error(f"Agent '{agent_id}' not found in the graph.")
                    except Exception as e:
                        self.logger.error(f"Error while executing task for agent '{agent_id}': {e}")

                # Update progress based on agents' results
                summary = self._summarize_results(agents_results)
                self.logger.info(summary)
                self.planner.update_progress(summary)

                # Evaluate the current state
                self.evaluator.update(self.environment, self.agents)

                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step(agents_results)
                if not continue_simulation:
                    self.logger.info("EnginePlanner decided to terminate the simulation.")
                    break

                # Check if task is completed within the environment
                if self.environment.is_task_completed():
                    self.logger.info("Task has been completed successfully.")
                    break

                if self.current_iteration >= self.max_iterations:
                    self.logger.info("Maximum iterations reached.")
                    break

            self.logger.info("Engine simulation loop completed.")

        except Exception:
            self.logger.exception("An error occurred during simulation.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Simulation completed.")

    def _should_terminate(self) -> bool:
        """
        Determine whether the simulation should terminate.

        Returns:
            bool: True if should terminate, False otherwise.
        """
        # Placeholder for any additional termination conditions
        return False

    def _summarize_results(self, agents_results: Dict[str, Any]) -> str:
        """
        Summarize the agents' results into a string.

        Args:
            agents_results (Dict[str, Any]): The results from all agents.

        Returns:
            str: The summary string.
        """
        summary = "Agents' Results Summary:\n"
        for agent_id, result in agents_results.items():
            summary += f"- {agent_id}: {result}\n"
        self.logger.debug(f"Summarized agents' results:\n{summary}")
        return summary

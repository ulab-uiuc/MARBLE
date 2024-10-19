# marble/engine/engine.py

"""
The core engine module that coordinates agents within the environment.
"""

from typing import Any, Dict, List, Union

from marble.agent import BaseAgent, ReasoningAgent
from marble.configs.config import Config
from marble.engine.engine_planner import EnginePlanner
from marble.environments import BaseEnvironment, WebEnvironment
from marble.evaluator.evaluator import Evaluator
from marble.graph.agent_graph import AgentGraph
from marble.memory.base_memory import BaseMemory
from marble.memory.shared_memory import SharedMemory
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

        # Initialize Memory
        self.memory = self._initialize_memory(config.memory)

        # Initialize Agents
        self.agents = self._initialize_agents(config.agents)

        # Initialize AgentGraph
        self.graph = AgentGraph(self.agents, config.graph)

        # Initialize Environment
        self.environment = self._initialize_environment(config.environment)

        # Initialize Evaluator
        self.evaluator = Evaluator(metrics_config=config.metrics)

        # Initialize EnginePlanner
        self.planner = EnginePlanner(agent_graph=self.graph, memory=self.memory, config=config.engine_planner)

        self.max_iterations = config.environment.get('max_iterations', 10)
        self.current_iteration = 0
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
                agent = ReasoningAgent(config=agent_config, shared_memory=self.memory)
            else:
                agent = BaseAgent(config=agent_config, shared_memory=self.memory)
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

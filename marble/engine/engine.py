# marble/engine/engine.py

"""
The core engine module that coordinates agents within the environment.
"""
from typing import Any, Dict, List, Optional, Union

from marble.agent import BaseAgent
from marble.configs.config import Config
from marble.engine.engine_planner import EnginePlanner
from marble.environments import BaseEnvironment, ResearchEnvironment, WebEnvironment
from marble.evaluator.evaluator import Evaluator
from marble.graph.agent_graph import AgentGraph
from marble.memory.base_memory import BaseMemory
from marble.memory.shared_memory import SharedMemory
from marble.utils.logger import get_logger

EnvType = Union[BaseEnvironment, WebEnvironment, ResearchEnvironment]
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
        # Initialize Environment
        self.environment = self._initialize_environment(config.environment)
        # Initialize Agents
        self.agents = self._initialize_agents(config.agents)
        # Initialize AgentGraph
        self.graph = AgentGraph(self.agents, config)
        for agent in self.agents:
            agent.set_agent_graph(self.graph)
        # Initialize Memory
        self.memory = self._initialize_memory(config.memory)
        # Initialize Evaluator
        self.evaluator = Evaluator(metrics_config=config.metrics)
        self.task = config.task.get('content', '')
        self.coordinate_mode = config.coordination_mode
        # Initialize EnginePlanner
        self.planner = EnginePlanner(agent_graph=self.graph, memory=self.memory, config=config.engine_planner, task=self.task)
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
            env1 = WebEnvironment(name="Web Environment", config=env_config)
            return env1
        elif env_type == "Base":
            env2 = BaseEnvironment(name="Base Environment", config=env_config)
            return env2
        elif env_type == "Research":
            env3 = ResearchEnvironment(name="Research Environment", config=env_config)
            return env3
        else:
            raise ValueError(f"Unsupported environment type: {env_type}")


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

    def star_coordinate(self) -> None:
        """
        Centralized coordination mode.
        """
        try:
            while not self._should_terminate():
                self.current_iteration += 1
                self.logger.info(f"Starting iteration {self.current_iteration}")

                # Assign tasks to agents
                assignment = self.planner.assign_tasks()
                tasks = assignment.get("tasks", {})
                self.logger.info(f"Assigned tasks: {tasks}")

                # Assign tasks to agents
                agents_results = []
                for agent_id, task in tasks.items():
                    try:
                        agent = self.graph.get_agent(agent_id)
                        self.logger.info(f"Assigning task to {agent_id}: {task}")
                        result = agent.act(task)
                        agents_results.append({agent_id: result})
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

    def graph_coordinate(self) -> None:
        """
        Graph-based coordination mode.
        """
        try:
            # Initial assignment: Distribute the overall task to each agent
            self.logger.info("Initial task distribution to all agents.")
            initial_tasks = {agent.agent_id: self.task for agent in self.graph.get_all_agents()}
            agents_results = []
            for agent_id, task in initial_tasks.items():
                try:
                    agent = self.graph.get_agent(agent_id)
                    self.logger.info(f"Assigning initial task to {agent_id}: {task}")
                    result = agent.act(task)
                    agents_results.append({agent_id: result})
                    self.logger.debug(f"Agent '{agent_id}' completed initial task with result: {result}")
                except KeyError:
                    self.logger.error(f"Agent '{agent_id}' not found in the graph.")
                except Exception as e:
                    self.logger.error(f"Error while executing initial task for agent '{agent_id}': {e}")

            # Update progress based on initial results
            summary = self._summarize_results(agents_results)
            self.logger.info(f"Initial Summary:\n{summary}")
            self.planner.update_progress(summary)

            # Evaluate the initial state
            self.evaluator.update(self.environment, self.agents)

            # Begin iterative coordination
            while self.current_iteration < self.max_iterations:
                self.current_iteration += 1
                self.logger.info(f"Starting iteration {self.current_iteration}")

                current_agents = self.graph.get_all_agents()
                current_tasks = {}
                agents_results = []

                for agent in current_agents:
                    try:
                        # Each agent plans its own task
                        task = agent.plan_task()
                        current_tasks[agent.agent_id] = task
                        self.logger.info(f"Agent '{agent.agent_id}' planned task: {task}")

                        # Agent acts on the planned task
                        result = agent.act(task)
                        agents_results.append({agent.agent_id: result})
                        self.logger.debug(f"Agent '{agent.agent_id}' executed task with result: {result}")
                    except Exception as e:
                        self.logger.error(f"Error in agent '{agent.agent_id}' during planning or action: {e}")

                # Summarize outputs and update planner
                summary = self._summarize_results(agents_results)
                self.logger.info(f"Iteration {self.current_iteration} Summary:\n{summary}")
                self.planner.summarize_output(summary, self.task)

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

            self.logger.info("Engine graph-based coordination loop completed.")

        except Exception:
            self.logger.exception("An error occurred during graph-based coordination.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Graph-based coordination simulation completed.")

    def tree_coordinate(self) -> None:
        """
        Tree-based coordination mode.
        """
        try:
            self.logger.info("Starting tree-based coordination.")
            root_agent = self.graph.get_root_agent()
            if not root_agent:
                self.logger.error("No root agent found in the tree.")
                return

            # Start the coordination from the root agent
            while self.current_iteration < self.max_iterations:
                self.current_iteration += 1
                self.logger.info(f"Starting iteration {self.current_iteration}")

                result = self._execute_agent_task_recursive(root_agent, self.task)

                # Update progress
                summary = self._summarize_results([{'root_agent': result}])
                self.logger.info(f"Iteration {self.current_iteration} Summary:\n{summary}")
                self.planner.update_progress(summary)

                # Evaluate the current state
                self.evaluator.update(self.environment, self.agents)

                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step([{'root_agent': result}])
                if not continue_simulation:
                    self.logger.info("EnginePlanner decided to terminate the simulation.")
                    break

            self.logger.info("Tree-based coordination simulation completed.")

        except Exception:
            self.logger.exception("An error occurred during tree-based coordination.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Tree-based coordination simulation completed.")

    def _execute_agent_task_recursive(self, agent: BaseAgent, task: str) -> Any:
        """
        Recursively execute tasks starting from the given agent.

        Args:
            agent (BaseAgent): The agent to execute task.
            task (str): The task to execute.

        Returns:
            Any: The result of the agent's execution.
        """
        self.logger.info(f"Agent '{agent.agent_id}' is executing task.")

        if agent.children:
            # Agent assigns tasks to children
            tasks_for_children = agent.plan_tasks_for_children(task)
            children_results = {}
            for child in agent.children:
                child_task = tasks_for_children.get(child.agent_id, "")
                if child_task:
                    child_result = self._execute_agent_task_recursive(child, child_task)
                    children_results[child.agent_id] = child_result
            # Agent may also act itself
            own_result = agent.act(task)
            # Combine results
            combined_result = agent.summarize_results(children_results, own_result)
            return combined_result
        else:
            # Agent directly acts on the task
            result = agent.act(task)
            return result

    def chain_coordinate(self) -> None:
        """
        Chain-based coordination mode.
        """
        try:
            self.logger.info("Starting chain-based coordination.")
            # Start with the initial agent
            current_agent = self._select_initial_agent()
            if not current_agent:
                self.logger.error("No initial agent found for chain.")
                return

            max_chain_length = self.max_iterations  # Or define a separate chain length limit
            chain_length = 0

            task = self.task
            agents_results = []
            visited_agents = set()

            while current_agent and chain_length < max_chain_length:
                self.logger.info(f"Agent '{current_agent.agent_id}' is executing task.")
                result = current_agent.act(task)
                agents_results.append({current_agent.agent_id: result})
                self.logger.info(f"Agent '{current_agent.agent_id}' completed task with result: {result}")

                # Prevent loops
                visited_agents.add(current_agent.agent_id)

                # Get profiles of other agents
                agent_profiles = self.graph.get_agent_profiles()
                # Current agent chooses the next agent
                next_agent_id, plan = current_agent.plan_next_agent(result, agent_profiles)
                current_agent = self.graph.get_agent(next_agent_id)
                task = plan
                chain_length += 1
                self.planner.update_progress(result)
                continue_simulation = self.planner.decide_next_step([{'root_agent': result}])
                if not continue_simulation:
                    self.logger.info("EnginePlanner decided to terminate the simulation.")
                    break

            # Update progress
            summary = self._summarize_results(agents_results)
            self.logger.info(f"Chain execution Summary:\n{summary}")
            self.planner.update_progress(summary)


            self.logger.info("Chain-based coordination simulation completed.")

        except Exception:
            self.logger.exception("An error occurred during chain-based coordination.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Chain-based coordination simulation completed.")

    def _select_initial_agent(self) -> Optional[BaseAgent]:
        """
        Select the initial agent to start the chain.

        Returns:
            Optional[BaseAgent]: The initial agent, or None if not found.
        """
        # For simplicity, select an agent based on some criteria.
        # Here, we'll select the agent with the highest priority or a predefined agent.
        # Alternatively, we could prompt the LLM to select the starting agent.

        # Example: Select agent1 as the starting agent
        starting_agent_id = 'agent1'
        if starting_agent_id in [agent.agent_id for agent in self.agents]:
            return self.graph.get_agent(starting_agent_id)
        else:
            self.logger.error(f"Starting agent '{starting_agent_id}' not found.")
            return None

    def start(self) -> None:
        """
        Start the engine to run the simulation.
        """
        self.logger.info("Engine starting simulation.")
        if self.coordinate_mode == "star":
            self.logger.info("Running in centralized coordination mode.")
            self.star_coordinate()
        elif self.coordinate_mode == "graph":
            self.logger.info("Running in graph-based coordination mode.")
            self.graph_coordinate()
        elif self.coordinate_mode == "chain":
            self.logger.info("Running in chain-based coordination mode.")
            self.chain_coordinate()
        elif self.coordinate_mode == "tree":
            self.logger.info("Running in tree-based coordination mode.")
            self.tree_coordinate()
        else:
            self.logger.error(f"Unsupported coordinate mode: {self.coordinate_mode}")
            raise ValueError(f"Unsupported coordinate mode: {self.coordinate_mode}")


    def _should_terminate(self) -> bool:
        """
        Determine whether the simulation should terminate.

        Returns:
            bool: True if should terminate, False otherwise.
        """
        # Placeholder for any additional termination conditions
        return False

    def _summarize_results(self, agents_results: List[Dict[str, Any]]) -> str:
        """
        Summarize the agents' results into a string.

        Args:
            agents_results (Dict[str, Any]): The results from all agents.

        Returns:
            str: The summary string.
        """
        summary = "Agents' Results Summary:\n"
        # for agent_id, result in agents_results.items():
        #     summary += f"- {agent_id}: {result}\n"
        for result in agents_results:
            summary += f"- {result}\n"

        self.logger.debug(f"Summarized agents' results:\n{summary}")
        return summary

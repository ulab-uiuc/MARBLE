# marble/engine/engine.py

"""
The core engine module that coordinates agents within the environment.
"""
import json
from typing import Any, Dict, List, Optional, Union

from marble.agent import BaseAgent, CodingAgent
from marble.configs.config import Config
from marble.engine.engine_planner import EnginePlanner
from marble.environments import BaseEnvironment, ResearchEnvironment, WebEnvironment, CodingEnvironment
from marble.evaluator.evaluator import Evaluator
from marble.graph.agent_graph import AgentGraph
from marble.memory.base_memory import BaseMemory
from marble.memory.shared_memory import SharedMemory
from marble.utils.logger import get_logger

EnvType = Union[BaseEnvironment, WebEnvironment, ResearchEnvironment, CodingEnvironment]
AgentType = Union[BaseAgent, CodingAgent]

class Engine:
    """
    The Engine class orchestrates the simulation, coordinating agents and the environment.
    """
    def _read_code_from_file(self, file_path: str) -> str:
        """
        从指定文件路径读取代码。

        Args:
            file_path (str): 文件路径

        Returns:
            str: 文件内容
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            self.logger.error(f"Failed to read code from {file_path}: {e}")
            return ""

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
        self.output_format = config.task.get('output_format','You are free to define your own output format to answer the task properly.')
        self.coordinate_mode = config.coordination_mode
        # Initialize EnginePlanner
        self.planner = EnginePlanner(agent_graph=self.graph, memory=self.memory, config=config.engine_planner, task=self.task, model=config.llm)
        self.max_iterations = config.environment.get('max_iterations', 10)
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
            env1 = WebEnvironment(name="Web Environment", config=env_config)
            return env1
        elif env_type == "Base":
            env2 = BaseEnvironment(name="Base Environment", config=env_config)
            return env2
        elif env_type == "Research":
            env3 = ResearchEnvironment(name="Research Environment", config=env_config)
            return env3
        elif env_type == "Coding":
            env4 = CodingEnvironment(name="Coding Environment", config=env_config)
            return env4
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
        llm = self.config.llm
        for agent_config in agent_configs:
            agent_type = agent_config.get("type")
            agent = BaseAgent(config=agent_config, env=self.environment, model=llm)
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


    def graph_coordinate(self) -> None:
        """
        Graph-based coordination mode.
        """
        try:
            summary_data = {"task": self.task, "coordination_mode": self.coordinate_mode, "iterations": []}
            # Initial assignment: Distribute the overall task to each agent
            self.logger.info("Initial task distribution to all agents.")
            initial_tasks = {agent.agent_id: self.task for agent in self.graph.get_all_agents()}
            agents_results = []

            # Initialize iteration_data for the initial assignment to match iterative structure
            iteration_data = {
                "iteration": self.current_iteration + 1,
                "task_assignments": {},
                "task_results": [],
                "summary": "",
                "continue_simulation": True,
                "communications": [],
            }
            communications = []
            for agent_id, task in initial_tasks.items():
                try:
                    agent = self.graph.get_agent(agent_id)
                    self.logger.info(f"Assigning initial task to {agent_id}: {task}")
                    # Assign the task to the agent
                    iteration_data["task_assignments"][agent_id] = task
                    result, communication = agent.act(task)
                    if communication:
                        communications.append(communication)
                    agents_results.append({agent_id: result})
                    # Record the result
                    task_result = {"agent_id": agent_id, "result": result}
                    iteration_data["task_results"].append(task_result)
                    self.logger.debug(f"Agent '{agent_id}' completed initial task with result: {result}")
                except KeyError:
                    self.logger.error(f"Agent '{agent_id}' not found in the graph.")
                except Exception as e:
                    self.logger.error(f"Error while executing initial task for agent '{agent_id}': {e}")
            iteration_data["communications"] = communications
            # Summarize outputs and update planner for the initial assignment
            summary = self._summarize_results(agents_results)
            self.logger.info(f"Initial Summary:\n{summary}")
            summary = self.planner.summarize_output(summary, self.task, self.output_format)
            iteration_data["summary"] = summary.content

            # Decide whether to continue or terminate after initial assignment
            continue_simulation = self.planner.decide_next_step(agents_results)
            iteration_data["continue_simulation"] = continue_simulation
            if not continue_simulation:
                self.logger.info("EnginePlanner decided to terminate the simulation after initial assignment.")
            else:
                self.planner.update_progress(summary)
                self.current_iteration += 1


            summary_data["iterations"].append(iteration_data)

                    # Evaluate communication
            if iteration_data["communications"]:
                communications_str = self._format_communications(iteration_data["communications"])
                self.evaluator.evaluate_communication(self.task, communications_str)
            else:
                # Store -1 if communications are empty
                self.evaluator.metrics["communication_score"].append(-1)

            # Evaluate planning
            agent_profiles = self._get_agent_profiles()
            agent_tasks_str = self._format_agent_tasks(iteration_data["task_assignments"])
            results_str = self._format_results(iteration_data["task_results"])
            self.evaluator.evaluate_planning(iteration_data["summary"], agent_profiles, agent_tasks_str, results_str)
            self.evaluator.evaluate_kpi(self.task, results_str)

            while self.current_iteration < self.max_iterations:
                iteration_data:Dict[str, Any] = {
                    "iteration": self.current_iteration + 1,
                    "task_assignments": {},
                    "task_results": [],
                    "summary": "",
                    "continue_simulation": True,
                    "communications": [],
                    "total_milestones": 0,
                    "agent_kpis": {}
                }
                self.logger.info(f"Starting iteration {self.current_iteration}")

                current_agents = self.graph.get_all_agents()
                current_tasks = {}
                agents_results = []
                communications = []

                for agent in current_agents:
                    try:
                        # Each agent plans its own task
                        task = agent.plan_task()
                        current_tasks[agent.agent_id] = task
                        iteration_data["task_assignments"][agent.agent_id] = task
                        self.logger.info(f"Agent '{agent.agent_id}' planned task: {task}")

                        # Agent acts on the planned task
                        result, communication = agent.act(task)
                        if communication:
                            communications.append(communication)
                        agents_results.append({agent.agent_id: result})
                        iteration_data["task_results"].append({agent.agent_id: result})
                        self.logger.debug(f"Agent '{agent.agent_id}' executed task with result: {result}")
                    except Exception as e:
                        self.logger.error(f"Error in agent '{agent.agent_id}' during planning or action: {e}")
                iteration_data["communications"] = communications
                # Summarize outputs and update planner
                summary = self._summarize_results(agents_results)
                self.logger.info(f"Iteration {self.current_iteration} Summary:\n{summary}")
                self.current_iteration += 1
                summary = self.planner.summarize_output(summary, self.task, self.output_format)
                iteration_data["summary"] = summary.content


                # Evaluate communication
                if iteration_data["communications"]:
                    communications_str = self._format_communications(iteration_data["communications"])
                    self.evaluator.evaluate_communication(self.task, communications_str)
                else:
                    # Store -1 if communications are empty
                    self.evaluator.metrics["communication_score"].append(-1)

                # Evaluate planning
                agent_profiles = self._get_agent_profiles()
                agent_tasks_str = self._format_agent_tasks(iteration_data["task_assignments"])
                results_str = self._format_results(iteration_data["task_results"])
                self.evaluator.evaluate_planning(iteration_data["summary"], agent_profiles, agent_tasks_str, results_str)
                self.evaluator.evaluate_kpi(self.task, results_str)
                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step(agents_results)
                iteration_data["continue_simulation"] = continue_simulation
                if not continue_simulation:
                    self.logger.info("EnginePlanner decided to terminate the simulation.")
                    break

                # # Check if task is completed within the environment
                # if self.environment.is_task_completed():
                #     self.logger.info("Task has been completed successfully.")
                #     break
                summary_data["iterations"].append(iteration_data)
            # At the end, add the scores to summary_data
            
            summary_data["planning_scores"] = self.evaluator.metrics["planning_score"]
            summary_data["communication_scores"] = self.evaluator.metrics["communication_score"]
            summary_data["token_usage"] = self._get_totoal_token_usage()
            summary_data["agent_kpis"] = self.evaluator.metrics["agent_kpis"]
            summary_data["total_milestones"] = self.evaluator.metrics["total_milestones"]
            if self.environment.name == 'Research Environment':
                self.evaluator.evaluate_task_research(self.task, iteration_data["summary"])
                summary_data['task_evaluation'] = self.evaluator.metrics["task_evaluation"]
                self.logger.info("Engine graph-based coordination loop completed.")
            self.logger.info("Engine graph-based coordination loop completed.")
            if self.environment.name == 'Coding Environment':
                code = self._read_code_from_file('/home/zhe36/MARBLE/marble/workspace/solution.py')
                if code:
                    self.evaluator.evaluate_code_quality(task=self.task, code_result=code)
                    summary_data["code_quality"] = self.evaluator.metrics["code_quality"]
                    self.logger.info(f"Code quality evaluation results: {self.evaluator.metrics['code_quality']}")
            

        except Exception:
            self.logger.exception("An error occurred during graph-based coordination.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Graph-based coordination simulation completed.")
            self._write_to_jsonl(summary_data)

    def star_coordinate(self) -> None:
        """
        Centralized coordination mode.
        """
        try:
            summary_data = {"task": self.task, "coordination_mode": self.coordinate_mode, "iterations": [], "final_output": ""}
            agents_results = []
            while self.current_iteration < self.max_iterations:
                self.current_iteration += 1
                iteration_data:Dict[str, Any] = {
                    "iteration": self.current_iteration + 1,
                    "task_assignments": {},
                    "task_results": [],
                    "summary": "",
                    "continue_simulation": True,
                    "total_milestones": 0,
                    "agent_kpis": {}
                }
                self.logger.info(f"Starting iteration {self.current_iteration}")

                # Assign tasks to agents
                assignment = self.planner.assign_tasks()
                tasks = assignment.get("tasks", {})
                iteration_data["task_assignments"] = tasks
                self.logger.info(f"Assigned tasks: {tasks}")

                # Assign tasks to agents
                agents_results = []
                communications = []
                for agent_id, task in tasks.items():
                    try:
                        agent = self.graph.get_agent(agent_id)
                        self.logger.info(f"Assigning task to {agent_id}: {task}")
                        result, communication = agent.act(task)
                        agents_results.append({agent_id: result})
                        if communication:
                            communications.append(communication)

                        self.logger.debug(f"Agent '{agent_id}' completed task with result: {result}")
                    except KeyError:
                        self.logger.error(f"Agent '{agent_id}' not found in the graph.")
                    except Exception as e:
                        self.logger.error(f"Error while executing task for agent '{agent_id}': {e}")
                iteration_data["task_results"] = agents_results
                iteration_data["communications"] = communications
                # Update progress based on agents' results
                summary = self._summarize_results(agents_results)
                summary = self.planner.summarize_output(summary, self.task,  self.output_format)
                iteration_data["summary"] = summary.content
                self.logger.info(summary)
                self.planner.update_progress(summary)

                # Evaluate communication
                if iteration_data["communications"]:
                    communications_str = self._format_communications(iteration_data["communications"])
                    self.evaluator.evaluate_communication(self.task, communications_str)
                else:
                    # Store -1 if communications are empty
                    self.evaluator.metrics["communication_score"].append(-1)

                # Evaluate planning
                agent_profiles = self._get_agent_profiles()
                agent_tasks_str = self._format_agent_tasks(iteration_data["task_assignments"])
                results_str = self._format_results(iteration_data["task_results"])
                self.evaluator.evaluate_planning(iteration_data["summary"], agent_profiles, agent_tasks_str, results_str)
                self.evaluator.evaluate_kpi(self.task, results_str)

                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step(agents_results)
                iteration_data["continue_simulation"] = continue_simulation
                if not continue_simulation:
                    self.logger.info("EnginePlanner decided to terminate the simulation.")
                    break

                # # Check if task is completed within the environment
                # if self.environment.is_task_completed():
                #     self.logger.info("Task has been completed successfully.")
                #     break

                if self.current_iteration >= self.max_iterations:
                    self.logger.info("Maximum iterations reached.")
                    break

                summary_data["iterations"].append(iteration_data)
            # At the end, add the scores to summary_data
            summary_data["planning_scores"] = self.evaluator.metrics["planning_score"]
            summary_data["communication_scores"] = self.evaluator.metrics["communication_score"]
            summary_data["token_usage"] = self._get_totoal_token_usage()
            summary_data["agent_kpis"] = self.evaluator.metrics["agent_kpis"]
            summary_data["total_milestones"] = self.evaluator.metrics["total_milestones"]
            if self.environment.name == 'Research Environment':
                self.evaluator.evaluate_task_research(self.task, iteration_data["summary"])
                summary_data['task_evaluation'] = self.evaluator.metrics["task_evaluation"]
                self.logger.info("Engine graph-based coordination loop completed.")
            if self.environment.name == 'Coding Environment':
                code = self._read_code_from_file('/home/zhe36/MARBLE/marble/workspace/solution.py')
                if code:
                    self.evaluator.evaluate_code_quality(task=self.task, code_result=code)
                    summary_data["code_quality"] = self.evaluator.metrics["code_quality"]
                    self.logger.info(f"Code quality evaluation results: {self.evaluator.metrics['code_quality']}")
            self.logger.info("Engine simulation loop completed.")

        except Exception:
            self.logger.exception("An error occurred during simulation.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Simulation completed.")
            self._write_to_jsonl(summary_data)

    def chain_coordinate(self) -> None:
        """
        Chain-based coordination mode.
        """
        try:
            self.logger.info("Starting chain-based coordination.")
            summary_data = {"task": self.task, "coordination_mode": self.coordinate_mode, "iterations": []}
            # Start with the initial agent
            current_agent = self._select_initial_agent()
            if not current_agent:
                self.logger.error("No initial agent found for chain.")
                return

            max_chain_length = self.max_iterations * len(self.agents)  # Or define a separate chain length limit
            chain_length = 0

            task = self.task
            agents_results = []

            while current_agent and chain_length < max_chain_length:
                iteration_data = {
                    "chain_length": chain_length + 1,
                    "current_agent": current_agent.agent_id,
                    "result": None,
                    "continue_simulation": True,
                    "task_assignments": {},
                    "total_milestones": 0,
                    "agent_kpis": {}
                }
                self.logger.info(f"Agent '{current_agent.agent_id}' is executing task.")
                result, communication = current_agent.act(task)
                result_str = f"AgentID: '{current_agent.agent_id}' completed task with result: {result}"
                iteration_data["task_assignments"][current_agent.agent_id] = task
                agents_results.append({current_agent.agent_id: result})
                iteration_data["result"] = result
                self.logger.info(f"Agent '{current_agent.agent_id}' completed task with result: {result}")
                # Get profiles of other agents
                agent_profiles = self.graph.get_agent_profiles()
                # Current agent chooses the next agent
                next_agent_id, plan = current_agent.plan_next_agent(result, agent_profiles)
                current_agent = self.graph.get_agent(next_agent_id)
                task = plan
                chain_length += 1
                self.planner.update_progress(result)
                iteration_data["communications"] = communication

                # Evaluate communication
                if iteration_data["communications"]:
                    communications_str = self._format_communications(iteration_data["communications"])
                    self.evaluator.evaluate_communication(self.task, communications_str)
                else:
                    # Store -1 if communications are empty
                    self.evaluator.metrics["communication_score"].append(-1)

                summary = self._summarize_results(agents_results)
                summary = self.planner.summarize_output(summary, self.task,  self.output_format)
                iteration_data["summary"] = summary.content

                # Evaluate planning
                agent_profiles = self._get_agent_profiles()
                agent_tasks_str = self._format_agent_tasks(iteration_data["task_assignments"])
                self.evaluator.evaluate_planning(iteration_data["summary"], agent_profiles, agent_tasks_str, result)
                self.evaluator.evaluate_kpi(self.task, result_str)


                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step([{'root_agent': result}])
                iteration_data["continue_simulation"] = continue_simulation
                summary_data["iterations"].append(iteration_data)
                if not continue_simulation:
                    self.logger.info("EnginePlanner decided to terminate the simulation.")
                    break
            # Update progress
            summary = self._summarize_results(agents_results)
            self.logger.info(f"Chain execution Summary:\n{summary}")
            self.planner.update_progress(summary)

            # At the end, add the scores to summary_data
            summary_data["planning_scores"] = self.evaluator.metrics["planning_score"]
            summary_data["communication_scores"] = self.evaluator.metrics["communication_score"]
            summary_data["token_usage"] = self._get_totoal_token_usage()
            summary_data["agent_kpis"] = self.evaluator.metrics["agent_kpis"]
            summary_data["total_milestones"] = self.evaluator.metrics["total_milestones"]
            if self.environment.name == 'Research Environment':
                self.evaluator.evaluate_task_research(self.task, iteration_data["summary"])
                summary_data['task_evaluation'] = self.evaluator.metrics["task_evaluation"]
                self.logger.info("Engine graph-based coordination loop completed.")
            if self.environment.name == 'Coding Environment':
                code = self._read_code_from_file('/home/zhe36/MARBLE/marble/workspace/solution.py')
                if code:
                    self.evaluator.evaluate_code_quality(task=self.task, code_result=code)
                    summary_data["code_quality"] = self.evaluator.metrics["code_quality"]
                    self.logger.info(f"Code quality evaluation results: {self.evaluator.metrics['code_quality']}")
        
        
            self.logger.info("Chain-based coordination simulation completed.")

        except Exception:
            self.logger.exception("An error occurred during chain-based coordination.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Chain-based coordination simulation completed.")
            self._write_to_jsonl(summary_data)

    def tree_coordinate(self) -> None:
        """
        Tree-based coordination mode.
        """
        try:
            self.logger.info("Starting tree-based coordination.")
            summary_data = {"task": self.task, "coordination_mode": self.coordinate_mode, "iterations": []}

            root_agent = self.graph.get_root_agent()
            if not root_agent:
                self.logger.error("No root agent found in the tree.")
                return

            # Start the coordination from the root agent
            while self.current_iteration < self.max_iterations:
                iteration_data:Dict[str, Any] = {
                    "iteration": self.current_iteration + 1,
                    "root_agent": root_agent.agent_id,
                    "result": None,
                    "continue_simulation": True,
                    "total_milestones": 0,
                    "agent_kpis": {}
                }
                self.current_iteration += 1
                self.logger.info(f"Starting iteration {self.current_iteration}")
                results, communication, tasks = self._execute_agent_task_recursive(root_agent, self.task)

                # Update progress
                summary = self._summarize_results(results)
                summary = self.planner.summarize_output(summary, self.task,  self.output_format)
                iteration_data["summary"] = summary.content
                self.logger.info(f"Iteration {self.current_iteration} Summary:\n{summary}")
                self.planner.update_progress(summary)
                iteration_data["communications"] = communication
                iteration_data["task_assignments"] = tasks
                iteration_data["task_results"] = results

                # Evaluate communication
                if iteration_data["communications"]:
                    communications_str = self._format_communications(iteration_data["communications"])
                    self.evaluator.evaluate_communication(self.task, communications_str)
                else:
                    # Store -1 if communications are empty
                    self.evaluator.metrics["communication_score"].append(-1)

                # Evaluate planning
                agent_profiles = self._get_agent_profiles()
                agent_tasks_str = self._format_agent_tasks(iteration_data["task_assignments"])
                results_str = self._format_results(iteration_data["task_results"])
                self.evaluator.evaluate_planning(iteration_data["summary"], agent_profiles, agent_tasks_str, results_str)
                self.evaluator.evaluate_kpi(self.task, results_str)

                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step(results)
                iteration_data["continue_simulation"] = continue_simulation
                if not continue_simulation:
                    self.logger.info("EnginePlanner decided to terminate the simulation.")
                    break

                summary_data["iterations"].append(iteration_data)
            # At the end, add the scores to summary_data
            summary_data["planning_scores"] = self.evaluator.metrics["planning_score"]
            summary_data["communication_scores"] = self.evaluator.metrics["communication_score"]
            summary_data["token_usage"] = self._get_totoal_token_usage()
            summary_data["agent_kpis"] = self.evaluator.metrics["agent_kpis"]
            summary_data["total_milestones"] = self.evaluator.metrics["total_milestones"]
            if self.environment.name == 'Research Environment':
                self.evaluator.evaluate_task_research(self.task, iteration_data["summary"])
                summary_data['task_evaluation'] = self.evaluator.metrics["task_evaluation"]
                self.logger.info("Engine graph-based coordination loop completed.")
            if self.environment.name == 'Coding Environment':
                code = self._read_code_from_file('/home/zhe36/MARBLE/marble/workspace/solution.py')
                if code:
                    self.evaluator.evaluate_code_quality(task=self.task, code_result=code)
                    summary_data["code_quality"] = self.evaluator.metrics["code_quality"]
                    self.logger.info(f"Code quality evaluation results: {self.evaluator.metrics['code_quality']}")
            self.logger.info("Tree-based coordination simulation completed.")

        except Exception:
            self.logger.exception("An error occurred during tree-based coordination.")
            raise
        finally:
            self.evaluator.finalize()
            self.logger.info("Tree-based coordination simulation completed.")
            self._write_to_jsonl(summary_data)

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
        tasks = []
        if agent.children:
            # Agent assigns tasks to children
            tasks_for_children = agent.plan_tasks_for_children(task)
            tasks.append(tasks_for_children)
            children_results = []
            communications = []
            for child in agent.children:
                child_task = tasks_for_children.get(child.agent_id, "")
                if child_task:
                    child_result, communication, tasks_ = self._execute_agent_task_recursive(child, child_task)
                    tasks += tasks_
                    if communication:
                        communications.append(communication)
                    children_results += child_result
            # Agent may also act itself
            own_result, communication = agent.act(task)
            if communication:
                communications.append(communication)
            communications_str = "\n".join(communications) if communications else None
            # # Combine results
            # combined_result = agent.summarize_results(children_results, own_result)
            results = [{'agent_id':agent.agent_id, 'result':own_result}] + children_results
            return results, communications_str, tasks
        else:
            # Agent directly acts on the task
            result, communication = agent.act(task)
            return [{'agent_id':agent.agent_id, 'result':result}], communication, tasks

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

    def _write_to_jsonl(self, summary_data: Dict[str, Any]) -> None:
        """
        Write summary data to the JSONL file.

        Args:
            summary_data (List[Dict[str, Any]]): Summary data to write to the JSONL file.
        """
        file_path = self.config.output.get("file_path", "result/discussion_output.jsonl")
        try:
            with open(file_path, "a") as jsonl_file:
                print(summary_data)
                jsonl_file.write(json.dumps(summary_data) + "\n")

                jsonl_file.flush()
            self.logger.info(f"Summary data successfully written to {file_path}")
        except IOError as e:
            self.logger.error(f"Failed to write summary data to {file_path}: {e}")

    def _get_final_ooutput_in_graph(self):
        """
        Get the final output graph.

        Returns:
            Dict[str, Any]: The final output graph.
        """
        return self.graph.get_output_graph()

    def _format_communications(self, communications: List[Any]) -> str:
        """
        Formats the communications list into a string suitable for evaluator input.
        """
        # Assuming each communication is a string or can be converted to string
        return "\n".join(str(c) for c in communications)

    def _get_agent_profiles(self) -> str:
        """
        Retrieves and formats agent profiles into a string.
        """
        agent_profiles = []
        for agent in self.graph.get_all_agents():
            # Assuming agent has attributes agent_id and profile
            agent_profiles.append(f"Agent ID: {agent.agent_id}, Profile: {agent.profile}")
        return "\n".join(agent_profiles)

    def _format_agent_tasks(self, agent_tasks: Dict[str, Any]) -> str:
        """
        Formats agent tasks into a string.
        """
        try:
            return "\n".join(f"Agent {agent_id}: Task: {task}" for agent_id, task in agent_tasks.items())
        except Exception:
            return "\n".join(json.dumps(item) for item in agent_tasks)

    def _format_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Formats results into a string.
        """
        results_str = []
        for result in results:
            if "agent_id" in result and "result" in result:
                agent_id = result["agent_id"]
                res_content = result["result"]
                results_str.append(f"AgentID: {agent_id}: Result: {res_content}")
            else:
                for agent_id, res_content in result.items():
                    results_str.append(f"Agent {agent_id}: Result: {res_content}")
        return "\n".join(results_str)

    def _get_totoal_token_usage(self) -> int:
        """
        Get the total token usage by all agents.
        """
        return sum(agent.token_usage for agent in self.graph.get_all_agents()) + self.planner.token_usage

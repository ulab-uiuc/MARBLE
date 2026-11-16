# marble/engine/engine.py

"""
The core engine module that coordinates agents within the environment.
"""
import json
import os
from typing import Any, Dict, List, Optional, Union

from marble.agent import BaseAgent
from marble.configs.config import Config
from marble.engine.engine_planner import EnginePlanner
from marble.environments import (
    BaseEnvironment,
    CodingEnvironment,
    DBEnvironment,
    MinecraftEnvironment,
    ResearchEnvironment,
    WebEnvironment,
    WorldSimulationEnvironment,
)
from marble.evaluator.evaluator import Evaluator
from marble.graph.agent_graph import AgentGraph
from marble.memory.base_memory import BaseMemory
from marble.memory.shared_memory import SharedMemory
from marble.utils.logger import get_logger
from marble.utils.paths import DATA_DIR, ensure_parent_dir

EnvType = Union[
    BaseEnvironment,
    WebEnvironment,
    ResearchEnvironment,
    WorldSimulationEnvironment,
    MinecraftEnvironment,
    DBEnvironment,
    CodingEnvironment,
]
AgentType = Union[BaseAgent]


class Engine:
    """
    The Engine class orchestrates the simulation, coordinating agents and the environment.
    """

    def _read_code_from_file(self, file_path: str) -> str:
        """
        Read code from a specified file path.

        Args:
            file_path (str): File path

        Returns:
            str: File content
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except IOError as e:
            self.logger.error(f"Failed to read code from {file_path}: {e}")
            return ""

    def _default_llm_name(self) -> str:
        """Model name used when a component has no explicit model configured."""
        llm = self.config.llm
        if isinstance(llm, dict):
            llm = llm.get("model", "")
        return llm or "gpt-3.5-turbo"

    def __init__(self, config: Config):
        """
        Initialize the Engine with the given configuration.

        Args:
            config (Config): Configuration parameters.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.config = config
        self.planning_method = config.engine_planner.get("planning_method", "naive")
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
        self.evaluator = Evaluator(
            metrics_config=config.metrics, default_llm=self._default_llm_name()
        )
        self.task = config.task.get("content", "")
        self.output_format = config.task.get(
            "output_format",
            "You are free to define your own output format to answer the task properly.",
        )
        self.coordinate_mode = config.coordination_mode
        # Initialize EnginePlanner
        self.planner = EnginePlanner(
            agent_graph=self.graph,
            memory=self.memory,
            config=config.engine_planner,
            task=self.task,
            model=self._default_llm_name(),
        )
        # Some benchmark configs store the value as a string ("5").
        self.max_iterations = int(config.environment.get("max_iterations") or 10)
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
            # The coding tools need the real task and the configured model:
            # they used to re-read a hard-coded YAML file and to trust whatever
            # model name the agent passed as a tool argument.
            env4.task_content = self.config.task.get("content", "")
            env4.llm = self._default_llm_name()
            return env4
        elif env_type == "WorldSimulation":
            env4 = WorldSimulationEnvironment(
                name="World Simulation Environment", config=env_config
            )
            return env4
        elif env_type == "Minecraft":
            env5 = MinecraftEnvironment(name="Minecraft Environment", config=env_config)
            return env5
        elif env_type == "DB":
            env6 = DBEnvironment(name="DB Environment", config=env_config)
            return env6
        else:
            raise ValueError(f"Unsupported environment type: {env_type}")

    def _initialize_agents(
        self, agent_configs: List[Dict[str, Any]]
    ) -> List[BaseAgent]:
        """
        Initialize agents based on configurations.

        Args:
            agent_configs (List[dict]): List of agent configurations.

        Returns:
            List[BaseAgent]: List of agent instances.
        """
        agents = []
        llm = self._default_llm_name()
        for agent_config in agent_configs:
            agent_llm = agent_config.get(
                "llm", llm
            )  # use agent-specific LLM if provided
            agent_type = agent_config.get("type")
            agent = BaseAgent(
                config=agent_config, env=self.environment, model=agent_llm
            )
            agents.append(agent)
            self.logger.debug(
                f"Agent '{agent.agent_id}' of type '{agent_type}' using LLM '{agent_llm}' initialized."
            )
            if isinstance(self.environment, MinecraftEnvironment):
                assert "agent_id" in agent_config and "agent_port" in agent_config
                self.environment.register_agent(
                    agent_config.get("agent_id"), agent_config.get("agent_port")
                )
            self.logger.debug(
                f"Agent '{agent.agent_id}' of type '{agent_type}' initialized."
            )
        return agents

    def _initialize_memory(
        self, memory_config: Dict[str, Any]
    ) -> Union[SharedMemory, BaseMemory]:
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

    # ------------------------------------------------------------------
    # Evaluation helpers shared by every coordination mode
    # ------------------------------------------------------------------
    def _minecraft_block_hit_rate(self) -> float:
        """Read the latest block hit rate written by the Minecraft judge."""
        try:
            with open(os.path.join(DATA_DIR, "score.json"), "r") as f:
                return float(json.load(f)[-1]["block_hit_rate"])
        except Exception:
            return 0.0

    def _llm_scoring_enabled(self) -> bool:
        """
        Whether the LLM judge scores communication/planning/milestones.

        Minecraft is scored by the rule-based block hit rate instead, so the
        judge calls stay disabled there.
        """
        return not isinstance(self.environment, MinecraftEnvironment)

    def _score_communication(self, communications: Any) -> None:
        """Score one iteration's communications (-1 when there is nothing to score)."""
        if communications and self._llm_scoring_enabled():
            try:
                self.evaluator.evaluate_communication(
                    self.task, self._format_communications(communications)
                )
                return
            except Exception as e:
                self.logger.error(f"Communication evaluation failed: {e}")
        else:
            self.logger.info("No communications to evaluate")
        # Store -1 if communications are empty or could not be scored
        self.evaluator.metrics["communication_score"].append(-1)

    def _score_planning_and_kpi(
        self, summary: str, task_assignments: Any, results_str: str
    ) -> None:
        """Score one iteration's planning quality and extract milestones (KPI)."""
        if not self._llm_scoring_enabled():
            self.evaluator.metrics["planning_score"].append(-1)
            return
        try:
            self.evaluator.evaluate_planning(
                summary or "",
                self._get_agent_profiles(),
                self._format_agent_tasks(task_assignments),
                results_str,
            )
        except Exception as e:
            self.logger.error(f"Planning evaluation failed: {e}")
            self.evaluator.metrics["planning_score"].append(-1)
        try:
            self.evaluator.evaluate_kpi(self.task, results_str)
        except Exception as e:
            self.logger.error(f"KPI evaluation failed: {e}")

    def _solution_path(self) -> str:
        """Path of the deliverable produced by the coding environment."""
        workspace_dir = getattr(self.environment, "workspace_dir", "workspace")
        return os.path.join(workspace_dir, "solution.py")

    def _evaluate_final_task(
        self, summary_data: Dict[str, Any], final_summary: str
    ) -> None:
        """
        Run the environment-specific task evaluation and store it in ``summary_data``.

        This is identical for every coordination mode; it used to be copy-pasted
        per mode, and the copies had drifted apart (e.g. no code-quality score in
        graph mode, no research score in chain mode).
        """
        try:
            if isinstance(self.environment, ResearchEnvironment):
                self.evaluator.evaluate_task_research(self.task, final_summary)
                summary_data["task_evaluation"] = self.evaluator.metrics[
                    "task_evaluation"
                ]
            elif isinstance(self.environment, CodingEnvironment):
                solution_path = self._solution_path()
                code = self._read_code_from_file(solution_path)
                if code:
                    self.evaluator.evaluate_code_quality(
                        task=self.task, code_result=code
                    )
                    self.logger.info(
                        f"Code quality evaluation results: {self.evaluator.metrics['code_quality']}"
                    )
                else:
                    self.logger.error(
                        f"No solution found at {solution_path}; skipping code quality evaluation."
                    )
                summary_data["code_quality"] = self.evaluator.metrics["code_quality"]
                summary_data["solution_path"] = solution_path
            elif isinstance(self.environment, WorldSimulationEnvironment):
                self.evaluator.evaluate_task_world(self.task, final_summary)
                summary_data["task_evaluation"] = self.evaluator.metrics[
                    "task_evaluation"
                ]
            elif isinstance(self.environment, MinecraftEnvironment):
                summary_data["task_evaluation"] = self._minecraft_block_hit_rate() * 5
            elif isinstance(self.environment, DBEnvironment):
                self.evaluator.evaluate_task_db(
                    self.task,
                    final_summary,
                    self.config.task["labels"],
                    self.config.task["number_of_labels_pred"],
                    self.config.task["root_causes"],
                )
                summary_data["task_evaluation"] = self.evaluator.metrics[
                    "task_evaluation"
                ]
        except Exception as e:
            # Keep the run's transcript even when the judge call fails.
            self.logger.error(f"Final task evaluation failed: {e}")
            summary_data["task_evaluation_error"] = str(e)

    def graph_coordinate(self) -> None:
        """
        Graph-based coordination mode.
        """
        try:
            summary_data = {
                "task": self.task,
                "coordination_mode": self.coordinate_mode,
                "iterations": [],
            }
            # Initial assignment: Distribute the overall task to each agent
            self.logger.info("Initial task distribution to all agents.")
            initial_tasks = {
                agent.agent_id: self.task for agent in self.graph.get_all_agents()
            }
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
                    iteration_data_task_assignments = iteration_data.get(
                        "task_assignments"
                    )
                    assert isinstance(iteration_data_task_assignments, dict)
                    iteration_data_task_assignments[agent_id] = task
                    result, communication = agent.act(task)
                    self.logger.info(f"Processing result for agent '{agent.agent_id}'")
                    self.logger.info(f"Communication received: {communication}")
                    if communication:
                        self.logger.info(
                            f"Adding communication to list: {communication}"
                        )
                        communications.append(communication)
                    agents_results.append({agent_id: result})
                    # Record the result
                    task_result = {"agent_id": agent_id, "result": result}
                    iteration_data_task_results = iteration_data.get("task_results")
                    assert isinstance(iteration_data_task_results, list)
                    iteration_data_task_results.append(task_result)
                    self.logger.debug(
                        f"Agent '{agent_id}' completed initial task with result: {result}"
                    )
                except KeyError:
                    self.logger.error(f"Agent '{agent_id}' not found in the graph.")
                except Exception as e:
                    self.logger.error(
                        f"Error while executing initial task for agent '{agent_id}': {e}"
                    )
            iteration_data["communications"] = communications
            # Summarize outputs and update planner for the initial assignment
            summary = self._summarize_results(agents_results)
            self.logger.info(f"Initial Summary:\n{summary}")
            summary = self.planner.summarize_output(
                summary, self.task, self.output_format
            )
            iteration_data["summary"] = summary.content or ""

            # Decide whether to continue or terminate after initial assignment
            if isinstance(self.environment, MinecraftEnvironment):
                block_hit_rate = self._minecraft_block_hit_rate()
                self.logger.info(
                    f"Using a rule-based EnginePlanner. block_hit_rate is {block_hit_rate}"
                )
                continue_simulation = int(block_hit_rate) != 1
            else:
                continue_simulation = self.planner.decide_next_step(agents_results)
            iteration_data["continue_simulation"] = continue_simulation
            if not continue_simulation:
                self.logger.info(
                    "EnginePlanner decided to terminate the simulation after initial assignment."
                )
            else:
                self.planner.update_progress(summary)
                self.current_iteration += 1

            summary_data["iterations"].append(iteration_data)

            # Evaluate communication, planning and milestones (KPI)
            self._score_communication(iteration_data["communications"])
            self._score_planning_and_kpi(
                summary=iteration_data["summary"],
                task_assignments=iteration_data["task_assignments"],
                results_str=self._format_results(iteration_data["task_results"]),
            )

            end_on_iter_0 = False
            if not continue_simulation:
                end_on_iter_0 = True

            while self.current_iteration < self.max_iterations and not end_on_iter_0:
                iteration_data = {
                    "iteration": self.current_iteration + 1,
                    "task_assignments": {},
                    "task_results": [],
                    "summary": "",
                    "continue_simulation": True,
                    "communications": [],
                    "total_milestones": 0,
                    "agent_kpis": {},
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
                        iteration_data_task_assignments = iteration_data.get(
                            "task_assignments"
                        )
                        assert isinstance(iteration_data_task_assignments, dict)
                        iteration_data_task_assignments[agent.agent_id] = task
                        self.logger.info(
                            f"Agent '{agent.agent_id}' planned task: {task}"
                        )

                        # Agent acts on the planned task
                        result, communication = agent.act(task)
                        self.logger.info(
                            f"Processing result for agent '{agent.agent_id}'"
                        )
                        self.logger.info(f"Communication received: {communication}")
                        if communication:
                            self.logger.info(
                                f"Adding communication to list: {communication}"
                            )
                            communications.append(communication)
                        agents_results.append({agent.agent_id: result})
                        iteration_data_task_results = iteration_data.get("task_results")
                        assert isinstance(iteration_data_task_results, list)
                        iteration_data_task_results.append(
                            {"agent_id": agent.agent_id, "result": result}
                        )
                        self.logger.debug(
                            f"Agent '{agent.agent_id}' executed task with result: {result}"
                        )
                    except Exception as e:
                        self.logger.error(
                            f"Error in agent '{agent.agent_id}' during planning or action: {e}"
                        )
                iteration_data["communications"] = communications
                # Summarize outputs and update planner
                summary = self._summarize_results(agents_results)
                self.logger.info(
                    f"Iteration {self.current_iteration} Summary:\n{summary}"
                )
                self.current_iteration += 1
                summary_from_planner = self.planner.summarize_output(
                    summary, self.task, self.output_format
                )
                iteration_data["summary"] = summary_from_planner.content or ""

                # Evaluate communication, planning and milestones (KPI)
                self._score_communication(iteration_data["communications"])
                self._score_planning_and_kpi(
                    summary=iteration_data["summary"],
                    task_assignments=iteration_data["task_assignments"],
                    results_str=self._format_results(iteration_data["task_results"]),
                )
                # Decide whether to continue or terminate
                if isinstance(self.environment, MinecraftEnvironment):
                    block_hit_rate = self._minecraft_block_hit_rate()
                    self.logger.info(
                        f"Using a rule-based EnginePlanner. block_hit_rate is {block_hit_rate}"
                    )
                    continue_simulation = int(block_hit_rate) != 1
                else:
                    continue_simulation = self.planner.decide_next_step(agents_results)
                iteration_data["continue_simulation"] = continue_simulation
                summary_data["iterations"].append(iteration_data)
                if not continue_simulation:
                    self.logger.info(
                        "EnginePlanner decided to terminate the simulation."
                    )
                    break

                # # Check if task is completed within the environment
                # if self.environment.is_task_completed():
                #     self.logger.info("Task has been completed successfully.")
                #     break
            # At the end, add the scores to summary_data

            summary_data["planning_scores"] = self.evaluator.metrics["planning_score"]
            summary_data["communication_scores"] = self.evaluator.metrics[
                "communication_score"
            ]
            summary_data["token_usage"] = self._get_total_token_usage()
            summary_data["agent_kpis"] = self.evaluator.metrics["agent_kpis"]
            summary_data["total_milestones"] = self.evaluator.metrics[
                "total_milestones"
            ]
            self._evaluate_final_task(summary_data, iteration_data.get("summary") or "")
            self.logger.info("Engine graph-based coordination loop completed.")

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
            summary_data = {
                "task": self.task,
                "coordination_mode": self.coordinate_mode,
                "iterations": [],
                "final_output": "",
            }
            agents_results: List[Dict[str, Any]] = []
            while self.current_iteration < self.max_iterations:
                iteration_data: Dict[str, Any] = {
                    "iteration": self.current_iteration + 1,
                    "task_assignments": {},
                    "task_results": [],
                    "summary": "",
                    "continue_simulation": True,
                    "total_milestones": 0,
                    "agent_kpis": {},
                }
                self.logger.info(f"Starting iteration {self.current_iteration}")

                # Assign tasks to agents
                assignment = self.planner.assign_tasks(
                    planning_method=self.planning_method
                )
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

                        self.logger.debug(
                            f"Agent '{agent_id}' completed task with result: {result}"
                        )
                    except KeyError:
                        self.logger.error(f"Agent '{agent_id}' not found in the graph.")
                    except Exception as e:
                        self.logger.error(
                            f"Error while executing task for agent '{agent_id}': {e}"
                        )
                iteration_data["task_results"] = agents_results
                iteration_data["communications"] = communications
                # Update progress based on agents' results
                summary = self._summarize_results(agents_results)
                summary_from_planner = self.planner.summarize_output(
                    summary, self.task, self.output_format
                )
                iteration_data["summary"] = summary_from_planner.content or ""
                self.logger.info(summary)
                self.planner.update_progress(summary)
                self.current_iteration += 1

                # Evaluate communication, planning and milestones (KPI)
                self._score_communication(iteration_data["communications"])
                self._score_planning_and_kpi(
                    summary=iteration_data["summary"],
                    task_assignments=iteration_data["task_assignments"],
                    results_str=self._format_results(iteration_data["task_results"]),
                )

                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step(agents_results)
                iteration_data["continue_simulation"] = continue_simulation
                summary_data["iterations"].append(iteration_data)
                if not continue_simulation:
                    self.logger.info(
                        "EnginePlanner decided to terminate the simulation."
                    )
                    break

                if self.current_iteration >= self.max_iterations:
                    self.logger.info("Maximum iterations reached.")
                    break
            # At the end, add the scores to summary_data
            summary_data["planning_scores"] = self.evaluator.metrics["planning_score"]
            summary_data["communication_scores"] = self.evaluator.metrics[
                "communication_score"
            ]
            summary_data["token_usage"] = self._get_total_token_usage()
            summary_data["agent_kpis"] = self.evaluator.metrics["agent_kpis"]
            summary_data["total_milestones"] = self.evaluator.metrics[
                "total_milestones"
            ]
            self._evaluate_final_task(summary_data, iteration_data.get("summary") or "")
            self.logger.info("Engine star-based coordination loop completed.")

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
            summary_data = {
                "task": self.task,
                "coordination_mode": self.coordinate_mode,
                "iterations": [],
            }
            # Start with the initial agent
            current_agent = self._select_initial_agent()
            if not current_agent:
                self.logger.error("No initial agent found for chain.")
                return

            max_chain_length = self.max_iterations * len(
                self.agents
            )  # Or define a separate chain length limit
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
                    "agent_kpis": {},
                }
                self.logger.info(f"Agent '{current_agent.agent_id}' is executing task.")
                result, communication = current_agent.act(task)
                result_str = f"AgentID: '{current_agent.agent_id}' completed task with result: {result}"
                iteration_data_task_assignments = iteration_data.get("task_assignments")
                assert isinstance(iteration_data_task_assignments, dict)
                iteration_data_task_assignments[current_agent.agent_id] = task
                agents_results.append({current_agent.agent_id: result})
                iteration_data["result"] = result
                self.logger.info(
                    f"Agent '{current_agent.agent_id}' completed task with result: {result}"
                )
                # Get profiles of other agents
                agent_profiles = self.graph.get_agent_profiles_linked(
                    current_agent.agent_id
                )
                # Current agent chooses the next agent
                next_agent_id, plan = current_agent.plan_next_agent(
                    result, agent_profiles
                )
                current_agent_ = current_agent
                try:
                    if not next_agent_id:
                        raise ValueError("no next agent selected")
                    current_agent = self.graph.get_agent(next_agent_id)
                except Exception:
                    self.logger.error(
                        f"Agent '{next_agent_id}' not found in the graph. keep the same agent."
                    )
                    current_agent = current_agent_
                # Keep working on the current task when no usable plan came back
                # (``None`` used to be handed to the next agent as its task).
                task = plan or task
                chain_length += 1
                self.planner.update_progress(result)
                # ``act`` returns a single chat transcript (or None), while the
                # evaluator helpers expect a list of them.
                iteration_data["communications"] = (
                    [communication] if communication else []
                )

                # Evaluate communication
                self._score_communication(iteration_data["communications"])

                summary = self._summarize_results(agents_results)
                summary_from_planner = self.planner.summarize_output(
                    summary, self.task, self.output_format
                )
                iteration_data["summary"] = summary_from_planner.content or ""

                # Evaluate planning and milestones (KPI)
                self._score_planning_and_kpi(
                    summary=iteration_data["summary"],
                    task_assignments=iteration_data["task_assignments"],
                    results_str=result_str,
                )

                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step(
                    [{"root_agent": result}]
                )
                iteration_data["continue_simulation"] = continue_simulation
                summary_data["iterations"].append(iteration_data)
                if not continue_simulation:
                    self.logger.info(
                        "EnginePlanner decided to terminate the simulation."
                    )
                    break
            # Update progress
            summary = self._summarize_results(agents_results)
            self.logger.info(f"Chain execution Summary:\n{summary}")
            self.planner.update_progress(summary)

            # At the end, add the scores to summary_data
            summary_data["planning_scores"] = self.evaluator.metrics["planning_score"]
            summary_data["communication_scores"] = self.evaluator.metrics[
                "communication_score"
            ]
            summary_data["token_usage"] = self._get_total_token_usage()
            summary_data["agent_kpis"] = self.evaluator.metrics["agent_kpis"]
            summary_data["total_milestones"] = self.evaluator.metrics[
                "total_milestones"
            ]
            self._evaluate_final_task(summary_data, iteration_data.get("summary") or "")
            self.logger.info("Engine chain-based coordination loop completed.")

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
            summary_data = {
                "task": self.task,
                "coordination_mode": self.coordinate_mode,
                "iterations": [],
            }

            root_agent = self.graph.get_root_agent()
            if not root_agent:
                self.logger.error("No root agent found in the tree.")
                return
            # Start the coordination from the root agent
            while self.current_iteration < self.max_iterations:
                iteration_data: Dict[str, Any] = {
                    "iteration": self.current_iteration + 1,
                    "root_agent": root_agent.agent_id,
                    "result": None,
                    "continue_simulation": True,
                    "total_milestones": 0,
                    "agent_kpis": {},
                }
                self.current_iteration += 1
                self.logger.info(f"Starting iteration {self.current_iteration}")
                results, communication, tasks = self._execute_agent_task_recursive(
                    root_agent, self.task
                )
                # Update progress
                summary = self._summarize_results(results)
                summary = self.planner.summarize_output(
                    summary, self.task, self.output_format
                )
                iteration_data["summary"] = summary.content or ""
                self.logger.info(
                    f"Iteration {self.current_iteration} Summary:\n{summary.content}"
                )
                self.planner.update_progress(summary)
                iteration_data["communications"] = (
                    [communication] if communication else []
                )
                iteration_data["task_assignments"] = tasks
                iteration_data["task_results"] = results
                # Evaluate communication, planning and milestones (KPI)
                self._score_communication(iteration_data["communications"])
                self._score_planning_and_kpi(
                    summary=iteration_data["summary"],
                    task_assignments=iteration_data["task_assignments"],
                    results_str=self._format_results(iteration_data["task_results"]),
                )

                # Decide whether to continue or terminate
                continue_simulation = self.planner.decide_next_step(results)
                iteration_data["continue_simulation"] = continue_simulation
                summary_data["iterations"].append(iteration_data)
                if not continue_simulation:
                    self.logger.info(
                        "EnginePlanner decided to terminate the simulation."
                    )
                    break
            # At the end, add the scores to summary_data
            summary_data["planning_scores"] = self.evaluator.metrics["planning_score"]
            summary_data["communication_scores"] = self.evaluator.metrics[
                "communication_score"
            ]
            summary_data["token_usage"] = self._get_total_token_usage()
            summary_data["agent_kpis"] = self.evaluator.metrics["agent_kpis"]
            summary_data["total_milestones"] = self.evaluator.metrics[
                "total_milestones"
            ]
            self._evaluate_final_task(summary_data, iteration_data.get("summary") or "")
            self.logger.info("Engine tree-based coordination loop completed.")

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
        if len(agent.children) > 0:
            # Agent assigns tasks to children
            tasks_for_children = agent.plan_tasks_for_children(task)
            tasks.append(tasks_for_children)
            children_results = []
            communications = []
            for child in agent.children:
                child_task = tasks_for_children.get(child.agent_id, "")
                if child_task:
                    (
                        child_result,
                        communication,
                        tasks_,
                    ) = self._execute_agent_task_recursive(child, child_task)
                    tasks += tasks_
                    if communication:
                        communications.append(communication)
                    children_results += child_result
            # Agent may also act itself
            results_str = "\n".join(
                json.dumps(result, default=str)[:500] for result in children_results
            )

            task_for_father = (
                task
                + "\nHere are the results of the children: "
                + results_str
                + "\nPlease don't repeat the same task and continue to work on the original task. You may also need to communicate with other agents or summarize the results or just continue to work on the original task."
            )
            own_result, communication = agent.act(task_for_father)

            if communication:
                communications.append(communication)
            communications_str = "\n".join(communications) if communications else None
            # # Combine results
            # combined_result = agent.summarize_results(children_results, own_result)
            results = [
                {"agent_id": agent.agent_id, "result": own_result}
            ] + children_results
            return results, communications_str, tasks
        else:
            # Agent directly acts on the task
            result, communication = agent.act(task)
            return (
                [{"agent_id": agent.agent_id, "result": result}],
                communication,
                tasks,
            )

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
        starting_agent_id = "agent1"
        if starting_agent_id in [agent.agent_id for agent in self.agents]:
            return self.graph.get_agent(starting_agent_id)
        if self.agents:
            # Agents do not have to be called "agentN": start from the first one.
            self.logger.warning(
                f"Starting agent '{starting_agent_id}' not found; "
                f"starting the chain from '{self.agents[0].agent_id}'."
            )
            return self.agents[0]
        self.logger.error("No agents available to start the chain.")
        return None

    def start(self) -> None:
        """
        Start the engine to run the simulation.
        """
        self.logger.info("Engine starting simulation.")
        if isinstance(self.environment, MinecraftEnvironment):
            self.environment.launch()
        try:
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
                self.logger.error(
                    f"Unsupported coordinate mode: {self.coordinate_mode}"
                )
                raise ValueError(
                    f"Unsupported coordinate mode: {self.coordinate_mode}. "
                    "Use one of: star, graph, chain, tree."
                )
        finally:
            # Always release external resources, even when the run fails.
            if isinstance(self.environment, MinecraftEnvironment):
                self.environment.finish()
            elif isinstance(self.environment, DBEnvironment):
                try:
                    self.environment.terminate()
                except Exception as e:
                    self.logger.error(f"Failed to stop the DB containers: {e}")

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
            shorten_result = f"- {result}"
            shorten_result = shorten_result[:1000]
            summary += f"{shorten_result}\n"

        self.logger.debug(f"Summarized agents' results:\n{summary}")
        return summary

    def _write_to_jsonl(self, summary_data: Dict[str, Any]) -> None:
        """
        Write summary data to the JSONL file.

        Args:
            summary_data (List[Dict[str, Any]]): Summary data to write to the JSONL file.
        """
        file_path = (
            self.config.output.get("file_path") or "result/discussion_output.jsonl"
        )
        # Make every record self-describing so results from many tasks/models
        # can be aggregated from the JSONL file alone.
        for key, value in (
            ("scenario", getattr(self.config, "scenario", None)),
            ("task_id", getattr(self.config, "task_id", None)),
            ("llm", self._default_llm_name()),
            ("evaluate_llm", self.evaluator.llm),
        ):
            if value is not None:
                summary_data.setdefault(key, value)
        try:
            # The output folder is not part of the repository; create it on
            # demand instead of silently dropping the results.
            ensure_parent_dir(file_path)
            with open(file_path, "a", encoding="utf-8") as jsonl_file:
                jsonl_file.write(json.dumps(summary_data, default=str) + "\n")

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

    def _format_communications(self, communications: Any) -> str:
        """
        Formats the communications list into a string suitable for evaluator input.
        """
        # A single transcript is a plain string: joining it would put every
        # character on its own line.
        if isinstance(communications, str):
            return communications
        return "\n".join(str(c) for c in communications if c)

    def _get_agent_profiles(self) -> str:
        """
        Retrieves and formats agent profiles into a string.
        """
        agent_profiles = []
        for agent in self.graph.get_all_agents():
            # Assuming agent has attributes agent_id and profile
            agent_profiles.append(
                f"Agent ID: {agent.agent_id}, Profile: {agent.profile}"
            )
        return "\n".join(agent_profiles)

    def _format_agent_tasks(self, agent_tasks: Dict[str, Any]) -> str:
        """
        Formats agent tasks into a string.
        """
        try:
            return "\n".join(
                f"Agent {agent_id}: Task: {task}"
                for agent_id, task in agent_tasks.items()
            )
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

    def _get_total_token_usage(self) -> int:
        """
        Get the total token usage by all agents.
        """
        return (
            sum(agent.token_usage for agent in self.graph.get_all_agents())
            + self.planner.token_usage
        )

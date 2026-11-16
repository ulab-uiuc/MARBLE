"""
Evaluator module for tracking metrics and evaluating agent performance.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

from marble.agent import BaseAgent
from marble.environments import BaseEnvironment
from marble.llms.model_prompting import model_prompting
from marble.utils.json_utils import extract_json
from marble.utils.logger import get_logger

# Resolved next to this module so the engine can be started from any directory.
EVALUATOR_PROMPTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "evaluator_prompts.json"
)


class Evaluator:
    """
    Evaluator class for tracking metrics like task completion success rate and token consumption.
    """
    def __init__(
        self,
        metrics_config: Optional[Dict[str, Any]],
        default_llm: Optional[str] = None,
    ):
        """
        Initialize the Evaluator with the specified metrics.

        Args:
            metrics_config (Dict[str, Any]): Configuration for the metrics to track.
            default_llm (str, optional): Judge model to use when the config does
                not set ``metrics.evaluate_llm`` (normally the agents' model).
        """
        self.logger = get_logger(self.__class__.__name__)
        self.metrics_config = metrics_config or {}
        self.metrics:Dict[str, Any] = {
            "task_completion": [],
            "token_consumption": [],
            "planning_score": [],
            "communication_score": [],
            "task_evaluation": {},
            "total_milestones": 0,
            "agent_kpis": {},
            "code_quality": {}
        }
        with open(EVALUATOR_PROMPTS_PATH, 'r', encoding='utf-8') as f:
            self.evaluation_prompts = json.load(f)

        fallback_llm = default_llm or 'gpt-3.5-turbo'
        evaluate_llm_config = self.metrics_config.get('evaluate_llm') or {}
        if isinstance(evaluate_llm_config, dict):
            self.llm = evaluate_llm_config.get('model') or fallback_llm
        else:
            self.llm = evaluate_llm_config or fallback_llm



    def update(self, environment: BaseEnvironment, agents: List[BaseAgent]) -> None:
        """
        Update the metrics based on the current state of the environment and agents.

        Args:
            environment (BaseEnvironment): The environment instance.
            agents (List[BaseAgent]): List of agent instances.
        """
        # For task completion, check if the environment indicates the task is done
        if environment.is_task_completed():
            self.metrics["task_completion"].append(1)
        else:
            self.metrics["task_completion"].append(0)

        # For token consumption, sum up the tokens used by agents in this iteration
        total_tokens = sum(agent.get_token_usage() for agent in agents)
        self.metrics["token_consumption"].append(total_tokens)

    def evaluate_communication(self, task: str, communications: str) -> None:
        """
        Evaluate communication between agents and update the communication score.

        Args:
            task (str): The task description.
            communications (str): The communication logs between agents.
        """
        # Get the communication prompt
        communication_prompt_template = self.evaluation_prompts["Graph"]["Communication"]["prompt"]
        # Fill in the placeholders {task} and {communications}
        prompt = communication_prompt_template.format(task=task, communications=communications)
        # Call the language model
        result = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "user", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
        )[0]
        # Parse the score from result.content
        score = self.parse_score(result.content or "")
        # Update the metric
        self.metrics["communication_score"].append(score)

    def evaluate_planning(self, summary: str, agent_profiles: str, agent_tasks: str, results: str) -> None:
        """
        Evaluate planning and self-coordination among agents and update the planning score.

        Args:
            summary (str): Last round summary.
            agent_profiles (str): Profiles of agents.
            agent_tasks (str): Tasks assigned to agents.
            results (str): Results of the next round.
        """
        # Get the planning prompt
        planning_prompt_template = self.evaluation_prompts["Graph"]["Planning"]["prompt"]
        # Fill in the placeholders
        prompt = planning_prompt_template.format(
            summary=summary,
            agent_profiles=agent_profiles,
            agent_tasks=agent_tasks,
            results=results
        )
        # Call the language model
        result = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "user", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
        )[0]
        # Parse the score from result.content
        score = self.parse_score(result.content or "")
        # Update the metric
        self.metrics["planning_score"].append(score)

    def evaluate_kpi(self, task: str, agent_results: str) -> None:
        """
        Evaluate milestones achieved and update agent KPIs.

        Args:
            task (str): The task description.
            agent_results (str): The results from the agents.
        """
        # Get the KPI prompt
        MAX_LENGTH = 7200

        if len(agent_results) > MAX_LENGTH:
            agent_results = agent_results[:MAX_LENGTH] + "..."
        kpi_prompt_template = self.evaluation_prompts["Graph"]["KPI"]["prompt"]
        # Fill in the placeholders {task} and {agent_results}
        prompt = kpi_prompt_template.format(task=task, agent_results=agent_results)
        # Call the language model
        result = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "user", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
        )[0]
        # Parse the milestones from result.content
        milestones = self.parse_milestones(result.content or "")
        # Update the metrics
        self.metrics["total_milestones"] += len(milestones)
        for milestone in milestones:
            if not isinstance(milestone, dict):
                continue
            # The KPI prompt asks the judge for an "agents" list; keep reading
            # the legacy "contributing_agents" key as well. Looking up only the
            # latter left ``agent_kpis`` empty for every run.
            agents = milestone.get("agents") or milestone.get("contributing_agents") or []
            if isinstance(agents, str):
                agents = [agents]
            for agent_id in agents:
                if agent_id in self.metrics["agent_kpis"]:
                    self.metrics["agent_kpis"][agent_id] += 1
                else:
                    self.metrics["agent_kpis"][agent_id] = 1
        self.logger.debug(f"LLM Response: {result.content}")

    def evaluate_task_research(self, task: str, result: str) -> None:
        """
        Evaluate the final research idea based on innovation, safety, and feasibility.

        Args:
            task (str): The task description.
            result (str): The final research idea.
        """
        # Get the research evaluation prompt
        research_prompt_template = self.evaluation_prompts["research"]["task_evaluation"]["prompt"]
        # Fill in the placeholders {task} and {result}
        prompt = research_prompt_template.format(task=task, result=result)
        # Call the language model
        llm_response = model_prompting(
            llm_model=self.llm,
            messages=[{"role": "user", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None,
        )[0]
        # Parse the ratings from llm_response.content
        ratings = self.parse_research_ratings(llm_response.content or "")
        # Update the metrics
        if ratings:
            self.metrics["task_evaluation"] = ratings
        else:
            self.logger.error("Failed to parse research ratings.")

    def evaluate_task_world(self, task: str, result: str) -> None:
        """
        Evaluate the final world idea based on Effectiveness of Strategies, Progress and Outcome and Interaction Dynamics

        Args:
            task (str): The task description.
            result (str): The final world idea.
        """
        # The seller and the buyer are judged with dedicated prompts; each one
        # only returns ratings for its own side, so both must be queried.
        # (Only the seller prompt used to run, leaving every buyer score at -1.)
        prompts = self.evaluation_prompts["world"]["task_evaluation"]
        task_evaluation: Dict[str, Any] = {}
        for role in ("buyer", "seller"):
            prompt = prompts[f"{role}_prompt"].format(task=task, result=result)
            llm_response = model_prompting(
                llm_model=self.llm,
                messages=[{"role": "user", "content": prompt}],
                return_num=1,
                max_token_num=1024,
                temperature=0.0,
                top_p=None,
                stream=None,
            )[0]
            ratings = self.parse_task_world_evaluation(llm_response.content or "")
            task_evaluation[role] = ratings[role]

        self.metrics["task_evaluation"] = task_evaluation

    def parse_task_world_evaluation(self, llm_response: str) -> Dict[str, Any]:
        """
        Parse the JSON ratings from the LLM response for buyer and seller evaluation.
        If the response is not a valid JSON, return default scores of -1.

        Args:
            llm_response (str): The LLM response containing the ratings in JSON format.

        Returns:
            Dict[str, Any]: A dictionary containing parsed ratings for buyer and seller.
        """
        default_ratings = {
            "buyer": {
                "effectiveness_of_strategies": -1,
                "progress_and_outcome": -1,
                "interaction_dynamics": -1
            },
            "seller": {
                "effectiveness_of_strategies": -1,
                "progress_and_outcome": -1,
                "interaction_dynamics": -1
            }
        }

        try:
            match = re.search(r'\{[\s\S]*\}', llm_response)
            if not match:
                return default_ratings

            json_str = match.group(0)

            ratings = json.loads(json_str)

            if "buyer" not in ratings and "seller" not in ratings:
                return default_ratings

            parsed_ratings = {
                "buyer": {
                    "effectiveness_of_strategies": int(ratings["buyer"].get("effectiveness_of_strategies", -1)),
                    "progress_and_outcome": int(ratings["buyer"].get("progress_and_outcome", -1)),
                    "interaction_dynamics": int(ratings["buyer"].get("interaction_dynamics", -1))
                } if "buyer" in ratings else default_ratings["buyer"],
                "seller": {
                    "effectiveness_of_strategies": int(ratings["seller"].get("effectiveness_of_strategies", -1)),
                    "progress_and_outcome": int(ratings["seller"].get("progress_and_outcome", -1)),
                    "interaction_dynamics": int(ratings["seller"].get("interaction_dynamics", -1))
                } if "seller" in ratings else default_ratings["seller"]
            }

            return parsed_ratings

        except (json.JSONDecodeError, KeyError, ValueError):
            return default_ratings  # 解析失败则返回默认评分

    def evaluate_task_db(self, task: str, result: str, labels: List[str], pred_num: int, root_causes: List[str]) -> None:
        """
        Evaluate the final database idea based on Data Quality, Data Security, and Data Privacy.

        Args:
            task (str): The task description.
            result (str): The final root cause analysis.
            labels (List[str]): The list of root cause labels.
            pred_num (int): The number of predicted root causes.
            root_causes (List[str]): The root cause labels.
        """
        # The final answer is free text and might not follow the requested
        # format, so the raw prediction is always kept for offline re-scoring.
        task_evaluation: Dict[str, Any] = {
            'root_cause': root_causes,
            'predicted': result,
        }
        # Score it right away as well (same procedure as
        # ``scripts/database/batch_eval.py``): ask the judge which root causes
        # were predicted and compare them with the gold labels.
        try:
            prompt = (
                f"{result}\n\n"
                f"From the text above, please identify the {pred_num} predicted root causes of the issue.\n"
                f"Only answer with labels from this list: {', '.join(labels)}.\n\n"
                "Please print each of them in the form they appear in the list, on separate lines, "
                "without any other text."
            )
            response = model_prompting(
                llm_model=self.llm,
                messages=[{"role": "user", "content": prompt}],
                return_num=1,
                max_token_num=512,
                temperature=0.0,
                top_p=None,
                stream=None,
            )[0]
            answer = response.content or ""
            predicted_labels = [label for label in labels if label in answer]
            matches = sum(1 for cause in root_causes if cause in predicted_labels)
            task_evaluation['predicted_labels'] = predicted_labels
            task_evaluation['accuracy'] = matches / len(root_causes) if root_causes else 0.0
        except Exception as e:
            self.logger.error(f"Failed to score the predicted root causes: {e}")
        self.metrics["task_evaluation"] = task_evaluation

    def parse_research_ratings(self, assistant_answer: str) -> Dict[str, int]:
        """
        Parse the research ratings from the assistant's answer.

        Args:
            assistant_answer (str): The assistant's answer containing the ratings.

        Returns:
            Dict[str, int]: The parsed ratings.
        """
        try:
            ratings = extract_json(assistant_answer)
        except ValueError:
            self.logger.error("No valid JSON found in assistant's answer.")
            return {}

        ratings_dict: Dict[str, int] = {}
        for key, value in ratings.items():
            try:
                # Ensure ratings are integers
                ratings_dict[key] = int(value)
            except (TypeError, ValueError):
                self.logger.warning(f"Ignoring non-numeric rating {key!r}: {value!r}")
        return ratings_dict

    def parse_score(self, assistant_answer: str) -> int:
        """
        Parse the score from the assistant's answer based on the strict JSON format requirement.

        Args:
            assistant_answer (str): The assistant's answer containing the score.

        Returns:
            int: The parsed score. Returns 3 (default score) if parsing fails.
        """
        try:
            # Clean the response content
            content = assistant_answer.strip()

            # Remove any markdown code block markers if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            # Find the JSON object
            json_start = content.find('{')
            json_end = content.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                try:
                    rating_data = json.loads(json_str)
                    if isinstance(rating_data, dict) and "rating" in rating_data:
                        score = int(rating_data["rating"])
                        if 1 <= score <= 5:
                            self.logger.debug(f"Successfully parsed score: {score}")
                            return score
                        else:
                            self.logger.warning(f"Score {score} out of valid range (1-5)")
                except json.JSONDecodeError:
                    self.logger.warning("Failed to parse JSON from response")
                except (ValueError, TypeError):
                    self.logger.warning("Invalid score format in JSON")
                except KeyError:
                    self.logger.warning("Missing 'rating' key in JSON response")

            # If JSON parsing fails, try to find a single digit between 1-5
            numbers = re.findall(r'\b[1-5]\b', content)
            if numbers:
                score = int(numbers[0])
                self.logger.debug(f"Found score using regex: {score}")
                return score

            # If all parsing attempts fail, return default score
            self.logger.warning("No valid score found, using default score (3)")
            return 3

        except Exception as e:
            self.logger.error(f"Unexpected error parsing score: {e}")
            return 3

    def finalize(self) -> None:
        """
        Finalize the evaluation, compute final metrics, and log or save the results.
        """
        total_tasks = len(self.metrics["task_completion"])
        tasks_completed = sum(self.metrics["task_completion"])
        success_rate = tasks_completed / total_tasks if total_tasks > 0 else 0

        total_tokens = sum(self.metrics["token_consumption"])
        avg_tokens_per_iteration = total_tokens / total_tasks if total_tasks > 0 else 0

        self.logger.info(f"Task Completion Success Rate: {success_rate * 100:.2f}%")
        self.logger.info(f"Total Token Consumption: {total_tokens}")
        self.logger.info(f"Average Tokens per Iteration: {avg_tokens_per_iteration}")

        # Additional metrics can be computed and logged here

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get the computed metrics.

        Returns:
            Dict[str, Any]: The computed metrics.
        """
        return {
            "success_rate": sum(self.metrics["task_completion"]) / len(self.metrics["task_completion"]) if self.metrics["task_completion"] else 0,
            "total_tokens": sum(self.metrics["token_consumption"]),
            "avg_tokens_per_iteration": sum(self.metrics["token_consumption"]) / len(self.metrics["token_consumption"]) if self.metrics["token_consumption"] else 0
        }

    def parse_milestones(self, assistant_answer: str) -> List[Dict[str, Any]]:
        """
        Parse the milestones from the assistant's answer.

        Args:
            assistant_answer (str): The assistant's answer containing the milestones.

        Returns:
            List[Dict[str, Any]]: The list of milestones.
        """
        try:
            milestones = extract_json(assistant_answer, expect=list)
        except ValueError:
            self.logger.error("Failed to parse JSON from assistant's answer.")
            return []
        return [m for m in milestones if isinstance(m, dict)]

    def parse_code_quality_scores(self, assistant_answer: str) -> Dict[str, int]:
        """
        Parse the code quality scores from the assistant's answer.

        Args:
            assistant_answer (str): The assistant's answer containing the code quality scores.

        Returns:
            Dict[str, int]: The parsed code quality scores.
        """
        try:
            content = assistant_answer.strip()

            json_start = content.find('{')
            json_end = content.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                scores = json.loads(json_str)

                required_keys = {
                    "instruction_following",
                    "executability",
                    "consistency",
                    "quality"
                }

                if all(key in scores for key in required_keys):
                    validated_scores = {}
                    for key in required_keys:
                        try:
                            score = int(scores[key])
                            if 1 <= score <= 5:
                                validated_scores[key] = score
                            else:
                                validated_scores[key] = 1  # 默认最低分
                        except (ValueError, TypeError):
                            validated_scores[key] = 1  # 默认最低分
                    return validated_scores

            self.logger.error("Invalid code quality scores format in response")
            return {
                "instruction_following": 1,
                "executability": 1,
                "consistency": 1,
                "quality": 1
            }

        except Exception as e:
            self.logger.error(f"Error parsing code quality scores: {e}")
            return {
                "instruction_following": 1,
                "executability": 1,
                "consistency": 1,
                "quality": 1
            }

    def evaluate_code_quality(self, task: str, code_result: str) -> None:
        """
        Evaluate the code quality based on stricter criteria.
        """
        try:
            # Score against the task that was actually run. This used to
            # re-read a hard-coded ``coding_config.yaml`` (and a hard-coded
            # workspace path), so every task was judged against the same
            # unrelated description unless that file was rewritten first.
            full_task_description = task

            requirements_start = "1. Implementation requirements:\n"
            requirements_end = "\n\n2. Project structure:"
            if (
                requirements_start in full_task_description
                and requirements_end in full_task_description
            ):
                requirements = full_task_description[
                    full_task_description.find(requirements_start) + len(requirements_start):
                    full_task_description.find(requirements_end)
                ].strip()
            else:
                requirements = "See the task description above."

            solution_content = code_result

            code_quality_prompt_template = """
                    [Context]
                    **Task Description:**
                    {task_description}

                    **Implementation Requirements:**
                    {requirements}

                    **Current Solution:**
                    {solution}

                    [System]
                    This evaluation requires strict scoring and deduction. The scores should not be generous, and deductions should be applied for every issue found.

                    ### **Evaluation Criteria**
                    1. **Instruction-Following:** Does the code fulfill all the requirements of the task? Deduct points for unmet or partially met requirement from the task instructions.
                    2. **Executability:** Is the code syntactically correct and executable? Deduct points for any syntax errors, missing imports, or runtime errors.
                    3. **Consistency:** Is the code consistent in variable naming, formatting, and logic? Deduct points for inconsistent variable naming, formatting issues, or contradictory logic.
                    4. **Quality:** Is the code well-documented, clear, and modular? Deduct points for poor documentation, unclear logic, or lack of modular design.

                    ### **Scoring**
                    - **1 point:** Below Average - Significant issues that need addressing.
                    - **2 points:** Average - Noticeable areas for improvement.
                    - **3 points:** Good - Minor issues or improvements needed.
                    - **4 points:** Excellent - Almost or fully satisfies the criterion.
                    - **5 points:** Legendary - Flawless, perfectly satisfies the criterion, and exceeds expectations.

                    **Do not give the same scores for different criteria, such as 3 for instruction-following, 3 for executability, 3 for consistency, and 3 for quality.**
                    If you give the same scores for the 4 criteria, you have to add or deduct 1 point randomly for one or two criteria.

                    ### **Question**
                    Based on the criteria, evaluate the code and output the scores for each criterion in the following JSON format:
                    {{
                        "instruction_following": score,
                        "executability": score,
                        "consistency": score,
                        "quality": score
                    }}
            """

            # Fill in the template
            prompt = code_quality_prompt_template.format(
                task_description=full_task_description,
                requirements=requirements,
                solution=solution_content
            )

            # Call the LLM
            response = model_prompting(
                llm_model=self.llm,
                messages=[{"role": "user", "content": prompt}],
                return_num=1,
                max_token_num=4096,
                temperature=0.0,
                top_p=None,
                stream=None,
            )[0]

            scores = self.parse_code_quality_scores(response.content or "")

            if scores:
                self.metrics["code_quality"] = scores
                self.logger.info(f"Code quality evaluated strictly: {scores}")
            else:
                self.logger.error("Failed to parse code quality scores.")
                self.metrics["code_quality"] = {
                    "instruction_following": 1,
                    "executability": 1,
                    "consistency": 1,
                    "quality": 1
                }
            self.logger.debug(f"LLM Response: {response.content}")

        except Exception as e:
            self.logger.error(f"Error in code quality evaluation: {e}")
            self.metrics["code_quality"] = {
                "instruction_following": 1,
                "executability": 1,
                "consistency": 1,
                "quality": 1
            }

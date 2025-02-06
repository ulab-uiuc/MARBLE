"""
Evaluator module for tracking metrics and evaluating agent performance.
"""

import json
import re
from typing import Any, Dict, List

from marble.agent import BaseAgent
from marble.environments import BaseEnvironment
from marble.llms.model_prompting import model_prompting
from marble.utils.logger import get_logger


class Evaluator:
    """
    Evaluator class for tracking metrics like task completion success rate and token consumption.
    """
    def __init__(self, metrics_config: Dict[str, Any]):
        """
        Initialize the Evaluator with the specified metrics.

        Args:
            metrics_config (Dict[str, Any]): Configuration for the metrics to track.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.metrics_config = metrics_config
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
        with open('evaluator/evaluator_prompts.json', 'r', encoding='utf-8') as f:
            self.evaluation_prompts = json.load(f)
        self.llm = self.metrics_config.get('evaluate_llm', 'meta-llama/Llama-3.1-70B-Instruct')


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
        result = None
        evaluation_type = "Communication"
        try:
            # Get the communication prompt
            communication_prompt_template = """
Rate the following communication between agents on a scale of 1-5 for each aspect:

Task Context:
{task}

Communication Logs:
{communications}

Evaluation Criteria:
1. Information Exchange (1-5): Was information shared effectively?
2. Clarity (1-5): Were messages clear and understandable?
3. Task Focus (1-5): Did communication stay relevant to the task?

Respond ONLY with three numbers separated by commas. Example:
4,3,5

Your rating:"""
            
            # Limit input length
            task = task[:1000] if task else ""
            communications = communications[:5000] if communications else ""
            
            # Format prompt
            prompt = communication_prompt_template.format(
                task=task,
                communications=communications
            )
            
            # Get LLM response
            result = model_prompting(
                llm_model=self.llm,
                messages=[{"role": "user", "content": prompt}],
                return_num=1,
                max_token_num=512,
                temperature=0.0,
                top_p=None,
                stream=None,
            )[0]
            
            # Parse scores
            scores = [int(x.strip()) for x in result.content.strip().split(',') if x.strip().isdigit()]
            if len(scores) == 3 and all(1 <= s <= 5 for s in scores):
                final_score = round(sum(scores) / 3)  # Average score rounded to nearest integer
                self.metrics["communication_score"].append(final_score)
                self.logger.info(f"[{evaluation_type}] Evaluation scores - Exchange: {scores[0]}, Clarity: {scores[1]}, Focus: {scores[2]} - Final: {final_score}/5")
            else:
                self.logger.warning(f"[{evaluation_type}] Invalid score format, using default score 3/5")
                self.metrics["communication_score"].append(3)
                
        except Exception as e:
            self.logger.error(f"[{evaluation_type}] Error in evaluation: {e}")
            self.metrics["communication_score"].append(3)
        finally:
            if result is not None:
                self.logger.debug(f"[{evaluation_type}] LLM Response: {result.content}")
            else:
                self.logger.warning(f"[{evaluation_type}] No LLM response available")

    def evaluate_planning(self, summary: str, agent_profiles: str, agent_tasks: str, results: str) -> None:
        """
        Evaluate planning and self-coordination among agents and update the planning score.

        Args:
            summary (str): Last round summary.
            agent_profiles (str): Profiles of agents.
            agent_tasks (str): Tasks assigned to agents.
            results (str): Results of the next round.
        """
        result = None
        evaluation_type = "Planning"
        try:
            # Get the planning prompt
            planning_prompt_template = """
Rate the following planning and coordination between agents on a scale of 1-5 for each aspect:

Context:
Summary: {summary}
Agent Profiles: {agent_profiles}
Tasks: {agent_tasks}
Results: {results}

Evaluation Criteria:
1. Role Understanding (1-5): Did agents understand their roles?
2. Task Alignment (1-5): Were tasks properly aligned with goals?
3. Execution (1-5): How well did agents execute their tasks?

Respond ONLY with three numbers separated by commas. Example:
4,3,5

Your rating:"""
            
            # Limit input length
            summary = summary[:2000] if summary else ""
            agent_profiles = agent_profiles[:1000] if agent_profiles else ""
            agent_tasks = agent_tasks[:1000] if agent_tasks else ""
            results = results[:5000] if results else ""
            
            # Format prompt
            prompt = planning_prompt_template.format(
                summary=summary,
                agent_profiles=agent_profiles,
                agent_tasks=agent_tasks,
                results=results
            )
            
            # Get LLM response
            result = model_prompting(
                llm_model=self.llm,
                messages=[{"role": "user", "content": prompt}],
                return_num=1,
                max_token_num=512,
                temperature=0.0,
                top_p=None,
                stream=None,
            )[0]
            
            # Parse scores
            scores = [int(x.strip()) for x in result.content.strip().split(',') if x.strip().isdigit()]
            if len(scores) == 3 and all(1 <= s <= 5 for s in scores):
                final_score = round(sum(scores) / 3)  # Average score rounded to nearest integer
                self.metrics["planning_score"].append(final_score)
                self.logger.info(f"[{evaluation_type}] Evaluation scores - Roles: {scores[0]}, Alignment: {scores[1]}, Execution: {scores[2]} - Final: {final_score}/5")
            else:
                self.logger.warning(f"[{evaluation_type}] Invalid score format, using default score 3/5")
                self.metrics["planning_score"].append(3)
                
        except Exception as e:
            self.logger.error(f"[{evaluation_type}] Error in evaluation: {e}")
            self.metrics["planning_score"].append(3)
        finally:
            if result is not None:
                self.logger.debug(f"[{evaluation_type}] LLM Response: {result.content}")
            else:
                self.logger.warning(f"[{evaluation_type}] No LLM response available")

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
        milestones = self.parse_milestones(result.content)
        # Update the metrics
        self.metrics["total_milestones"] += len(milestones)
        for milestone in milestones:
            agents = milestone.get("contributing_agents", [])
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
        ratings = self.parse_research_ratings(llm_response.content)
        # Update the metrics
        if ratings:
            self.metrics["task_evaluation"] = ratings
        else:
            self.logger.error("Failed to parse research ratings.")
        self.logger.debug(f"LLM Response: {llm_response.content}")

    def parse_research_ratings(self, assistant_answer: str) -> Dict[str, int]:
        """
        Parse the research ratings from the assistant's answer.

        Args:
            assistant_answer (str): The assistant's answer containing the ratings.

        Returns:
            Dict[str, int]: The parsed ratings.
        """
        try:
            # 清理响应内容
            content = assistant_answer.strip()
            
            # 尝试提取JSON部分
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                ratings = json.loads(json_str)
                
                # 验证所有必需的键都存在且值在有效范围内
                required_keys = {"innovation", "safety", "feasibility"}
                if all(key in ratings for key in required_keys):
                    validated_ratings = {}
                    for key in required_keys:
                        try:
                            score = int(ratings[key])
                            if 1 <= score <= 5:
                                validated_ratings[key] = score
                            else:
                                validated_ratings[key] = 3  # 默认中等分数
                        except (ValueError, TypeError):
                            validated_ratings[key] = 3  # 默认中等分数
                    return validated_ratings
                    
            self.logger.error("Invalid ratings format in response")
            return {"innovation": 3, "safety": 3, "feasibility": 3}
            
        except Exception as e:
            self.logger.error(f"Error parsing research ratings: {e}")
            return {"innovation": 3, "safety": 3, "feasibility": 3}

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
            List[Dict[str, Any]]: The list of milestones. Returns empty list if parsing fails.
        """
        try:
            # 清理响应内容
            content = assistant_answer.strip()
            
            # 移除可能的 markdown 代码块标记
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # 尝试提取JSON数组部分
            array_start = content.find('[')
            array_end = content.rfind(']') + 1
            
            if array_start >= 0 and array_end > array_start:
                json_str = content[array_start:array_end]
                try:
                    milestones = json.loads(json_str)
                    
                    # 验证和清理里程碑数据
                    validated_milestones = []
                    for milestone in milestones:
                        if not isinstance(milestone, dict):
                            continue
                            
                        # 检查必需的字段
                        if "milestone" not in milestone or "agents" not in milestone:
                            continue
                            
                        # 验证agents是列表
                        if not isinstance(milestone["agents"], list):
                            continue
                            
                        # 清理和验证数据
                        clean_milestone = {
                            "milestone_content": str(milestone["milestone"])[:100],  # 限制长度
                            "contributing_agents": [
                                str(agent_id) for agent_id in milestone["agents"]
                                if isinstance(agent_id, (str, int))
                            ]
                        }
                        
                        if clean_milestone["contributing_agents"]:  # 只添加有贡献者的里程碑
                            validated_milestones.append(clean_milestone)
                    
                    self.logger.debug(f"Successfully parsed {len(validated_milestones)} milestones")
                    return validated_milestones
                    
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse milestone JSON: {e}")
                    
            self.logger.warning("No valid milestone array found in response")
            return []
            
        except Exception as e:
            self.logger.error(f"Error processing milestones: {e}")
            return []

    def parse_code_quality_scores(self, assistant_answer: str) -> Dict[str, int]:
        """
        Parse the code quality scores from the assistant's answer.

        Args:
            assistant_answer (str): The assistant's answer containing the code quality scores.

        Returns:
            Dict[str, int]: The parsed code quality scores.
        """
        try:
            # 清理响应内容
            content = assistant_answer.strip()
            
            # 尝试提取JSON部分
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                scores = json.loads(json_str)
                
                # 验证所有必需的键都存在且值在有效范围内
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
        
        Args:
            task (str): The task description.
            code_result (str): The code result to be evaluated.
        """
        code_quality_prompt_template = """
                [Context]
                **Task:** {task}

                **Code Result:** {code_result}

                [System]
                This evaluation requires **extremely stringent scoring and strict deduction**. The scores must not be generous, and deductions should be applied strictly for every issue found. 

                ### **Evaluation Criteria**
                1. **Instruction-Following:** Does the code fulfill all the requirements of the task? Deduct 1 point for every unmet or partially met requirement from the task instructions. 
                2. **Executability:** Is the code syntactically correct and executable? Deduct points for any syntax errors, missing imports, or runtime errors. 
                3. **Consistency:** Is the code consistent in variable naming, formatting, and logic? Deduct points for inconsistent variable naming, formatting issues, or contradictory logic. 
                4. **Quality:** Is the code well-documented, clear, and modular? Deduct points for poor documentation, unclear logic, or lack of modular design. 

                ### **Scoring**
                - **1 point:** Below Average - Significant issues that need addressing.
                - **2 points:** Average - Noticeable areas for improvement.
                - **3 points:** Good - Minor issues or improvements needed.

                bonus stage:
                Only code with a base score of **3** can be considered for bonus points.
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
        prompt = code_quality_prompt_template.format(task=task, code_result=code_result)

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

        # 使用新的解析方法替换原来的 parse_research_ratings
        scores = self.parse_code_quality_scores(response.content)

        if scores:
            self.metrics["code_quality"] = scores
            self.logger.info(f"Code quality evaluated strictly: {scores}")
        else:
            self.logger.error("Failed to parse code quality scores.")
            # 设置默认的最低分数
            self.metrics["code_quality"] = {
                "instruction_following": 1,
                "executability": 1,
                "consistency": 1,
                "quality": 1
            }
        self.logger.debug(f"LLM Response: {response.content}")



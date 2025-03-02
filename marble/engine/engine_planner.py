# marble/engine/engine_planner.py

"""
Engine Planner module responsible for task assignment and scheduling.
"""

import json
import os
from typing import Any, Dict, List

from litellm import token_counter
from litellm.types.utils import Message
from ruamel.yaml import YAML

from marble.graph.agent_graph import AgentGraph
from marble.llms.model_prompting import model_prompting
from marble.utils.logger import get_logger


class EnginePlanner:
    """
    The EnginePlanner class handles task assignment and scheduling for agents.
    """

    def __init__(self, agent_graph: AgentGraph, memory: Any, config: Dict[str, Any], task:str, model:str="gpt-3.5-turbo"):
        """
        Initialize the EnginePlanner.

        Args:
            agent_graph (AgentGraph): The graph of agents.
            memory (Any): Shared memory instance.
            config (Dict[str, Any]): Configuration parameters.
        """
        self.agent_graph = agent_graph
        self.memory = memory
        self.logger = get_logger(self.__class__.__name__)
        self.config = config
        self.current_progress = config.get('initial_progress', '')
        self.task = task
        self.model = model
        self.token_usage = 0
        self.logger.info("EnginePlanner initialized.")

    def create_prompt(self) -> str:
        """
        Create a prompt for the LLM to assign tasks to agents.

        Returns:
            str: The prompt string.
        """
        agent_profiles = self.agent_graph.get_agent_profiles()
        prompt = (
            "You are an orchestrator assigning tasks to a group of agents based on their profiles and current progress and task description.\n\n"
            f"Task Description:\n{self.task}\n\n"
            f"Current Progress: {self.current_progress}\n\n"
            "Agent Profiles:\n"
        )
        for agent_id, profile in agent_profiles.items():
            prompt += f"- Agent ID: {agent_id}\n"
            prompt += f"  Relationships: {profile['relationships']}\n"
            prompt += f"  Profile: {profile['profile']}\n"

        prompt += (
            "Based on the current progress and agent profiles, assign the next task to each agent that needs to perform an action.\n"
            "Provide the assignments in the following JSON format:\n\n"
            "{\n"
            '  "tasks": {\n'
            '    "agent1": "...", \n'
            '    "agent2": "...", \n'
            '    // Add more agents as needed\n'
            '  },\n'
            '  "continue": true // Set to false if the task is completed\n'
            "}\n\n"
            "If an agent does not need to be assigned a task, you can omit it from the 'tasks' section.\n"
        )
        self.logger.debug(f"Created prompt for task assignment:\n{prompt}")
        return prompt

    def assign_tasks(self) -> Dict[str, Any]:
        """
        Assign tasks to agents by interacting with the LLM.

        Returns:
            Dict[str, Any]: The task assignments and continuation flag.
        """
        prompt = self.create_prompt()
        system_message = (
            "You are a task assignment system for multiple AI agents based on their profiles and current progress.\n"
            "Your task is to analyze the current state and assign the next task to each agent that requires an action.\n"
            "Don't ask agents to assign tasks to other agents.\n"
        )
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
        response = model_prompting(
            llm_model=self.model,
            messages=messages,
            return_num=1,
            max_token_num=2048,
            temperature=0.7,
            top_p=1.0
        )
        messages =[{"role": "system", "content": system_message}, {"role": "user", "content": prompt}, {"role": "assistant", "content": response[0].content}]
        self.token_usage += token_counter(model=self.model, messages=messages)
        try:
            assignment:Dict[str, Any] = json.loads(response[0].content if response[0].content else "")
            self.logger.debug(f"Received task assignment: {assignment}")
            return assignment
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            return {"tasks": {}, "continue": False}

    def update_progress(self, summary: str) -> None:
        """
        Update the current progress based on the agents' outputs.

        Args:
            summary (str): Summary of the latest iteration.
        """
        self.current_progress += f"\n{summary}"
        self.logger.debug(f"Updated progress: {self.current_progress}")

    def summarize_output(self, summary:str, task:str, output_format:str) -> Message:
        """
        Summarize the output of the agents.

        Args:
            summary (str): Summary of the latest iteration.

        Returns:
            str: The summarized output.
        """
        response = model_prompting(
            llm_model=self.model,
            messages=[{"role": "user", "content": f"Summarize the output of the agents for the task: {task}\n\nNow here is some result of thr agent: {summary}, please summarize it. You should follow the use of the following format: {output_format}"}],
            return_num=1,
            max_token_num=2048,
            temperature=0.0,
            top_p=None,
            stream=None
        )[0]
        self.token_usage += token_counter(model=self.model, messages=[{"role": "user", "content": f"Summarize the output of the agents for the task: {task}\n\nNow here is some result of thr agent: {summary}, please summarize it. You should follow the use of the following format: {output_format}"}, {"role": "assistant", "content": response.content}])
        return response

    def decide_next_step(self, agents_results: List[Dict[str, Any]]) -> bool:
        """
        Decide whether to continue or terminate the simulation based on agents' results.

        Args:
            agents_results (Dict[str, Any]): The results from all agents.

        Returns:
            bool: True to continue, False to terminate.
        """
        try:
            # 读取配置文件
            config_path = "/opt/dlami/nvme/zhe/MARBLE/marble/configs/coding_config/coding_config.yaml"
            if not os.path.exists(config_path):
                self.logger.error("Config file not found")
                return False

            yaml = YAML()
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.load(f)

            full_task_description = config['task']['content']
            
            # 提取requirements部分
            requirements_start = "1. Implementation requirements:\n"
            requirements_end = "\n\n2. Project structure:"
            requirements = full_task_description[
                full_task_description.find(requirements_start) + len(requirements_start):
                full_task_description.find(requirements_end)
            ].strip()

            # 读取solution.py
            solution_path = "/opt/dlami/nvme/zhe/MARBLE/marble/workspace/solution.py"
            solution_content = ""
            if os.path.exists(solution_path):
                with open(solution_path, 'r', encoding='utf-8') as f:
                    solution_content = f.read()

            prompt = (
                "You are a task completion validator. Determine if the task is completed based on the following information:\n\n"
                f"Task Description:\n{full_task_description}\n\n"
                f"Implementation Requirements:\n{requirements}\n\n"
                f"Current Solution:\n{solution_content}\n\n"
                "Agents' Results:\n"
            )
            
            for result in agents_results:
                prompt += f"- {result}\n"

            prompt += (
                "\nYou must respond with a valid JSON object containing a single key 'continue' set to true or false.\n"
                "Consider:\n"
                "1. Does the solution meet all implementation requirements?\n"
                "2. Are there any critical issues in the agents' results?\n"
                "3. Is the code complete and functional?\n\n"
                "Some times the results will have a key call success and its value is true, but this does not mean the task is completed, "
                "This only means the tool execute successfully.\n"
                "You should analyze the results and decide whether the task is completed or not.\n"
                "Your response must be a valid JSON object in exactly this format:\n"
                "{\n"
                '  "continue": true\n'
                "}\n"
                "If you cannot provide a JSON response, simply respond with 'true' or 'false' to indicate whether to continue.\n"
                "Do not include any additional text, explanation, or formatting."
            )

            messages = [{"role": "system", "content": prompt}]
            response = model_prompting(
                llm_model=self.model,
                messages=messages,
                return_num=1,
                max_token_num=2048,
                temperature=0.3,
                top_p=1.0
            )
            
            messages = [{"role": "system", "content": prompt}, {"role": "assistant", "content": response[0].content}]
            self.token_usage += token_counter(model=self.model, messages=messages)
            
            # 清理响应内容
            content = response[0].content.strip() if response[0].content else ""
            
            # 尝试提取JSON部分
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                try:
                    decision = json.loads(json_str)
                    self.logger.debug(f"Received continuation decision: {decision}")
                    bool_decision: bool = decision.get("continue", False)
                    return bool_decision
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse extracted JSON: {e}, falling back to keyword analysis")
            else:
                self.logger.warning("No valid JSON found in response, falling back to keyword analysis")
            
            # 关键词分析作为备选方案
            continue_keywords = {'true', 'yes', 'continue', 'True', 'TRUE', 'Yes', 'YES'}
            stop_keywords = {'false', 'no', 'stop', 'False', 'FALSE', 'No', 'NO', 'completed', 'done', 'finished'}
            
            # 转换内容为小写进行比较
            content_lower = content.lower()
            
            # 检查是否包含继续关键词
            for keyword in continue_keywords:
                if keyword.lower() in content_lower:
                    self.logger.info(f"Found continue keyword: {keyword}")
                    return True
                    
            # 检查是否包含停止关键词
            for keyword in stop_keywords:
                if keyword.lower() in content_lower:
                    self.logger.info(f"Found stop keyword: {keyword}")
                    return False
                    
            # 如果没有找到任何关键词，返回默认值（结束）
            self.logger.warning("No keywords found in response, defaulting to terminate")
            return False
            
        except Exception as e:
            self.logger.error(f"Error processing decision response: {e}, defaulting to terminate")
            return False

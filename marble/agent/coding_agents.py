from typing import Any, Dict, Union
from marble.agent.base_agent import BaseAgent
from marble.llms.model_prompting import model_prompting
from marble.memory import BaseMemory, SharedMemory
from marble.environments import BaseEnvironment, CodingEnvironment


class AnalystAgent(BaseAgent):
    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: CodingEnvironment, shared_memory: Union[SharedMemory, None] = None):
        super().__init__(config, env, shared_memory)
        self.env = env

    def act(self, task: str) -> Any:
        self.logger.info(f"Analyst agent analyzing task: {task}")
        
        result = model_prompting(
            llm_model="gpt-4",
            messages=[{
                "role": "system",
                "content": """You are a senior software analyst. Analyze the given coding task and provide clear implementation suggestions.
                Output should be in markdown format with following sections:
                - Problem Analysis
                - Function Design
                - Implementation Steps"""
            }, {
                "role": "user",
                "content": task
            }],
            return_num=1,
            max_token_num=1024,
            temperature=0.7
        )[0]
        
        analysis = result.content if result.content else ""
        
        return self.env.apply_action(
            self.agent_id,
            "analyze_task",
            {"task": task, "analysis": analysis}
        )

class CoderAgent(BaseAgent):
    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: CodingEnvironment, shared_memory: Union[SharedMemory, None] = None):
        super().__init__(config, env, shared_memory)
        self.env = env

    def act(self, task: str) -> Any:
        self.logger.info(f"Coder agent implementing solution for: {task}")
        
        current_state = self.env.get_state()
        analysis = current_state.get("task_analysis", "")
        
        # First get the implementation code
        code_result = model_prompting(
            llm_model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You are an expert programmer. Implement the solution based on the analysis provided. Return ONLY the implementation code, no explanations or markdown."
            }, {
                "role": "user",
                "content": f"Task: {task}\nAnalysis: {analysis}"
            }],
            return_num=1,
            max_token_num=1024,
            temperature=0.7
        )[0]
        
        # Then get the documentation
        doc_result = model_prompting(
            llm_model="gpt-4",
            messages=[{
                "role": "system",
                "content": """Create a README.md documentation for the implementation. Include:
                - Function/Class Overview
                - Parameters
                - Return Value
                - Usage Examples
                - Implementation Notes"""
            }, {
                "role": "user",
                "content": f"Task: {task}\nImplementation: {code_result.content}"
            }],
            return_num=1,
            max_token_num=1024,
            temperature=0.7
        )[0]
        
        if not code_result.content or not doc_result.content:
            return {"success": False, "error": "Failed to generate content"}
            
        return self.env.apply_action(
            self.agent_id,
            "implement_code",
            {
                "code": code_result.content,
                "documentation": doc_result.content
            }
        )
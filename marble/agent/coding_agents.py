from typing import Any, Dict, List, Optional, Tuple, Union
from marble.agent.base_agent import BaseAgent
from marble.llms.model_prompting import model_prompting
from marble.memory import BaseMemory, SharedMemory
from marble.environments import BaseEnvironment, CodingEnvironment
from litellm import token_counter

class AnalystAgent(BaseAgent):
    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: CodingEnvironment, shared_memory: Union[SharedMemory, None] = None):
        super().__init__(config, env, shared_memory)
        self.env = env
        # 更新系统消息以包含分析师角色
        self.system_message += "\nAs a senior software analyst, you analyze coding tasks and provide clear implementation suggestions."

    def act(self, task: str) -> Any:
        self.logger.info(f"Analyst agent analyzing task: {task}")
        self.task_history.append(task)
        
        result = model_prompting(
            llm_model=self.llm,
            messages=[{
                "role": "system",
                "content": """You are a senior software analyst. Analyze the given coding task and provide clear implementation suggestions.
                Output should be in markdown format with following sections:
                - Problem Analysis
                - Function Signature Design
                - Implementation Method"""
            }, {
                "role": "user",
                "content": task
            }],
            return_num=1,
            max_token_num=1024,
            temperature=0.7
        )[0]
        
        analysis = result.content if result.content else ""
        
        # 计算token使用量
        messages = [{"role": "system", "content": self.system_message}, {"role": "user", "content": task}, {"role": "assistant", "content": analysis}]
        self.token_usage += token_counter(model=self.llm, messages=messages)
        
        # 更新内存
        self.memory.update(self.agent_id, {
            "type": "analysis",
            "task": task,
            "analysis": analysis
        })
        
        return self.env.apply_action(
            self.agent_id,
            "analyze_task",
            {"task": task, "analysis": analysis}
        )

    def plan_next_phase(self, analysis_result: Any) -> Tuple[Optional[str], Optional[str]]:
        """规划下一个阶段，通常是将任务传递给CoderAgent"""
        return self.plan_next_agent(analysis_result, self.agent_graph.agents)

class CoderAgent(BaseAgent):
    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: CodingEnvironment, shared_memory: Union[SharedMemory, None] = None):
        super().__init__(config, env, shared_memory)
        self.env = env
        self.system_message += "\nAs an expert programmer, you implement solutions based on provided analysis."

    def act(self, task: str) -> Any:
        self.logger.info(f"Coder agent implementing solution for: {task}")
        self.task_history.append(task)
        
        current_state = self.env.get_state()
        analysis = current_state.get("task_analysis", "")
        
        code_result = model_prompting(
            llm_model=self.llm,
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
        
        doc_result = model_prompting(
            llm_model=self.llm,
            messages=[{
                "role": "system",
                "content": """Create a README.md documentation for the implementation. Include:
                - Implementation Overview
                - Function Signature
                - Parameters
                - Return Value"""
            }, {
                "role": "user",
                "content": f"Task: {task}\nImplementation: {code_result.content}"
            }],
            return_num=1,
            max_token_num=1024,
            temperature=0.7
        )[0]
        
        # 计算token使用量
        for result in [code_result, doc_result]:
            messages = [{"role": "system", "content": self.system_message}, {"role": "user", "content": task}, {"role": "assistant", "content": result.content if result.content else ""}]
            self.token_usage += token_counter(model=self.llm, messages=messages)
        
        if not code_result.content or not doc_result.content:
            return {"success": False, "error": "Failed to generate content"}
            
        # 更新内存
        self.memory.update(self.agent_id, {
            "type": "implementation",
            "task": task,
            "code": code_result.content,
            "documentation": doc_result.content
        })
            
        return self.env.apply_action(
            self.agent_id,
            "implement_code",
            {
                "code": code_result.content,
                "documentation": doc_result.content
            }
        )

class TestorAgent(BaseAgent):
    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], env: CodingEnvironment, shared_memory: Union[SharedMemory, None] = None):
        super().__init__(config, env, shared_memory)
        self.env = env
        self.system_message += "\nAs a test engineer, you create and implement comprehensive test cases."

    def analyze_test_cases(self, task: str) -> Any:
        self.logger.info(f"Testor agent analyzing test cases for: {task}")
        
        current_state = self.env.get_state()
        implementation_code = current_state.get("implementation_code", "")
        
        test_analysis_result = model_prompting(
            llm_model=self.llm,
            messages=[{
                "role": "system",
                "content": """You are a test analyst. Analyze the implementation and provide test strategy.
                Include:
                - Test Cases Categories
                - Edge Cases
                - Performance Test Cases
                - Error Handling Cases"""
            }, {
                "role": "user",
                "content": f"Implementation:\n{implementation_code}"
            }],
            return_num=1,
            max_token_num=1024,
            temperature=0.7
        )[0]
        
        # 计算token使用量
        messages = [{"role": "system", "content": self.system_message}, {"role": "user", "content": task}, {"role": "assistant", "content": test_analysis_result.content if test_analysis_result.content else ""}]
        self.token_usage += token_counter(model=self.llm, messages=messages)
        
        if not test_analysis_result.content:
            return {"success": False, "error": "Failed to generate test analysis"}
            
        # 更新内存
        self.memory.update(self.agent_id, {
            "type": "test_analysis",
            "task": task,
            "test_analysis": test_analysis_result.content
        })
            
        return self.env.apply_action(
            self.agent_id,
            "update_analysis_with_test",
            {"test_analysis": test_analysis_result.content}
        )

    def act(self, task: str) -> Any:
        self.logger.info(f"Testor agent implementing tests for: {task}")
        self.task_history.append(task)
        
        analysis_result = self.analyze_test_cases(task)
        if not analysis_result.get("success", False):
            return analysis_result
        
        current_state = self.env.get_state()
        implementation_code = current_state.get("implementation_code", "")
        task_analysis = current_state.get("task_analysis", "")
        test_analysis = current_state.get("test_analysis", "")
            
        test_result = model_prompting(
            llm_model=self.llm,
            messages=[{
                "role": "system",
                "content": """You are a test engineer. Implement comprehensive test cases based on the analysis and implementation.
                Include unit tests for all main functionalities and edge cases. Use pytest framework."""
            }, {
                "role": "user",
                "content": f"Task: {task}\nImplementation:\n{implementation_code}\nAnalysis:\n{task_analysis}\nTest Analysis:\n{test_analysis}"
            }],
            return_num=1,
            max_token_num=2048,
            temperature=0.7
        )[0]
        
        # 计算token使用量
        messages = [{"role": "system", "content": self.system_message}, {"role": "user", "content": task}, {"role": "assistant", "content": test_result.content if test_result.content else ""}]
        self.token_usage += token_counter(model=self.llm, messages=messages)
        
        if not test_result.content:
            return {"success": False, "error": "Failed to generate test content"}
        
        # 更新内存
        self.memory.update(self.agent_id, {
            "type": "test_implementation",
            "task": task,
            "test_code": test_result.content
        })
            
        return self.env.apply_action(
            self.agent_id,
            "implement_test",
            {"test_code": test_result.content}
        )
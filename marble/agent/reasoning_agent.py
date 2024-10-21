import yaml
from typing import Any, Dict, Union
from marble.agent import BaseAgent
from marble.llms import OpenAILLM
from marble.memory.base_memory import BaseMemory

class ReasoningAgent(BaseAgent):
    """
    Agent that uses reasoning strategies (Chain-of-Thought, ReAct, Reflexion, etc.).
    """

    def __init__(self, config: Dict[str, Union[Any, Dict[str, Any]]], prompt_config_path: str):
        """
        Initialize the ReasoningAgent with the desired reasoning strategy.

        Args:
            config (dict): Configuration for the reasoning agent.
            prompt_config_path (str): Path to the prompt configuration file.
        """
        super().__init__(config)

        llm_config = config.get("llm")
        assert llm_config is not None
        llm_type = llm_config.get("type")
        if llm_type == "OpenAI":
            self.llm = OpenAILLM(llm_config)
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
        
        self.memory = BaseMemory()
        self.reasoning_strategy = config.get("reasoning_strategy", "default")
        self.prompts = self._load_prompt_config(prompt_config_path)

    def _load_prompt_config(self, prompt_config_path: str) -> Dict[str, Any]:
        """
        Load the prompt configuration from the specified YAML file.

        Args:
            prompt_config_path (str): Path to the prompt configuration YAML file.

        Returns:
            dict: Loaded prompt templates.
        """
        try:
            with open(prompt_config_path, 'r') as file:
                prompt_config = yaml.safe_load(file)
            return prompt_config['prompts']
        except FileNotFoundError:
            raise ValueError(f"Prompt configuration file not found: {prompt_config_path}")
        except KeyError:
            raise ValueError(f"Invalid format in prompt configuration file: {prompt_config_path}")

    def perceive(self, state: Any) -> Any:
        """
        Process perception with cognitive abilities.

        Args:
            state (Any): The current state of the environment.

        Returns:
            Any: Processed perception data.
        """
        self.memory.update(self.agent_id, state)
        perception = self.memory.retrieve_latest()
        return perception

    def act(self, perception: Any) -> Any:
        """
        Decide on an action using the LLM and the configured reasoning strategy.

        Args:
            perception (Any): Processed perception data.

        Returns:
            Any: The action decided by the agent.
        """
        prompt = self._generate_prompt(perception)
        action = self.llm.generate_text(prompt)
        return action

    def _generate_prompt(self, perception: Any) -> str:
        """
        Generate a prompt for the LLM based on the selected reasoning strategy.

        Args:
            perception (Any): Perception data.

        Returns:
            str: The generated prompt.
        """
        if self.reasoning_strategy == "cot":
            prompt_template = self.prompts["cot"]
        elif self.reasoning_strategy == "react":
            prompt_template = self.prompts["react"]
        elif self.reasoning_strategy == "reflexion":
            prompt_template = self.prompts["reflexion"]
        else:
            prompt_template = self.prompts["default"]
        
        return prompt_template.format(perception=perception)

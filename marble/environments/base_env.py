"""
Base environment module.
"""

from typing import Any, Callable, Dict, List, Union


class BaseEnvironment:
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize the environment.

        Args:
            name (str): The name of the environment.
            config (Dict[str, Any]): Configuration for the environment.
        """
        self.name = name
        self.agents: List[Any] = []
        self.state: Dict[str, Any] = {}
        self._action_handlers: Dict[str, Callable[..., Dict[str, Any]]] = {} # private to avoid direct calls from outside
        self.action_handler_descriptions: Dict[str, Any] = {} # in openai format
        self.done = False
        self.description: str = config.get("description", "")
        self.task_description: str = config.get("task_description", "")
        self.ground_truth: str = config.get("ground_truth", "")
        self.max_iterations: int = config.get("max_iterations", 10)
        self.current_iteration: int = 0
        # Initialize the state with the task description
        self.state['task_description'] = self.task_description

    def is_done(self) -> bool:
        return self.done

    def is_task_completed(self) -> bool:
        # Compare the agent's last action or the state to the ground truth
        # For simplicity, let's assume the state contains 'last_action_result'
        last_action_result = self.state.get('last_action_result', '')
        return self._compare_to_ground_truth(last_action_result, self.ground_truth)

    def _compare_to_ground_truth(self, result: str, ground_truth: str) -> bool:
        # Implement a method to compare result to ground truth
        # For simplicity, check if result matches ground_truth exactly
        if result:
            import pdb; pdb.set_trace()

            return result.strip().lower() == ground_truth.strip().lower()
        else:
            return False

    def get_description(self) -> str:
        return self.description

    def register_action(self, action_name: str, handler: Callable[..., Dict[str, Any]], description: Dict[str, Any]) -> None:
        """
        Register an action handler for the environment.

        Args:
            action_name (str): The name of the action.
            description (dict): Discription of action (in openai "function calling" format).
            handler (Callable): The handler function for the action.
        """
        self._action_handlers[action_name] = handler
        self.action_handler_descriptions[action_name] = description

    def apply_action(self, agent_id: Union[str, None], action_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an action in the environment.

        Args:
            agent_id (str): The ID of the agent performing the action.
            action_name (str): The action to execute. Action name is used to retrieve the handler.
            arguments (dict): Arguments for the action handler.
        """
        # Execution
        action_result = self._action_handlers[action_name](**arguments)

        # Update the state with the action result
        self.state['last_action_result'] = action_result

        # Increment iteration count
        self.current_iteration += 1
        if self.current_iteration >= self.max_iterations:
            self.done = True

        return action_result

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current environment state.

        Returns:
            Dict[str, Any]: The current environment state.
        """
        return self.state.copy()

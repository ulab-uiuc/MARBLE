from typing import List, Dict, Union
from litellm.types.utils import Message
from collections import deque

from marble.memory.base_memory import BaseMemory
from marble.llms.model_prompting import model_prompting


class ShortTermMemory(BaseMemory):
    """
    Short term momery class that automatically summarizes old information.
    """

    def __init__(self, memory_limit: int = 10) -> None:
        """
        Initialize the memory module.

        Args:
            memory_limit (int): Maximum length of the memory.
        """
        super().__init__()
        self.memory_limit: int = memory_limit
        self.storage: deque = deque(maxlen=self.memory_limit)

    def update(self, key: str, information: Dict[str, Union[str, Message]]) -> None:
        """
        Update memory with new information.

        Args:
            key (str): Only here to keep the signature consistent with SharedMemory.
            information (Dict[str, Union[str, Message]]): Information to store.
        """
        if len(self.storage) == self.memory_limit:
            oldest_event = self.storage.popleft()
            sec_oldest_event = self.storage.popleft()
            summary = self.summarize([oldest_event, sec_oldest_event])
            self.storage.appendleft({
                "type": "old_memory_summary",
                "result": summary
            })
        self.storage.append(information)

    def summarize(self, memory: List[Dict[str, Union[str, Message]]] = None) -> Message:
        """
        Summarize the input memory.

        Args:
            memory (List[Dict[str, Union[str, Message]]]): Input memory to be summarized.

        Returns:
            Message: Summary of the input memory.
        """
        if not memory:
            memory = self.storage

        prompt = (
            "You are a helpful assistant that can concisely summarize the following json format content which is listed in temporally sequential order:\n"
        )
        for idx, information in enumerate(memory):
            prompt += f"{idx}. {str(information)}\n"

        summary = model_prompting(
            llm_model="gpt-3.5-turbo",
            messages=[{"role":"system", "content": prompt}],
            return_num=1,
            max_token_num=512,
            temperature=0.0,
            top_p=None,
            stream=None
        )[0]
        return summary
    
    def retrieve_latest(self) -> Dict[str, Union[str, Message]]:
        """
        Retrieve the most recent information from memory.

        Returns:
            Dict[str, Union[str, Message]]: The most recently stored information, or None if empty.
        """
        return self.storage[-1] if self.storage else None

    def retrieve_all(self) -> List[Dict[str, Union[str, Message]]]:
        """
        Retrieve all stored information.

        Returns:
            List[Dict[str, Union[str, Message]]]: All stored information.
        """
        return list(self.storage)
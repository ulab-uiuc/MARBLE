import warnings
from typing import Any, Dict, List, Union

import numpy as np
from litellm.types.utils import Message
from numpy.typing import NDArray
from sklearn.metrics.pairwise import cosine_similarity

from marble.llms.model_prompting import model_prompting
from marble.llms.text_embedding import text_embedding
from marble.memory.base_memory import BaseMemory


class LongTermMemory(BaseMemory):
    """
    Long term momery class that implements memory retrieval.
    """


    def __init__(self) -> None:
        """
        Initialize the memory module.
        """
        super().__init__()
        self.storage: List[tuple[Any, Any]] = []

    def update(self, key: str, information: Dict[str, Any]) -> None:
        """
        Update memory with new information.

        Args:
            key (str): Only here to keep the signature consistent with SharedMemory.
            information (Dict[str, Union[str, Message]]): Information to store.
        """
        embedding = text_embedding(
            model="text-embedding-3-small",
            input=str(information),
        )
        embedding_array:NDArray[Any] = np.array(embedding)
        self.storage.append((information, embedding_array))

    def retrieve_latest(self) -> Any:
        """
        Retrieve the most recent information from memory.

        Returns:
            Dict[str, Union[str, Message]]: The most recently stored information, or None if empty.
        """
        return self.storage[-1][0] if self.storage else None

    def retrieve_most_relevant(self, information: Dict[str, Union[str, Message]], n: int = 1, summarize: bool = False) -> Any:
        """
        Retrieve the most relevant information from memory.

        Args:
            information (Dict[str, Union[str, Message]]): Query for retrieval.
            n (int): Number of retrieved information.
            summarize (bool): Whether to summarize the retrieved information.

        Returns:
            Union[List[Dict[str, Union[str, Message]]], Message]: The most information most relevant to the given information, or None if empty.
        """
        if not self.storage:
            return None
        embedding = text_embedding(
            model="text-embedding-3-small",
            input=str(information),
        )
        embedding_array:NDArray[Any] = np.array(embedding)
        retrieval_scores = []
        for stored_information in self.storage:
            similarity = cosine_similarity(stored_information[1].reshape((1, -1)), embedding_array.reshape((1, -1)))[0][0]
            retrieval_scores.append((stored_information[0], similarity))
        retrieval_scores = sorted(retrieval_scores, key=lambda score: score[1], reverse=True)[:n]
        if summarize:
            summary = self.summarize([scored_information[0] for scored_information in retrieval_scores])
            return summary
        else:
            return [information[0] for information in retrieval_scores]

    def summarize(self, memory: List[Dict[str, Union[str, Message]]]) -> Message:
        """
        Summarize the input memory.

        Args:
            memory (List[Dict[str, Union[str, Message]]]): Input memory to be summarized.

        Returns:
            Message: Summary of the input memory.
        """
        if not memory:
            warnings.warn("You are tring to summarize a long-term memory! This may cost a lot of tokens!")
            memory = [information[0] for information in self.storage]

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

    def retrieve_all(self) -> List[Dict[str, Union[str, Message]]]:
        """
        Retrieve all stored information.

        Returns:
            List[Dict[str, Union[str, Message]]]: All stored information.
        """
        return [information[0] for information in self.storage]

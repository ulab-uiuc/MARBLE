import unittest
from collections import deque
from litellm.types.utils import Message

from marble.memory.short_term_memory import ShortTermMemory

class TestLongTermMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.memory = ShortTermMemory(memory_limit=2)

    def test_update(self) -> None:
        result_1 = Message(content="It is cold today.", role="assistant")
        self.memory.update(key="key", information={
            "type": "action_response",
            "result": result_1
        })
        result_2 = Message(content="I want to sleep.", role="assistant")
        self.memory.update(key="key", information={
            "type": "action_response",
            "result": result_2
        })
        self.assertIsInstance(self.memory.storage, deque)
        self.assertIsInstance(self.memory.storage[0], dict)
        self.assertEqual(len(self.memory.storage), 2)

        result_3 = Message(content="I am so hungry.", role="assistant")
        self.memory.update(key="key", information={
            "type": "action_response",
            "result": result_3
        })
        self.assertIsInstance(self.memory.storage, deque)
        self.assertIsInstance(self.memory.storage[0], dict)
        self.assertEqual(len(self.memory.storage), 2)


    def test_retrieve_latest(self) -> None:
        result_1 = Message(content="It is cold today.", role="assistant")
        information_1 = {
            "type": "action_response",
            "result": result_1
        }
        self.memory.update(key="key", information=information_1)
        true_latest_information = information_1
        latest_information = self.memory.retrieve_latest()
        self.assertIs(latest_information, true_latest_information)

        result_2 = Message(content="I want to sleep.", role="assistant")
        information_2 = {
            "type": "action_response",
            "result": result_2
        }
        self.memory.update(key="key", information=information_2)
        result_3 = Message(content="I am so hungry.", role="assistant")
        information_3 = {
            "type": "action_response",
            "result": result_3
        }
        self.memory.update(key="key", information=information_3)
        true_latest_information = information_3
        latest_information = self.memory.retrieve_latest()
        self.assertIs(latest_information, true_latest_information)

    def test_retrieve_all(self) -> None:
        result_1 = Message(content="It is cold today.", role="assistant")
        information_1 = {
            "type": "action_response",
            "result": result_1
        }
        self.memory.update(key="key", information=information_1)
        result_2 = Message(content="I want to sleep.", role="assistant")
        information_2 = {
            "type": "action_response",
            "result": result_2
        }
        self.memory.update(key="key", information=information_2)
        all_information = self.memory.retrieve_all()
        self.assertIn(information_1, all_information)
        self.assertIn(information_2, all_information)
        self.assertEqual(len(all_information), 2)

        result_3 = Message(content="I am so hungry.", role="assistant")
        information_3 = {
            "type": "action_response",
            "result": result_3
        }
        self.memory.update(key="key", information=information_3)
        all_information = self.memory.retrieve_all()
        self.assertNotIn(information_1, all_information)
        self.assertNotIn(information_2, all_information)
        self.assertIn(information_3, all_information)
        self.assertEqual(len(all_information), 2)

if __name__ == "__main__":
    unittest.main()
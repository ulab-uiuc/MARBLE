"""
Tests for the Engine and AgentGraph.
"""

import unittest

from marble.configs import Config
from marble.engine.engine import Engine


class TestEngine(unittest.TestCase):
    """
    Test cases for the Engine class.
    """

    def test_hierarchical_execution(self) -> None:
        """
        Test the hierarchical execution mode in the Engine.
        """
        config_data = {
            'environment': {
                'type': 'Web',
                'parameters': {}
            },
            'agents': [
                {'agent_id': 'agent_root', 'type': 'ReasoningAgent', 'llm': {'type': 'OpenAI', 'api_key': 'sk-14EtoJxEXbFGnniZfACxAVujYGXED7n6wuDRV0vEkoq6iEW1', 'api_base': 'https://api.chatanywhere.cn/v1', 'model_name': 'openai/gpt-4o-mini'}},
                {'agent_id': 'agent_child1', 'type': 'ReasoningAgent', 'llm': {'type': 'OpenAI', 'api_key': 'sk-14EtoJxEXbFGnniZfACxAVujYGXED7n6wuDRV0vEkoq6iEW1', 'api_base': 'https://api.chatanywhere.cn/v1', 'model_name': 'openai/gpt-4o-mini'}},
                {'agent_id': 'agent_child2', 'type': 'ReasoningAgent', 'llm': {'type': 'OpenAI',  'api_key': 'sk-14EtoJxEXbFGnniZfACxAVujYGXED7n6wuDRV0vEkoq6iEW1', 'api_base': 'https://api.chatanywhere.cn/v1', 'model_name': 'openai/gpt-4o-mini'}}
            ],
            'graph': {
                'execution_mode': 'hierarchical',
                'structure': {
                    'agent_root': ['agent_child1', 'agent_child2']
                }
            },
            'memory': {
                'type': 'SharedMemory'
            },
            'metrics': {}
        }

        config = Config(config_data)
        engine = Engine(config)
        assert engine is not None
        # engine.start()

        # Assertions can be added here to check the state after execution
        self.assertTrue(True)  # Placeholder assertion

if __name__ == '__main__':
    unittest.main()

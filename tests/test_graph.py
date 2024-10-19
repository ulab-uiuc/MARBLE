import unittest

from typing import List, Dict, Any

from marble.agent.base_agent import BaseAgent
from marble.environments import BaseEnvironment
from marble.graph.agent_graph import AgentGraph
from marble.memory import SharedMemory


class TestAgentGraph(unittest.TestCase):
    def setUp(self)->None:
        self.placebo_env = BaseEnvironment(name="foobar", config={})
        # Initialize shared memory
        self.shared_memory = SharedMemory()

        # Define agent configurations
        self.agent_configs: List[Dict[str, Any]] = [
            {"agent_id": "agent_1"},
            {"agent_id": "agent_2"},
            {"agent_id": "agent_3"},
            {"agent_id": "agent_4"},
        ]

        # Create BaseAgent instances
        self.agents = [BaseAgent(config=config, env=self.placebo_env) for config in self.agent_configs]

        # Define structure configuration
        self.structure_config = {
            "execution_mode": "hierarchical",
            "structure": {
                "agent_1": ["agent_2", "agent_3"],
                "agent_2": ["agent_4"]
            },
            "relationships": [
                {"source": "agent_1", "target": "agent_3", "type": "collaborates_with"},
                {"source": "agent_2", "target": "agent_4", "type": "supervises"}
            ]
        }

        # Initialize AgentGraph
        self.graph = AgentGraph(self.agents, self.structure_config)

    def test_initialization(self)-> None:
        # Test if all agents are added
        self.assertEqual(len(self.graph.agents), 4)
        # Test adjacency list
        self.assertIn("agent_1", self.graph.adjacency_list)
        self.assertIn("agent_2", self.graph.adjacency_list)
        self.assertIn("agent_3", self.graph.adjacency_list)
        self.assertIn("agent_4", self.graph.adjacency_list)
        self.assertListEqual(self.graph.adjacency_list["agent_1"], ["agent_2", "agent_3"])
        self.assertListEqual(self.graph.adjacency_list["agent_2"], ["agent_4"])
        self.assertListEqual(self.graph.adjacency_list["agent_3"], [])
        self.assertListEqual(self.graph.adjacency_list["agent_4"], [])

        # Test relationships
        self.assertEqual(len(self.graph.relationships), 2)
        self.assertIn(("agent_1", "agent_3", "collaborates_with"), self.graph.relationships)
        self.assertIn(("agent_2", "agent_4", "supervises"), self.graph.relationships)

        # Test relationships in agents
        self.assertEqual(self.graph.agents["agent_1"].relationships["agent_3"], "collaborates_with")
        self.assertEqual(self.graph.agents["agent_2"].relationships["agent_4"], "supervises")

    def test_get_children(self)->None:
        children_agent_1 = self.graph.get_children("agent_1")
        children_ids = [agent.agent_id for agent in children_agent_1]
        self.assertListEqual(children_ids, ["agent_2", "agent_3"])

    def test_get_roots(self)->None:
        roots = self.graph.get_roots()
        root_ids = [agent.agent_id for agent in roots]
        self.assertListEqual(root_ids, ["agent_1"])

    def test_traversal_hierarchical(self)->None:
        traversal = self.graph.traverse()
        traversal_ids = [agent.agent_id for agent in traversal]
        expected_order = ["agent_1", "agent_2", "agent_3", "agent_4"]
        self.assertListEqual(traversal_ids, expected_order)

    def test_add_agent(self)->None:
        new_agent = BaseAgent({"agent_id": "agent_5"}, env=self.placebo_env)
        self.graph.add_agent(new_agent)
        self.assertIn("agent_5", self.graph.agents)
        self.assertListEqual(self.graph.adjacency_list["agent_5"], [])

    def test_remove_agent(self)->None:
        self.graph.remove_agent("agent_3")
        self.assertNotIn("agent_3", self.graph.agents)
        self.assertNotIn("agent_3", self.graph.adjacency_list)
        # Check that relationships are updated
        self.assertNotIn(("agent_1", "agent_3", "collaborates_with"), self.graph.relationships)
        self.assertNotIn("agent_3", self.graph.agents["agent_1"].relationships)

    def test_update_agent(self)->None:
        self.graph.update_agent("agent_2", token_usage=100)
        agent_2 = self.graph.get_agent("agent_2")
        self.assertEqual(agent_2.token_usage, 100)

    def test_add_relationship(self)->None:
        self.graph.add_relationship("agent_3", "agent_4", "supports")
        self.assertIn(("agent_3", "agent_4", "supports"), self.graph.relationships)
        self.assertEqual(self.graph.agents["agent_3"].relationships["agent_4"], "supports")

    def test_remove_relationship(self)->None:
        self.graph.remove_relationship("agent_1", "agent_3")
        self.assertNotIn(("agent_1", "agent_3", "collaborates_with"), self.graph.relationships)
        self.assertNotIn("agent_3", self.graph.agents["agent_1"].relationships)

    def test_update_relationship(self)->None:
        self.graph.update_relationship("agent_2", "agent_4", "mentors")
        self.assertIn(("agent_2", "agent_4", "mentors"), self.graph.relationships)
        self.assertEqual(self.graph.agents["agent_2"].relationships["agent_4"], "mentors")

    def test_invalid_add_agent(self)->None:
        with self.assertRaises(ValueError):
            duplicate_agent = BaseAgent({"agent_id": "agent_1"}, env=self.placebo_env)
            self.graph.add_agent(duplicate_agent)

    def test_invalid_remove_agent(self)->None:
        with self.assertRaises(ValueError):
            self.graph.remove_agent("agent_999")

    def test_invalid_add_relationship(self)->None:
        with self.assertRaises(ValueError):
            self.graph.add_relationship("agent_1", "agent_999")

    def test_invalid_remove_relationship(self)->None:
        with self.assertRaises(ValueError):
            self.graph.remove_relationship("agent_1", "agent_999")

    def test_invalid_update_relationship(self)->None:
        with self.assertRaises(ValueError):
            self.graph.update_relationship("agent_1", "agent_999", "assists")


if __name__ == '__main__':
    unittest.main()

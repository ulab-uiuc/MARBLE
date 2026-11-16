from typing import List

from marble.agent import BaseAgent
from marble.configs.config import Config
from marble.environments import BaseEnvironment
from marble.graph.agent_graph import AgentGraph


def build_graph(relationships: List[List[str]], mode: str = "graph") -> AgentGraph:
    env = BaseEnvironment(name="test", config={})
    agents = [
        BaseAgent(config={"agent_id": f"agent{i}", "profile": f"p{i}"}, env=env)
        for i in range(1, 5)
    ]
    return AgentGraph(
        agents, Config({"coordinate_mode": mode, "relationships": relationships})
    )


def test_tree_children_are_registered_once() -> None:
    graph = build_graph(
        [["agent1", "agent2", "parent"], ["agent1", "agent3", "parent"]], mode="tree"
    )
    root = graph.get_root_agent()
    assert root is not None and root.agent_id == "agent1"
    assert [child.agent_id for child in root.children] == ["agent2", "agent3"]
    assert graph.get_agent("agent2").parent is root


def test_linked_profiles_are_undirected() -> None:
    graph = build_graph(
        [["agent1", "agent2", "reports_to"], ["agent3", "agent1", "supports"]]
    )
    assert sorted(graph.get_agent_profiles_linked("agent1")) == ["agent2", "agent3"]
    assert sorted(graph.get_agent_profiles_linked("agent2")) == ["agent1"]


def test_linked_profiles_fall_back_to_everyone_else() -> None:
    graph = build_graph([["agent1", "agent2", "reports_to"]])
    assert sorted(graph.get_agent_profiles_linked("agent4")) == [
        "agent1",
        "agent2",
        "agent3",
    ]


def test_invalid_relationship_is_rejected() -> None:
    try:
        build_graph([["agent1", "agent2"]])
    except ValueError as e:
        assert "Expected 3 elements" in str(e)
    else:
        raise AssertionError("expected a ValueError")

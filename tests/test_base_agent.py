"""Regression tests for BaseAgent (issues #188 and #241)."""

from typing import Any, Dict, List

from litellm.types.utils import Message

from marble.agent import BaseAgent
from marble.configs.config import Config
from marble.environments import BaseEnvironment
from marble.graph.agent_graph import AgentGraph
from tests.conftest import FakeLLM, tool_call_message


def build_agents(
    relationships: List[List[str]], mode: str = "graph", n: int = 3
) -> Dict[str, BaseAgent]:
    env = BaseEnvironment(name="test", config={})
    agents = [
        BaseAgent(
            config={"agent_id": f"agent{i}", "profile": f"profile {i}"},
            env=env,
            model="fake-model",
        )
        for i in range(1, n + 1)
    ]
    config = Config({"coordinate_mode": mode, "relationships": relationships})
    graph = AgentGraph(agents, config)
    for agent in agents:
        agent.set_agent_graph(graph)
    return {agent.agent_id: agent for agent in agents}


def communication_tool(call: Dict[str, Any]) -> Dict[str, Any]:
    tools = call.get("tools") or []
    matches = [t for t in tools if t["function"]["name"] == "new_communication_session"]
    assert len(matches) == 1
    return matches[0]["function"]["parameters"]["properties"]["target_agent_id"]


def test_communication_enum_lists_incoming_and_outgoing_neighbours(
    fake_llm: FakeLLM,
) -> None:
    # agent2 is only ever the *target* of a relationship (issue #241).
    agents = build_agents(
        [["agent1", "agent2", "manages"], ["agent3", "agent2", "helps"]]
    )
    agents["agent2"].act("say hello")

    target = communication_tool(fake_llm.calls[0])
    assert sorted(target["enum"]) == ["agent1", "agent3"]
    for agent_id in target["enum"]:
        assert f"- {agent_id} (" in target["description"]


def test_no_communication_tool_without_neighbours(fake_llm: FakeLLM) -> None:
    agents = build_agents([["agent1", "agent2", "manages"]])
    agents["agent3"].act("work alone")
    assert not fake_llm.calls[0].get("tools")


def test_communication_session_runs_and_uses_valid_tool_schema(
    fake_llm: FakeLLM,
) -> None:
    agents = build_agents([["agent1", "agent2", "collaborates with"]], n=2)

    def router(prompt: str, kwargs: Dict[str, Any]) -> Message:
        tools = kwargs.get("tools") or []
        names = [t["function"]["name"] for t in tools]
        if "new_communication_session" in names:
            return tool_call_message(
                "new_communication_session",
                {"target_agent_id": "agent2", "message": "Hi agent2, any ideas?"},
            )
        if "communicate_to" in names:
            schema = tools[0]["function"]["parameters"]
            # Strict providers reject ``required`` entries that are not declared.
            assert set(schema["required"]) <= set(schema["properties"])
            return tool_call_message("communicate_to", {"message": "<end-of-session>"})
        return Message(role="assistant", content="summary of the chat")

    fake_llm.router = router
    output, communication = agents["agent1"].act("discuss the task")

    assert "Hi agent2, any ideas?" in communication
    assert "From agent2 to agent1: <end-of-session>" in communication
    assert "Successfully completed session" in output
    assert isinstance(agents["agent1"].session_id, str)


def test_unknown_tool_does_not_crash_the_turn(fake_llm: FakeLLM) -> None:
    agents = build_agents([["agent1", "agent2", "collaborates with"]], n=2)
    fake_llm.router = lambda prompt, kwargs: tool_call_message("no_such_tool", {})
    output, communication = agents["agent1"].act("do something")
    assert "Error while executing 'no_such_tool'" in output
    assert communication is None


def test_truncated_tool_call_is_retried_with_a_larger_budget(
    fake_llm: FakeLLM,
) -> None:
    agents = build_agents([["agent1", "agent2", "collaborates with"]], n=2)

    def router(prompt: str, kwargs: Dict[str, Any]) -> Message:
        if kwargs["max_token_num"] <= 512:
            return Message(role="assistant", content=None)  # cut off mid tool call
        return Message(role="assistant", content="full answer")

    fake_llm.router = router
    output, _ = agents["agent1"].act("write a long message")
    assert "full answer" in output
    assert [c["max_token_num"] for c in fake_llm.calls] == [512, 2048]


def test_plan_tasks_for_children_parses_fenced_json(fake_llm: FakeLLM) -> None:
    # Issue #188: "Failed to parse tasks for children: Expecting value".
    agents = build_agents(
        [["agent1", "agent2", "parent"], ["agent1", "agent3", "parent"]], mode="tree"
    )
    tasks = agents["agent1"].plan_tasks_for_children("Discuss AI in healthcare")

    assert tasks == {"agent2": "child task 2", "agent3": "child task 3"}
    prompt = fake_llm.prompts()[0]
    # The JSON example used to be silently dropped from the prompt.
    assert '"child_agent_id": "Task description"' in prompt


def test_plan_tasks_for_children_falls_back_to_overall_task(
    fake_llm: FakeLLM,
) -> None:
    agents = build_agents(
        [["agent1", "agent2", "parent"], ["agent1", "agent3", "parent"]], mode="tree"
    )
    fake_llm.router = lambda prompt, kwargs: Message(
        role="assistant", content="I cannot produce JSON, sorry."
    )
    tasks = agents["agent1"].plan_tasks_for_children("Overall task")
    assert tasks == {"agent2": "Overall task", "agent3": "Overall task"}


def test_plan_next_agent_accepts_text_around_json(fake_llm: FakeLLM) -> None:
    agents = build_agents([["agent1", "agent2", "collaborates with"]], n=2)
    profiles = agents["agent1"].agent_graph.get_agent_profiles_linked("agent1")
    next_agent, plan = agents["agent1"].plan_next_agent("my result", profiles)
    assert (next_agent, plan) == ("agent2", "continue the work")

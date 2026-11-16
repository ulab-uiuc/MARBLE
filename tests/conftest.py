"""Shared fixtures for the offline test-suite (no API keys required)."""

import json
import os
from typing import Any, Callable, Dict, List

import pytest
from litellm.types.utils import Message

Router = Callable[[str, Dict[str, Any]], Message]

# Tests that talk to the real OpenAI API only run when a key is configured.
requires_openai = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY is not set; skipping tests that call the OpenAI API.",
)


def default_router(prompt: str, kwargs: Dict[str, Any]) -> Message:
    """Return a plausible canned answer for every kind of MARBLE prompt."""
    if "assigning tasks to a group of agents" in prompt:
        return Message(
            role="assistant",
            content='```json\n{"tasks": {"agent1": "do part A", "agent2": "do part B"},\n "continue": true // keep going\n}\n```',
        )
    if "determine whether the overall task is completed" in prompt:
        return Message(role="assistant", content='{"continue": false}')
    if "identify concrete milestones" in prompt:
        return Message(
            role="assistant",
            content='```json\n[{"milestone": "drafted a plan", "agents": ["agent1", "agent2"]}]\n```',
        )
    if '{"rating": X}' in prompt:
        return Message(role="assistant", content='{"rating": 4}')
    if "Assign specific tasks to your children agents" in prompt:
        return Message(
            role="assistant",
            content='Sure!\n```json\n{"agent2": "child task 2", "agent3": "child task 3"}\n```',
        )
    if "select the most suitable agent to continue the task" in prompt:
        return Message(
            role="assistant",
            content='Here you go: {"agent_id": "agent2", "planning_task": "continue the work"}',
        )
    if "Summarize the output of the agents" in prompt:
        return Message(role="assistant", content='{"summary": "all good"}')
    return Message(role="assistant", content="Finished my part of the task.")


class FakeLLM:
    """Records every call and answers through a router function."""

    def __init__(self, router: Router = default_router) -> None:
        self.router = router
        self.calls: List[Dict[str, Any]] = []

    def __call__(self, *args: Any, **kwargs: Any) -> List[Message]:
        if args:
            kwargs["llm_model"] = args[0]
        self.calls.append(kwargs)
        prompt = "\n".join(str(m.get("content", "")) for m in kwargs["messages"])
        return [self.router(prompt, kwargs)]

    def prompts(self) -> List[str]:
        return [
            "\n".join(str(m.get("content", "")) for m in call["messages"])
            for call in self.calls
        ]


@pytest.fixture
def fake_llm(monkeypatch: pytest.MonkeyPatch) -> FakeLLM:
    """Replace every ``model_prompting`` entry point with an offline fake."""
    fake = FakeLLM()
    for module in (
        "marble.agent.base_agent",
        "marble.engine.engine_planner",
        "marble.evaluator.evaluator",
    ):
        monkeypatch.setattr(f"{module}.model_prompting", fake)
    return fake


def tool_call_message(name: str, arguments: Dict[str, Any]) -> Message:
    return Message(
        role="assistant",
        content=None,
        tool_calls=[
            {
                "id": "call_1",
                "type": "function",
                "function": {"name": name, "arguments": json.dumps(arguments)},
            }
        ],
    )

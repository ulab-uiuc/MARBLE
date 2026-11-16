"""End-to-end engine runs with a fake LLM, for every coordination mode."""

import json
from typing import Any, Dict

import pytest

from marble.configs.config import Config
from marble.engine.engine import Engine
from tests.conftest import FakeLLM


def make_config(mode: str, output_path: str) -> Config:
    data: Dict[str, Any] = {
        "scenario": "unit-test",
        "task_id": 7,
        "coordinate_mode": mode,
        "relationships": [
            ["agent1", "agent2", "parent"],
            ["agent1", "agent3", "parent"],
        ],
        "llm": "fake-model",
        # A string on purpose: several benchmark configs store "5".
        "environment": {"type": "Base", "name": "Base", "max_iterations": "2"},
        "task": {"content": "Write a short plan."},
        "agents": [
            {"type": "BaseAgent", "agent_id": f"agent{i}", "profile": f"profile {i}"}
            for i in (1, 2, 3)
        ],
        "memory": {"type": "SharedMemory"},
        "metrics": None,  # an empty ``metrics:`` block in YAML
        "engine_planner": {"initial_progress": "Starting."},
        "output": {"file_path": output_path},
    }
    return Config(data)


@pytest.mark.parametrize("mode", ["graph", "star", "tree", "chain"])
def test_engine_runs_end_to_end(mode: str, tmp_path, monkeypatch, fake_llm: FakeLLM) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)  # the engine must not depend on the cwd
    output_path = tmp_path / "nested" / "dir" / "out.jsonl"  # created on demand

    engine = Engine(make_config(mode, str(output_path)))
    engine.start()

    records = [json.loads(line) for line in output_path.read_text().splitlines()]
    assert len(records) == 1
    record = records[0]
    assert record["coordination_mode"] == mode
    assert record["task_id"] == 7 and record["scenario"] == "unit-test"
    assert record["llm"] == "fake-model" and record["evaluate_llm"] == "fake-model"
    assert record["iterations"], "at least one iteration must be recorded"
    assert record["token_usage"] > 0
    # Scores come from the judge now instead of being hard-coded to -1.
    assert record["planning_scores"] and all(s == 4 for s in record["planning_scores"])
    assert record["total_milestones"] >= 1
    assert record["agent_kpis"].get("agent1", 0) >= 1


def test_tree_mode_runs_each_child_once(tmp_path, monkeypatch, fake_llm: FakeLLM) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    engine = Engine(make_config("tree", str(tmp_path / "out.jsonl")))
    engine.start()
    child_prompts = [p for p in fake_llm.prompts() if "This is your task: child task 2" in p]
    assert len(child_prompts) == 1


def test_unknown_coordination_mode_is_reported(tmp_path, monkeypatch, fake_llm: FakeLLM) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    engine = Engine(make_config("centralized", str(tmp_path / "out.jsonl")))
    with pytest.raises(ValueError, match="star, graph, chain, tree"):
        engine.start()


def test_coding_environment_uses_task_and_configured_model(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    from litellm.types.utils import Message

    import marble.environments.coding_utils.coder as coder

    monkeypatch.chdir(tmp_path)
    config = make_config("graph", str(tmp_path / "out.jsonl"))
    config.environment = {
        "type": "Coding",
        "name": "Coding Environment",
        "workspace_dir": str(tmp_path / "workspace"),
        "max_iterations": 1,
    }
    config.task = {"content": "Software Development Task:\n\nBuild UNIQUE_APP."}
    captured: Dict[str, Any] = {}

    def fake(model_name, messages, **kwargs):  # type: ignore[no-untyped-def]
        captured["model"] = model_name
        captured["prompt"] = messages[0]["content"]
        return [Message(role="assistant", content="```python\nprint('hi')\n```")]

    monkeypatch.setattr(coder, "model_prompting", fake)
    engine = Engine(config)
    # The agent passes a bogus model name; the configured one must be used.
    result = engine.environment.apply_action(
        agent_id="agent1",
        action_name="create_solution",
        arguments={"task_description": "ignored", "model_name": "gpt-3.5-turbo"},
    )
    assert result["success"], result
    assert captured["model"] == "fake-model"
    assert "UNIQUE_APP" in captured["prompt"]
    assert (tmp_path / "workspace" / "solution.py").read_text() == "print('hi')"
    assert engine._solution_path() == str(tmp_path / "workspace" / "solution.py")

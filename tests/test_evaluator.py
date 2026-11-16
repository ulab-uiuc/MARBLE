"""Regression tests for the Evaluator (no API access needed)."""

import os

from marble.evaluator.evaluator import Evaluator
from tests.conftest import FakeLLM


def test_evaluator_loads_prompts_from_any_directory(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)  # used to require cwd == marble/
    evaluator = Evaluator(metrics_config=None, default_llm="my-model")
    assert evaluator.llm == "my-model"
    assert "Graph" in evaluator.evaluation_prompts
    assert not os.path.exists(tmp_path / "evaluator")


def test_evaluate_llm_config_forms() -> None:
    assert Evaluator({"evaluate_llm": "judge-a"}).llm == "judge-a"
    assert Evaluator({"evaluate_llm": {"model": "judge-b"}}).llm == "judge-b"
    assert Evaluator({"evaluate_llm": ""}, default_llm="agent-model").llm == "agent-model"
    assert Evaluator({}).llm == "gpt-3.5-turbo"


def test_every_prompt_template_can_be_formatted() -> None:
    evaluator = Evaluator({})
    values = dict(
        task="t",
        communications="c",
        summary="s",
        agent_profiles="p",
        agent_tasks="a",
        results="r",
        agent_results="ar",
        result="res",
    )
    for group in evaluator.evaluation_prompts.values():
        for entry in group.values():
            for key, template in entry.items():
                if "prompt" in key:
                    # Used to raise KeyError('"rating"') for the scoring prompts.
                    rendered = template.format(**values)
                    assert "{{" not in rendered


def test_planning_and_communication_scores(fake_llm: FakeLLM) -> None:
    evaluator = Evaluator({})
    evaluator.evaluate_communication("task", "From agent1 to agent2: hi")
    evaluator.evaluate_planning("summary", "profiles", "tasks", "results")
    assert evaluator.metrics["communication_score"] == [4]
    assert evaluator.metrics["planning_score"] == [4]
    assert '{"rating": X}' in fake_llm.prompts()[0]


def test_kpi_counts_agents_from_the_prompted_key(fake_llm: FakeLLM) -> None:
    evaluator = Evaluator({})
    evaluator.evaluate_kpi("task", "results")
    assert evaluator.metrics["total_milestones"] == 1
    assert evaluator.metrics["agent_kpis"] == {"agent1": 1, "agent2": 1}


def test_parse_research_ratings() -> None:
    evaluator = Evaluator({})
    answer = 'Sure:\n```json\n{"innovation": 4, "safety": "5", "feasibility": 3}\n```'
    assert evaluator.parse_research_ratings(answer) == {
        "innovation": 4,
        "safety": 5,
        "feasibility": 3,
    }
    assert evaluator.parse_research_ratings("no ratings") == {}


def test_parse_milestones_handles_fences_and_garbage() -> None:
    evaluator = Evaluator({})
    assert evaluator.parse_milestones('[{"milestone": "m", "agents": []}]') == [
        {"milestone": "m", "agents": []}
    ]
    assert evaluator.parse_milestones("nothing") == []


def test_world_evaluation_scores_both_sides(fake_llm: FakeLLM) -> None:
    from litellm.types.utils import Message

    def router(prompt, kwargs):  # type: ignore[no-untyped-def]
        role = "buyer" if "**only for the buyer**" in prompt else "seller"
        return Message(
            role="assistant",
            content=f'{{"{role}": {{"effectiveness_of_strategies": 4, "progress_and_outcome": 3, "interaction_dynamics": 5}}}}',
        )

    fake_llm.router = router
    evaluator = Evaluator({})
    evaluator.evaluate_task_world("task", "negotiation transcript")
    evaluation = evaluator.metrics["task_evaluation"]
    assert evaluation["buyer"]["effectiveness_of_strategies"] == 4
    assert evaluation["seller"]["interaction_dynamics"] == 5


def test_code_quality_uses_the_given_task_and_code(fake_llm: FakeLLM) -> None:
    from litellm.types.utils import Message

    fake_llm.router = lambda prompt, kwargs: Message(
        role="assistant",
        content='{"instruction_following": 4, "executability": 5, "consistency": 3, "quality": 4}',
    )
    evaluator = Evaluator({})
    evaluator.evaluate_code_quality(
        task="Build UNIQUE_TASK_MARKER", code_result="print('UNIQUE_CODE_MARKER')"
    )
    prompt = fake_llm.prompts()[0]
    assert "UNIQUE_TASK_MARKER" in prompt and "UNIQUE_CODE_MARKER" in prompt
    assert evaluator.metrics["code_quality"]["executability"] == 5


def test_db_evaluation_computes_accuracy(fake_llm: FakeLLM) -> None:
    from litellm.types.utils import Message

    fake_llm.router = lambda prompt, kwargs: Message(
        role="assistant", content="LOCK_CONTENTION\nVACUUM"
    )
    evaluator = Evaluator({})
    evaluator.evaluate_task_db(
        "task",
        "we think it is lock contention and vacuum",
        ["INSERT_LARGE_DATA", "LOCK_CONTENTION", "VACUUM"],
        2,
        ["LOCK_CONTENTION"],
    )
    evaluation = evaluator.metrics["task_evaluation"]
    assert evaluation["predicted_labels"] == ["LOCK_CONTENTION", "VACUUM"]
    assert evaluation["accuracy"] == 1.0

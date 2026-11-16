"""Regression test for issue #244 (KeyError: 'player_dead_tonight')."""

import os
from typing import Any, Dict, List

from marble.agent.werewolf_agent import PROMPTS_DIR, resolve_api_key
from marble.environments.werewolf_env import WerewolfEnv, resolve_system_prompt_path


def make_env(night_log: Dict[str, Any]) -> WerewolfEnv:
    env = WerewolfEnv.__new__(WerewolfEnv)  # skip the API-backed constructor
    players = {
        "Martina": {"role": "witch", "status": {"health": 1, "antidote_count": 1, "poison_count": 1}},
        "Santos": {"role": "wolf", "status": {"health": 1}},
    }
    env.shared_memory = {
        "public_state": {"alive_players": list(players)},
        "private_state": {
            "players": players,
            # Werewolves failed to agree: there is no final target tonight.
            "werewolf_action": {"final_target": None},
            "night_cache": [night_log],
        },
    }
    env.scores = {
        "villager": {"total": 0, "details": []},
        "werewolf": {"total": 0, "details": []},
    }
    completed: List[str] = []
    env.completed = completed  # type: ignore[attr-defined]
    env.log_event = lambda **kwargs: None  # type: ignore[method-assign]
    env.mark_event_complete = lambda event_type: completed.append(event_type)  # type: ignore[method-assign]
    env.get_player_role = lambda player: players[player]["role"]  # type: ignore[method-assign]
    return env


def poison_event() -> Dict[str, Any]:
    return {
        "sender": "Martina",
        "content": {"use_antidote": False, "use_poison": True, "poison_target": "Santos"},
    }


def test_witch_poison_after_failed_werewolf_consensus() -> None:
    # Night log exactly as left behind by a night without a majority target.
    night_log: Dict[str, Any] = {
        "werewolf_action": {
            "final_target": "None",
            "attack_successful": False,
            "reason": "Failed due to lack of consensus",
        }
    }
    env = make_env(night_log)

    env.process_witch_action(poison_event())  # used to raise KeyError

    assert night_log["player_dead_tonight"] == ["Santos"]
    assert night_log["witch_action"] == {"action": "poison", "target": "Santos"}
    players = env.shared_memory["private_state"]["players"]
    assert players["Santos"]["status"]["health"] == 0
    assert players["Martina"]["status"]["poison_count"] == 0
    assert env.completed == ["witch_action"]  # type: ignore[attr-defined]
    assert env.get_night_deceased() == ["Santos"]


def test_prompt_files_resolve_on_every_platform() -> None:
    assert os.path.isfile(os.path.join(PROMPTS_DIR, "witch_prompt.yaml"))
    # Windows-style path from the old sample config.
    windows_style = "marble\\\\agent\\\\werewolf_prompts\\\\system_prompt.yaml"
    assert os.path.isfile(resolve_system_prompt_path(windows_style))
    assert os.path.isfile(resolve_system_prompt_path(None))
    assert os.path.isfile(resolve_system_prompt_path("does/not/exist.yaml"))


def test_api_key_resolution(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("OPENAI_API_KEY", "from-env")
    monkeypatch.setenv("MY_KEY", "custom-env")
    assert resolve_api_key({"api_key": "explicit"}, {}) == "explicit"
    assert resolve_api_key({"api_key": "your api key"}, {}) == "from-env"
    assert resolve_api_key({"api_key_env": "MY_KEY"}, {}) == "custom-env"
    assert resolve_api_key({}, {"openai_api_key": "top-level"}) == "top-level"

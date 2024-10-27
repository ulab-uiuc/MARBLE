from collections import defaultdict

import pytest

from marble.agent import BaseAgent
from marble.environments import WebEnvironment


@pytest.fixture
def test_agent_communication() -> None:
    env = WebEnvironment(config={})
    agent1 = BaseAgent(config={"agent_id": "Agent 1"}, env=env)
    agent2 = BaseAgent(config={"agent_id": "Agent 2"}, env=env)
    agent1.send_message("session", agent2, "Hi, how are you?")
    agent2.send_message("session", agent1, "Not bad.")
    # dictify
    agent1_msg_box = (lambda d: {k: (lambda f: f(f, v))(lambda f, x: {k2: f(f, v2) for k2, v2 in x.items()} if isinstance(x, defaultdict) else x) for k, v in d.items()})(agent1.msg_box)
    agent2_msg_box = (lambda d: {k: (lambda f: f(f, v))(lambda f, x: {k2: f(f, v2) for k2, v2 in x.items()} if isinstance(x, defaultdict) else x) for k, v in d.items()})(agent2.msg_box)
    # stringify
    assert f"{agent1_msg_box}" == "{'session': {'Agent 2': [(0, 'Hi, how are you?'), (1, 'Not bad.')]}}"
    assert f"{agent2_msg_box}" == "{'session': {'Agent 1': [(1, 'Hi, how are you?'), (0, 'Not bad.')]}}"

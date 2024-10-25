import pytest

from marble.graph.communications import CommunicationAgent, CommunicationAgentGraph
from marble.environments import BaseEnvironment

@pytest.fixture
def environment():
    return BaseEnvironment(name="TestEnv", config={})

@pytest.fixture
def agent_a(environment):
    return CommunicationAgent({"agent_id": "A"}, env=environment)

@pytest.fixture
def agent_b(environment):
    return CommunicationAgent({"agent_id": "B"}, env=environment)

@pytest.fixture
def agent_c(environment):
    return CommunicationAgent({"agent_id": "C"}, env=environment)

@pytest.fixture
def agent_d(environment):
    return CommunicationAgent({"agent_id": "D"}, env=environment)

@pytest.fixture
def agent_graph(agent_a, agent_b, agent_c, agent_d):
    structure_config = {
        "execution_mode": "centralized",  # You can change this to "layered" or "decentralized" for different tests
        "structure": {
            "A": ["B", "C", "D"],  # Define communication structure
        }
    }
    return CommunicationAgentGraph([agent_a, agent_b, agent_c, agent_d], structure_config, central_agent=agent_a)

# Test message sending and receiving for CommunicationAgent
def test_send_and_receive_message(agent_a, agent_b):
    agent_a.message = "Test Message from A"
    agent_a.send_message(agent_b)
    assert agent_b.inbox[agent_a.agent_id] == "Test Message from A"

def test_process_inbox(agent_a, agent_b):
    agent_a.message = "Process Test Message"
    agent_a.send_message(agent_b)
    agent_b.process_inbox(agent_a)
    assert agent_b.message == f"Result (B) of acting on task: Process Test Message"

# Test centralized communication
def test_centralized_communication(agent_graph, agent_a, agent_b, agent_c):
    agent_a.message = "Task from A"
    
    # Central agent starts communication
    agent_graph.execute()

    # Central agent should have received the results from the other agents
    assert agent_a.inbox[agent_b.agent_id] is not None
    assert agent_a.inbox[agent_c.agent_id] is not None

# Test layered communication
def test_layered_communication(agent_graph, agent_a, agent_b, agent_c):
    agent_graph.structure_config["execution_mode"] = "layered"

    agent_a.message = "Layered Message from A"
    agent_graph.execute()

    # Each agent in the next layer should have processed the previous agent's message
    print(agent_b.inbox)
    assert agent_b.message is not None

# Test decentralized communication
def test_decentralized_communication(agent_graph, agent_a, agent_b, agent_c):
    agent_graph.structure_config["execution_mode"] = "decentralized"

    agent_a.message = "Message from A"
    agent_graph.execute()

    # Agents should have communicated with each other
    assert agent_b.message is not None
    assert agent_c.message is not None
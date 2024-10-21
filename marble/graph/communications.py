import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath('/Users/guoshuyi/Desktop/MARBLE'))

from marble.agent.base_agent import BaseAgent
from marble.graph.agent_graph import AgentGraph
from marble.environments.base_env import BaseEnvironment
from marble.memory import SharedMemory

class CommunicationAgent(BaseAgent):
    def __init__(self, agent_id, env, shared_memory):
        super().__init__(agent_id, env)
        self.shared_memory = shared_memory
    
    def send_message(self, target_agent_id, message):
        """Send a message by updating the shared memory."""
        key = f"{self.agent_id}_to_{target_agent_id}"
        self.shared_memory.update(key, message)
        self.logger.info(f"Agent {self.agent_id} sent message to {target_agent_id}: {message}")
    
    def receive_messages(self):
        """Retrieve messages addressed to this agent from shared memory."""
        keys = [key for key in self.shared_memory.retrieve_all().keys() if key.endswith(f"_to_{self.agent_id}")]
        for key in keys:
            message = self.shared_memory.retrieve(key)
            from_agent_id = key.split('_to_')[0]
            self.handle_message(from_agent_id, message)
    
    def handle_message(self, from_agent_id, message):
        """Process the received message."""
        print(f"Agent {self.agent_id} processing message from {from_agent_id}: {message}")

class CommunicationAgentGraph(AgentGraph):
    def __init__(self, agents, structure_config, shared_memory):
        super().__init__(agents, structure_config)
        self.shared_memory = shared_memory

    def execute(self):
        if self.execution_mode == 'hierarchical':
            self._hierarchical_execution()
        elif self.execution_mode == 'cooperative':
            self._cooperative_execution()
        else:
            self._parallel_execution()

    def _parallel_execution(self):
        """Parallel execution where agents operate independently."""
        for agent in self.agents.values():
            agent.receive_messages()  # Process any new messages received
            for target_agent in self.agents.values():
                if agent.agent_id != target_agent.agent_id:
                    agent.send_message(target_agent.agent_id, "Parallel execution message")
            agent.receive_messages()  # Process any new messages received

    def _hierarchical_execution(self):
        """Hierarchical execution with message passing."""
        roots = self.get_roots()
        for agent in roots:
            self._traverse_hierarchy(agent)

    def _traverse_hierarchy(self, agent):
        children = self.get_children(agent.agent_id)
        for child in children:
            agent.send_message(child.agent_id, f"Message from {agent.agent_id}")
            child.receive_messages()  # Child processes the message
            self._traverse_hierarchy(child)

    def _cooperative_execution(self):
        """Cooperative execution with shared memory message passing."""
        for agent in self.agents.values():
            for target_agent in self.agents.values():
                if agent.agent_id != target_agent.agent_id:
                    agent.send_message(target_agent.agent_id, "Collaborate with me!")
            agent.receive_messages()  # Process any incoming messages



if __name__ == "__main__":
    # Initialize shared memory
    shared_memory = SharedMemory()

    # Create a test environment
    env = BaseEnvironment("Test Environment", {})

    # Example usage with CommunicationAgents using shared memory
    agent_a = CommunicationAgent({"agent_id": "A"}, env=env, shared_memory=shared_memory)
    agent_b = CommunicationAgent({"agent_id": "B"}, env=env, shared_memory=shared_memory)
    agent_c = CommunicationAgent({"agent_id": "C"}, env=env, shared_memory=shared_memory)

    structure_config = {
        "execution_mode": "cooperative",  # Can be "parallel", "hierarchical", or "cooperative"
        "structure": {
            "A": ["B"],  # A is parent of B
            "B": ["C"],  # B is parent of C
        },
    }

    # Create the agent communication graph
    communication_graph = CommunicationAgentGraph([agent_a, agent_b, agent_c], structure_config, shared_memory)

    # Execute the communication graph
    communication_graph.execute()

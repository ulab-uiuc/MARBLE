"""
Communication structures for agents in a multi-agent system.
"""

from typing import Any, Dict, List, Optional

from marble.agent.base_agent import BaseAgent
from marble.environments.base_env import BaseEnvironment
from marble.graph.agent_graph import AgentGraph
from marble.memory import SharedMemory


class CommunicationAgent(BaseAgent):
    def __init__(self, agent_id: str, env: BaseEnvironment, central_agent: Optional['CommunicationAgent'] = None, shared_memory: Optional[SharedMemory] = None, message: Optional[Any] = None) -> None:
        super().__init__(agent_id, env)
        self.inbox: Dict[str, Any] = {}  # Inbox stores received messages with {from_agent_id: message}
        self.outbox: Dict[str, Any] = {}  # Outbox stores sent messages with {target_agent_id: message}
        self.central_agent = central_agent  # Central agent for centralized communication
        self.shared_memory = shared_memory  # Shared memory for communication
        self.message = message  # Message to send

    def receive_message(self, from_agent: 'CommunicationAgent', message: Any) -> None:
        """
        Store the received message in the inbox.
        Args:
            from_agent (CommunicationAgent): The agent that sent the message.
            message (Any): The message received.
        """
        from_agent_id = from_agent.agent_id
        if message is None:
            self.logger.info(f"Agent {self.agent_id} received an empty message from {from_agent_id}.")
        else:
            self.inbox[from_agent_id] = message
            self.logger.info(f"Agent {self.agent_id} received message from {from_agent_id}: {message}")

    def send_message(self, target_agent: 'CommunicationAgent') -> None:
        """
        Send a message directly to the target agent's inbox and store in outbox.
        Args:
            target_agent (CommunicationAgent): The target agent to send the message to.
            message (Any): The message to send.
        """
        if self.message:
            # Store the sent message in the outbox
            self.outbox[target_agent.agent_id] = self.message
            # Directly place the message in the target agent's inbox
            target_agent.receive_message(self, self.message)
            self.logger.info(f"Agent {self.agent_id} sent message to {target_agent.agent_id}: {self.message}")
        else:
            self.logger.info(f"Agent {self.agent_id} has no message to send.")

    def act_on_task_and_communicate(self, task: str, target_agent: 'CommunicationAgent') -> None:
        """
        Use LLM to act on a task and send the result to another agent.
        """
        # result = self.act(task)
        result = f"Result ({self.agent_id}) of acting on task: {task}"
        self.message = result
        # Send the result to the target agent
        self.send_message(target_agent)

    def process_inbox(self, target_agent: 'CommunicationAgent') -> None:
        """
        Process all messages in the inbox.
        """
        if not self.inbox:
            self.send_message(target_agent)
        else:
            for from_agent_id, message in self.inbox.items():
                self.act_on_task_and_communicate(message, target_agent)
            self.inbox.clear()  # Clear the inbox after processing


class CommunicationAgentGraph(AgentGraph):
    def __init__(self, agents: List['CommunicationAgent'], structure_config: Dict[str, Any], central_agent: Optional['CommunicationAgent'] = None, shared_memory: Optional[SharedMemory] = None, central_agent_initiates=True):
        super().__init__(agents, structure_config)
        self.central_agent = central_agent  # Central agent for centralized communication
        self.structure_config = structure_config
        self.shared_memory = shared_memory
        self.central_agent_initiates = central_agent_initiates # Whether the central agent initiates communication

    def execute(self) -> None:
        """
        Execute agents based on the selected communication structure.
        """
        if self.execution_mode == 'layered':
            self._layered_execution()
        elif self.execution_mode == 'decentralized':
            self._decentralized_execution()
        elif self.execution_mode == 'centralized':
            self._centralized_execution()
        elif self.execution_mode == 'shared_message_pool':
            self._shared_message_pool_execution()  # Only applicable if you still want a shared pool
        else:
            raise ValueError(f"Unknown execution mode: {self.execution_mode}")

    # 1. Layered Communication
    def _layered_execution(self) -> None:
        """
        In Layered mode, each layer sends messages to the next layer.
        """
        layers = self.get_layers()
        for layer in layers[:-1]:  # Skip the last layer as they have no one to send to
            for agent in layer:
                next_layer = self.get_next_layer(agent.agent_id)
                for next_agent in next_layer:
                    agent.process_inbox(next_agent)  # Process any messages they received

    def get_layers(self) -> List[List['CommunicationAgent']]:
        """
        Return agents grouped by layers.
        """
        layers = []
        visited = set()
        queue = self.get_roots()
        while queue:
            current_layer = []
            next_queue = []
            for agent in queue:
                if agent.agent_id not in visited:
                    visited.add(agent.agent_id)
                    current_layer.append(agent)
                    next_queue.extend(self.get_children(agent.agent_id))
            layers.append(current_layer)
            queue = next_queue
        return layers

    def get_next_layer(self, agent_id: str) -> List['CommunicationAgent']:
        """
        Get the next layer of agents for a given agent.
        """
        return self.get_children(agent_id)

    # 2. Decentralized Communication
    def _decentralized_execution(self) -> None:
        """
        In Decentralized mode, every agent communicates with every other agent.
        """
        for agent in self.agents.values():
            for other_agent in self.agents.values():
                if agent.agent_id != other_agent.agent_id:
                    agent.process_inbox(other_agent)

    # 3. Centralized Communication
    def _centralized_execution(self) -> None:
            """
            In Centralized mode, all agents send messages to the central agent.
            """
            if self.central_agent is None:
                raise ValueError("Central agent is not set for centralized execution.")

            # The central agent initiates communication
            if self.central_agent_initiates:
                # Central agent sends messages to other agents
                for agent in self.agents.values():
                    if agent.agent_id != self.central_agent.agent_id:
                        self.central_agent.process_inbox(agent)
                # Each agent processes the received messages
                for agent in self.agents.values():
                    if agent.agent_id != self.central_agent.agent_id:
                        agent.process_inbox(self.central_agent)

            # Other agents send messages to the central agent first
            else:
                for agent in self.agents.values():
                    if agent.agent_id != self.central_agent.agent_id:
                        agent.process_inbox(self.central_agent)

                # Central agent processes the received messages and sends them to other agents
                for agent in self.agents.values():
                    if agent.agent_id != self.central_agent.agent_id:
                        self.central_agent.process_inbox(agent)


    # 4. Shared Message Pool Communication
    def _shared_message_pool_execution(self) -> None:
        """
        In Shared Message Pool mode, agents communicate via a shared message pool.
        """
        # for agent in self.agents.values():
        #     # Agent sends message to shared memory
        #     if agent.message:
        #         agent.communicate(agent.message)
        # for agent in self.agents.values():
        #     # Agent receives messages from shared memory
        #     retrieved_messages = agent.receive_communication()
            # for from_agent_id, message in retrieved_messages.items():
            #     # Process the received messages into the inbox
            #     from_agent = self.agents[from_agent_id]
            #     agent.receive_message(from_agent, message)
            # agent.process_inbox()
        pass





# Example usage
if __name__ == "__main__":
    # Initialize shared memory
    shared_memory = SharedMemory()

    # Create a test environment
    env = BaseEnvironment("Test Environment", {})

    # Define some agents
    agent_a = CommunicationAgent({"agent_id": "A"}, env, shared_memory=shared_memory, message="Task A")
    agent_b = CommunicationAgent({"agent_id": "B"}, env, shared_memory=shared_memory)
    agent_c = CommunicationAgent({"agent_id": "C"}, env, shared_memory=shared_memory)
    agent_d = CommunicationAgent({"agent_id": "D"}, env, shared_memory=shared_memory)
    # 1. layered communication
    # Define a structure configuration for layered communication
    structure_config = {
        "execution_mode": 'layered',  # Change to 'decentralized' or 'centralized' to try other modes
        "structure": {
            "A": ["B", "C"],  # A is parent of B, C
            "B": ["D"],  # B is parent of D
            "C": ["D"],  # C is parent of D
        }
    }
    # create the communication agent graph
    communication_graph = CommunicationAgentGraph([agent_a, agent_b, agent_c, agent_d], structure_config)
    # Execute the communication graph (Layered communication)
    communication_graph.execute()

    # # 2. centralized communication
    # # Define a structure configuration for centralized communication
    # structure_config = {
    #     "execution_mode": 'centralized',  # Change to 'decentralized' or 'centralized' to try other modes
    #     "structure": {
    #         "A": ["B", "C", "D"],  # A is parent of B, C, D
    #     }
    # }

    # # Create the communication agent graph
    # communication_graph = CommunicationAgentGraph([agent_a, agent_b, agent_c, agent_d], structure_config, central_agent=agent_a, central_agent_initiates=False)
    # # Execute the communication graph (Layered communication)
    # communication_graph.execute()

    # # 3. decentralized communication
    # # Define a structure configuration for decentralized communication
    # structure_config = {
    #     "execution_mode": 'decentralized',  # Change to 'decentralized' or 'centralized' to try other modes
    #     "structure": {
    #         "A": ["B", "C", "D"],  # A is parent of B, C, D
    #         "B": ["A", "C", "D"],  # B is parent of A, C, D
    #         "C": ["A", "B", "D"],  # C is parent of A, B, D
    #         "D": ["A", "B", "C"]   # D is parent of A, B, C
    #     }
    # }
    # communication_graph = CommunicationAgentGraph([agent_a, agent_b, agent_c, agent_d], structure_config)
    # communication_graph.execute()


    # # 4. shared message pool communication
    # # Define a structure configuration for shared message pool communication
    # structure_config = {
    #     "execution_mode": 'shared_message_pool',  # Change to 'decentralized' or 'centralized' to try other modes
    #     "structure": {
    #         "A": [],  # A is parent of B, C, D
    #         "B": [],  # B is parent of A, C, D
    #         "C": [],  # C is parent of A, B, D
    #         "D": []   # D is parent of A, B, C
    #     }
    # }
    # communication_graph = CommunicationAgentGraph([agent_a, agent_b, agent_c, agent_d], structure_config)
    # communication_graph.execute()

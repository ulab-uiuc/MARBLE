# Multi-Agent Benchmark (MultiAgentBench)

**MultiAgentBench** is a modular and extensible framework designed to facilitate the development, testing, and evaluation of multi-agent systems leveraging Large Language Models (LLMs). It provides a structured environment where agents can interact with various simulated environments, utilizing cognitive abilities and communication mechanisms to perform tasks collaboratively or competitively.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
  - [Folder Structure](#folder-structure)
  - [Key Components](#key-components)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Steps](#setup-steps)
- [Usage](#usage)
  - [Running the Simulation](#running-the-simulation)
  - [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Modular Design**: Easily extend or replace components like agents, environments, and LLM integrations.
- **Multi-Agent Support**: Model complex interactions between multiple agents with hierarchical or cooperative execution modes.
- **LLM Integration**: Interface with various LLM providers (OpenAI, Claude, etc.) through a unified API.
- **Shared Memory**: Implement shared memory mechanisms for agent communication and collaboration.
- **Flexible Environments**: Support for different simulated environments like Minecraft, ResearchTown, and Sotopia.
- **Metrics and Evaluation**: Built-in evaluation metrics to assess agent performance on tasks.
- **Industrial Coding Standards**: High-quality, well-documented code adhering to industry best practices.
- **Docker Support**: Containerized setup for consistent deployment and easy experimentation.

---

## Architecture

### Folder Structure

```bash
MultiAgentBench/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── reasoning_agent.py
│   └── cognitive_module.py
├── configs/
│   ├── __init__.py
│   ├── config.py
│   └── llm_config.py
├── datasets/
│   ├── __init__.py
│   └── classic_benchmark.py
├── engine/
│   ├── __init__.py
│   └── engine.py
├── environments/
│   ├── __init__.py
│   ├── base_env.py
│   ├── minecraft_env.py
│   ├── research_town_env.py
│   └── sotopia_env.py
├── graphs/
│   ├── __init__.py
│   └── agent_graph.py
├── llms/
│   ├── __init__.py
│   ├── base_llm.py
│   ├── openai_llm.py
│   ├── claude_llm.py
│   └── other_llm.py
├── memory/
│   ├── __init__.py
│   ├── base_memory.py
│   ├── long_term_memory.py
│   ├── short_term_memory.py
│   └── shared_memory.py
├── metrics/
│   ├── __init__.py
│   └── evaluation.py
├── tools/
│   ├── __init__.py
│   ├── web_search_tool.py
│   └── code_interpreter.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── parallel.py
│   └── config_loader.py
├── tests/
│   ├── __init__.py
│   └── test_engine.py
├── configs/
│   └── config.yaml
├── logs/
│   └── app.log
├── Dockerfile
├── requirements.txt
└── main.py
```

# Key Components
- Agents Module (agents/): Contains agent implementations, such as ReasoningAgent, which utilizes LLMs for decision-making and may include cognitive modules.
- LLMs Module (llms/): Interfaces with various language models, providing a unified API for agent interaction.
- Memory Module (memory/): Implements memory mechanisms for agents, including long-term, short-term, and shared memories.
- Environments Module (environments/): Abstracts different simulation environments where agents operate.
- Graphs Module (graphs/): Manages the agent network graph, supporting execution modes like hierarchical and cooperative.
- Engine Module (engine/): The core orchestrator that initializes components and runs the simulation loop.
- Metrics Module (metrics/): Provides evaluation metrics to assess agent performance.
- Tools Module (tools/): Includes utilities that agents can leverage, such as web search and code interpretation.
- Utils Module (utils/): Contains utility functions like logging, parallel execution, and configuration loading.
- Configurations (configs/): Manages configuration files for the system and LLMs.
- Tests (tests/): Contains unit and integration tests to validate system functionality.
- Dockerfile: Provides containerization for the application.
- Main Entry Point (main.py): The starting script to run the simulation.

# Installation

Prerequisites: Python 3.8 or higher
Docker (optional, for containerized setup)
OpenAI API Key (if using OpenAI's LLM)

## Setup Steps
Clone the Repository

```bash
git clone https://github.com/yourusername/MultiAgentBench.git
cd MultiAgentBench
```

## Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
## Install Dependencies
```bash
pip install -r requirements.txt
```
## Set Up Environment Variables Create a .env file in the root directory and add your OpenAI API key:
```bash
OPENAI_API_KEY=your-openai-api-key
Configure the Application Update the configs/config.yaml file with your desired settings.
```
## Usage

Running the Simulation
Using Python Directly
```bash

python main.py
```
Using Docker Build the Docker Image
```bash

docker build -t multiagentbench .
```
Run the Docker Container
```bash

docker run -p 8080:8080 --env OPENAI_API_KEY=your-openai-api-key multiagentbench
```
Configuration
The simulation behavior is controlled via the configs/config.yaml file.

Example Configuration (configs/config.yaml):

yaml
environment:
  type: Minecraft
  parameters:
    world_seed: 12345

agents:
  - agent_id: agent_1
    type: ReasoningAgent
    llm:
      type: OpenAI
      api_key: 'your-openai-api-key'
      model_name: 'text-davinci-003'
  - agent_id: agent_2
    type: ReasoningAgent
    llm:
      type: OpenAI
      api_key: 'your-openai-api-key'
      model_name: 'text-davinci-003'

graph:
  execution_mode: hierarchical
  structure:
    agent_1:
      - agent_2

memory:
  type: SharedMemory

metrics:
  - TaskCompletion

logger:
  level: DEBUG
Key Configuration Sections:

environment: Defines the simulation environment.
agents: Lists the agents participating in the simulation and their configurations.
graph: Specifies the execution mode and structure of agent interactions.
memory: Configures the memory mechanism used by agents.
metrics: Sets the evaluation metrics to be used.
logger: Configures logging levels and formats.
Examples
Hierarchical Execution Example
In hierarchical execution mode, agents are executed following a defined hierarchy.

Graph Structure:


agent_1
└── agent_2
    └── agent_3
Config Snippet:

yaml

graph:
  execution_mode: hierarchical
  structure:
    agent_1:
      - agent_2
    agent_2:
      - agent_3
Cooperative Execution Example
In cooperative execution mode, agents communicate via shared memory and coordinate their actions.

Config Snippet:

yaml

graph:
  execution_mode: cooperative
  structure: {}

memory:
  type: SharedMemory
Adding a New Agent
To add a new agent, such as a CollaborativeAgent, implement it in the agents/ directory and update the configuration.

Implementing CollaborativeAgent (agents/collaborative_agent.py):


from agents.base_agent import BaseAgent

class CollaborativeAgent(BaseAgent):
    def perceive(self, state):
        # Custom perception logic
        pass

    def act(self, perception):
        # Custom action logic
        pass
Updating Configuration:

yaml

agents:
  - agent_id: agent_1
    type: CollaborativeAgent
    # Additional configurations
Contributing
Contributions are welcome! Please follow these steps:

Fork the Repository
Create a Feature Branch
bash

git checkout -b feature/your-feature
Commit Your Changes
bash

git commit -m "Add your feature"
Push to Your Fork
bash

git push origin feature/your-feature
Create a Pull Request Submit your pull request for review.
License
This project is licensed under the MIT License.

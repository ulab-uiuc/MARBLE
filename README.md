
**MultiAgentBench** is a modular and extensible framework designed to facilitate the development, testing, and evaluation of multi-agent systems leveraging Large Language Models (LLMs). It provides a structured environment where agents can interact within various simulated environments, utilizing cognitive abilities and communication mechanisms to perform tasks collaboratively or competitively.

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
  - [Hierarchical Execution Example](#hierarchical-execution-example)
  - [Cooperative Execution Example](#cooperative-execution-example)
  - [Adding a New Agent](#adding-a-new-agent)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Modular Design**: Easily extend or replace components like agents, environments, and LLM integrations.
- **Multi-Agent Support**: Model complex interactions between multiple agents with hierarchical or cooperative execution modes.
- **LLM Integration**: Interface with various LLM providers (OpenAI, etc.) through a unified API.
- **Shared Memory**: Implement shared memory mechanisms for agent communication and collaboration.
- **Flexible Environments**: Support for different simulated environments like web-based tasks.
- **Metrics and Evaluation**: Built-in evaluation metrics to assess agent performance on tasks.
- **Industrial Coding Standards**: High-quality, well-documented code adhering to industry best practices.
- **Docker Support**: Containerized setup for consistent deployment and easy experimentation.

---

## Architecture

### Folder Structure

```bash
MultiAgentBench/
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── assets/
├── data/
│   ├── dataloader.py
│   └── task.json
├── examples/
│   └── docs/
├── logs/
│   └── __init__.py
├── marble/
│   ├── README.md
│   ├── __init__.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   └── reasoning_agent.py
│   ├── configs/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── config.yaml
│   │   └── test_config.yaml
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── engine_planner.py
│   ├── environments/
│   │   ├── __init__.py
│   │   ├── base_env.py
│   │   └── web_env.py
│   ├── evaluator/
│   │   ├── __init__.py
│   │   └── evaluator.py
│   ├── graph/
│   │   ├── __init__.py
│   │   └── agent_graph.py
│   ├── llms/
│   │   ├── __init__.py
│   │   ├── base_llms.py
│   │   ├── error_handler.py
│   │   ├── model_prompting.py
│   │   └── openai_api.py
│   ├── main.py
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── base_memory.py
│   │   └── shared_memory.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── web_search.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── poetry.lock
├── pyproject.toml
├── scripts/
└── tests/
    ├── test_engine.py
    ├── test_graph.py
    └── test_init.py

## Key Components

- **Agents Module (`marble/agent/`):**  
  Contains agent implementations, such as `BaseAgent` and `ReasoningAgent`, which utilize LLMs for decision-making and may include cognitive modules.

- **LLMs Module (`marble/llms/`):**  
  Interfaces with various language models, providing a unified API for agent interaction.

- **Memory Module (`marble/memory/`):**  
  Implements memory mechanisms for agents, including shared memory for inter-agent communication.

- **Environments Module (`marble/environments/`):**  
  Abstracts different simulation environments where agents operate, such as web-based environments.

- **Graphs Module (`marble/graph/`):**  
  Manages the agent network graph, supporting execution modes like hierarchical and cooperative, and handles agent relationships.

- **Engine Module (`marble/engine/`):**  
  The core orchestrator that initializes components and runs the simulation loop.

- **Evaluator Module (`marble/evaluator/`):**  
  Provides evaluation metrics to assess agent performance.

- **Tools Module (`marble/tools/`):**  
  Includes utilities that agents can leverage, such as web search functionality.

- **Utils Module (`marble/utils/`):**  
  Contains utility functions like logging and configuration loading.

- **Configurations (`marble/configs/`):**  
  Manages configuration files for the system and LLMs.

- **Tests (`tests/`):**  
  Contains unit and integration tests to validate system functionality.

- **Main Entry Point (`marble/main.py`):**  
  The starting script to run the simulation.

- **Scripts (`scripts/`):**  
  Contains auxiliary scripts for tasks like data processing or setup.

- **Assets and Data (`assets/`, `data/`):**  
  Include any additional resources or datasets required for simulations.

- **Examples (`examples/`):**  
  Provides example configurations and documentation to help users get started.

## Installation

### Prerequisites

- **Python 3.8 or higher**
- **Docker** (optional, for containerized setup)
- **OpenAI API Key** (if using OpenAI's LLM)

### Setup Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/MultiAgentBench.git
    cd MultiAgentBench
    ```

2. **Create a Virtual Environment (Recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**

    Create a `.env` file in the root directory and add your OpenAI API key:

    ```bash
    OPENAI_API_KEY=your-openai-api-key
    ```

5. **Configure the Application**

    Update the `marble/configs/config.yaml` file with your desired settings.

## Usage

### Running the Simulation

#### Using Python Directly

```bash
python marble/main.py
```


## Developing

#### Develop Demo

To develop the demo (both frontend and backend):

```bash
cd frontend
npm install
npm start
```

```bash
poetry install -E backend
cd backend
uvicorn main:app --reload
```

#### Install dev options

Follow the installation instruction above and then, instead of running `python -m pip install -e .`, run the following commands:

```
python -m pip install -e ".[dev]"
mypy --install-types --non-interactive research_town
python -m pip install pre-commit
pre-commit install
```

The installation of pre-commit would avoid formatting error and large file injects into github commits.

#### New branch for each feature

`git checkout -b feature/feature-name` and PR to `main` branch.

#### Before committing

Run `poetry run pytest` to make sure all tests pass (this will ensure dynamic typing passed with beartype) and `poetry run mypy --config-file pyproject.toml .` to check static typing. (You can also run `pre-commit run --all-files` to run all checks)

#### Check github action result

Check the github action result to make sure all tests pass. If not, fix the errors and push again.


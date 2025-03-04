# Research Collaboration Simulation Environment

This repository provides a configurable environment for simulating multiagent research collaboration tasks. The environment facilitates knowledge exchange among AI agents to generate novel research ideas using a structured approach.

## Features

- **Multiagent Collaboration:** Agents interact in a fully connected network to exchange expertise and ideas.
- **Research Tools Integration:** Built-in functions to fetch related papers, recent publications, co-author networks, and more.
- **Curated Benchmark Dataset:** Utilizes 100 curated ML/AI papers from the ResearchTown project, categorized into 33 easy, 34 medium, and 33 hard tasks.
- **Structured Idea Generation:** Generates research ideas using a standardized 5q format.
- **Configurable Environment:** Easily adjustable simulation parameters and evaluation metrics through configuration files.

---


## Execution Steps
1. Navigate to the multiagentbench folder:
```bash
cd multiagentbench
```

2. Generate the Configuration Folder: Run the conversion script to generate YAML configuration files:

```bash
bash runjsonl2yaml.sh
```

3. Update the Configuration Path: Edit the run_simulation.sh script to update the CONFIG_FILE variable to point to the newly generated configuration folder:
```bash

CONFIG_FILE="./configs/test_config"  # config path for the research scenario
```

4. Run the Simulation: Execute the simulation:
```bash
bash run_simulation.sh
```

Parameter Explanation for runjsonl2yaml.sh
The runjsonl2yaml.sh script accepts parameters to customize the research simulation environment. Example parameters include:

```bash

DEFAULT_COORDINATE_MODE="graph"
DEFAULT_ENVIRONMENT='{"max_iterations": 5, "name": "Research Collaboration Environment", "type": "Research"}'
DEFAULT_LLM="gpt-3.5-turbo"
DEFAULT_MEMORY='{"type": "BaseMemory"}'
DEFAULT_METRICS_EVALUATE_LLM="gpt-4o"
DEFAULT_OUTPUT='{"file_path": "result/discussion_output.jsonl"}'
DEFAULT_COORDINATE_MODE: Sets the collaboration mode for agents (graph-based coordination).
DEFAULT_ENVIRONMENT: Configures environment settings such as maximum iterations, environment name, and type.
DEFAULT_LLM: Specifies the language model for agent interactions.
DEFAULT_MEMORY: Defines the memory system used during the simulation.
DEFAULT_METRICS_EVALUATE_LLM: Determines the LLM for performance evaluation.
DEFAULT_OUTPUT: Sets the file path where the simulation output will be saved.
```

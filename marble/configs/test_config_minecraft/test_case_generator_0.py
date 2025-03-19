import json

import yaml
from tqdm import tqdm

# with open("marble/configs/test_config_minecraft/depricated/test_config_llama-31-8b_4.yaml", "r") as f:
#     data = yaml.safe_load(f)

# print(json.dumps(data, indent=4))

with open("data/blueprint_description_all.json", "r") as f:
    source_data = json.load(f)

models = [
    [
        "gpt-4o-mini",
        "gpt-4o-mini"
    ],
]

minecraft_knowledge_card = """
Here are some knowledge about minecraft:
1. The minecraft world x,z is the horizontal coordinate, y is the vertical coordinate. y=-61 is the ground level.
2. You can use the tool or empty hand to dig the block, and place the block to the world.
3. A block cannot be directly placed in the air. When being placed, there must be at least one existing block next to it.
4. A block can exist in the air by removing all the other blocks attached to it.
5. You can find the item in the chest. Item in the chest can not directly be seen or used, take it out and use it or equip it.
6. If their is no items in the chest, maybe you can find the item at other chest or get it from other agent or dig it up or craft it.
7. One bucket can hold one item, if you want to get more items, you need to get more buckets at first.
8. You are in a team with other agents, you can try to find the item from other agents, and do not change the blocks other agents placed without permission.
""".strip()

task_template = """
This is in the game of Minecraft. Build a building according to a blueprint. The blueprint contains necessary information about the material, facing direction and position of each block.
*** The minecraft knowledge card ***
{minecraft_knowledge_card}
*** The blueprint ***
{blueprint}
""".strip()

max_iterations = 1

offset = 0

for model in tqdm(models):
    short_model_name = model[0]
    long_model_name = model[1]
    for task_name, task_blueprint in tqdm(source_data.items(), leave=False):
        task_id = int(task_name.split("_")[-1])
        if task_id >= 10:
            break
        task_config = dict()
        task_config["coordinate_mode"] = "graph"
        task_config["relationships"] = [
            [
                "agent1",
                "agent2",
                "collaborate with"
            ],
            [
                "agent1",
                "agent3",
                "collaborate with"
            ],
            [
                "agent2",
                "agent3",
                "collaborate with"
            ]
        ]
        task_config["environment"] = {
            "type": "Minecraft",
            "name": "Minecraft Environment",
            "host": "localhost",
            "port": 25565 + offset,
            "max_iterations": max_iterations,
            "task_id": task_id,
            "task_name": "test"
        }
        task_config["task"] = {
            "content": task_template.format(minecraft_knowledge_card=minecraft_knowledge_card, blueprint=json.dumps(task_blueprint, indent=4))
        }
        # task_config["agents"] = [
        #     {
        #         "type": "BaseAgent",
        #         "agent_id": "agent1",
        #         "agent_port": 5000,
        #         "profile": "agent1 is a pragmatic team member. agen1 prefers doing more actual work rather than talking."
        #     },
        #     {
        #         "type": "BaseAgent",
        #         "agent_id": "agent2",
        #         "agent_port": 5001,
        #         "profile": "agent2 is a talkative team member. agent2 talks more than doing actual work."
        #     },
        #     {
        #         "type": "BaseAgent",
        #         "agent_id": "agent3",
        #         "agent_port": 5002,
        #         "profile": "agent3 is a judgmental team member. agent3 likes making reflections and criticizing team members."
        #     }
        # ]
        task_config["agents"] = [
            {
                "type": "BaseAgent",
                "agent_id": "agent1",
                "agent_port": 5000 + 10*offset,
                "profile": "agent1 is a team member good at finding correct materials in the container and place the block in the correct place. agent1 know that retrieving materials can be done by using 'withdrawItem' and placing blocks can be done by using 'placeBlock'. agent1 is willing to seek help from other team members."
            },
            {
                "type": "BaseAgent",
                "agent_id": "agent2",
                "agent_port": 5001 + 10*offset,
                "profile": "agent2 is a team member good at designing the correct order of placing the blocks since a block cannot be directly placed in the air. agent2 knows how to design auxilary blocks when some target blocks have to be in the air. agent2 tends to tell agent1 the correct order of placing target blocks and tell agent3 when to put auxilary blocks and when to remove them."
            },
            {
                "type": "BaseAgent",
                "agent_id": "agent3",
                "agent_port": 5002 + 10*offset,
                "profile": "agent3 is a team member good at placing auxilary blocks and removing them according to the discussion with agent2. agent1 know that placing auxilary blocks can be done by using 'placeBlock' or 'erectDirtLadder' and removing them can be done by using 'MineBlock' or 'dismantleDirtLadder'."
            }
        ]
        task_config["memory"] = {
            "type": "SharedMemory"
        }
        task_config["metrics"] = {
            "evaluate_llm": {
                "model": "gpt-3.5-turbo",
                "provider": "openai"
            }
        }
        task_config["engine_planner"] = {
            "initial_progress": "Starting the simulation."
        }
        task_config["llm"] = long_model_name
        task_config["output"] = {
            "file_path": f"result/minecraft/iteration_ablation/discussion_output_{short_model_name}_{task_id//20}.jsonl"
        }
        with open(f"marble/configs/test_config_minecraft/iteration_ablation/test_config_{short_model_name}_{task_id}.yaml", "w") as f:
            yaml.safe_dump(task_config, f)
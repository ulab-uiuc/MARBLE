import yaml, json

with open("marble/configs/test_config_minecraft/test_config_gpt-4o-mini_0.yaml", "r") as f:
    data = yaml.safe_load(f)

# print(json.dumps(data, indent=4))
print(data["task"]["content"])
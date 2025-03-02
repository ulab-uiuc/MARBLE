import json

# 用于存储唯一的类别
topic_categories = set()
coordination_categories = set()

# 读取文件
with open('/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/benchmark.jsonl', 'r') as file:
    for line in file:
        try:
            data = json.loads(line)
            topic_categories.add(data['topic_category'])
            coordination_categories.add(data['coordination_category'])
        except json.JSONDecodeError:
            continue

print("Topic Categories:")
print(list(topic_categories))
print("\nCoordination Categories:")
print(list(coordination_categories))

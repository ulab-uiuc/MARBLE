import json

import fire


def read_categories(
    benchmark_path="/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/assets/benchmark.jsonl",
):
    topic_categories = set()
    coordination_categories = set()

    with open(benchmark_path, "r") as file:
        for line in file:
            try:
                data = json.loads(line)
                topic_categories.add(data["topic_category"])
                coordination_categories.add(data["coordination_category"])
            except json.JSONDecodeError:
                continue

    print("Topic Categories:")
    print(list(topic_categories))
    print("\nCoordination Categories:")
    print(list(coordination_categories))

    return {
        "topic_categories": list(topic_categories),
        "coordination_categories": list(coordination_categories),
    }


if __name__ == "__main__":
    fire.Fire(read_categories)

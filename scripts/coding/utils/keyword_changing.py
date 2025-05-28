import os

import fire


def replace_model_name(
    old_model="gpt-4o-mini",
    new_model="gpt-3.5-turbo",
    file_paths=[
        "/opt/dlami/nvme/zhe/MARBLE/marble/engine/engine_planner.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/agent/coding_agent.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/agent/base_agent.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/memory/long_term_memory.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/memory/short_term_memory.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/coder.py",
        "/opt/dlami/nvme/zhe/MARBLE/marble/environments/coding_utils/reviewer.py",
        "/opt/dlami/nvme/zhe/MARBLE/scripts/coding/run_demo.sh",
    ],
):
    print("Starting model name replacement...")

    for file_path in file_paths:
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            if old_model in content:
                new_content = content.replace(old_model, new_model)

                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"Replaced model name in: {file_path}")
            else:
                print(f"Model name not found in: {file_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    print("Replacement process completed.")


if __name__ == "__main__":
    fire.Fire(replace_model_name)

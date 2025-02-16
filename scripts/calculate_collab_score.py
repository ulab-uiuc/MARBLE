import os
import json

def calculate_scores(folder_path):
    """
    从指定文件夹下读取所有 .jsonl 文件，
    计算每个文件中的 communication_score 和 planning_score 的平均值，
    并输出这两个平均值以及它们的平均。
    """
    # 1. 获取文件夹中所有以 .jsonl 结尾的文件列表
    files = [f for f in os.listdir(folder_path) if f.endswith(".jsonl")]
    
    # 如果只想固定处理5个文件（假设文件名是已知），可以改成：
    # files = ["file1.jsonl", "file2.jsonl", "file3.jsonl", "file4.jsonl", "file5.jsonl"]

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        
        total_communication = 0.0
        total_planning = 0.0
        count = 0
        
        # 2. 读取 .jsonl 文件，每行都是一个 JSON 对象
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    
                    # 获取 communication_score 和 planning_score
                    comm_score = data.get("communication_score") or 0.0
                    plan_score = data.get("planning_score") or 0.0
                    
                    total_communication += comm_score
                    total_planning += plan_score
                    count += 1
                except json.JSONDecodeError:
                    # 如果某行不是合法JSON，可以选择跳过或直接报错
                    continue
        
        if count == 0:
            # 处理空文件或没有任何有效数据的情况
            print(f"文件 {file_name} 中无有效数据。")
            continue
        
        # 3. 计算平均值
        avg_communication = total_communication / count
        avg_planning = total_planning / count
        
        # 计算 (communication + planning) 的平均值
        avg_of_two = (avg_communication + avg_planning) / 2
        
        # 4. 打印结果（保留三位小数）
        print(f"文件: {file_name}")
        print(f"  平均 communication_score: {avg_communication:.3f}")
        print(f"  平均 planning_score: {avg_planning:.3f}")
        print(f"  两者平均值: {avg_of_two:.3f}")
        print("-" * 50)

if __name__ == "__main__":
    # 将此路径替换为你放置 .jsonl 文件的文件夹路径
    folder_path = "llm_eval_result\\ablation\output"
    calculate_scores(folder_path)

import json

def calculate_scores(file_path):
    # 初始化列表存储所有分数
    collaboration_scores = []
    coordination_scores = []
    task_completion_scores = []
    
    # 读取jsonl文件
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            
            # 获取planning和communication scores
            planning_scores = data.get('planning_scores', [])
            communication_scores = data.get('communication_scores', [])
            
            # 将-1视为0
            communication_scores = [0 if score == -1 else score for score in communication_scores]
            
            # 计算collaboration score(包括-1, 视为0)
            if planning_scores and communication_scores:
                avg_score = (sum(planning_scores) + sum(communication_scores)) / (len(planning_scores) + len(communication_scores))
                collaboration_scores.append(avg_score)
            
            # 计算coordination score(不包括-1)
            valid_scores = planning_scores + [s for s in communication_scores if s != 0]
            if valid_scores:
                coord_score = sum(valid_scores) / len(valid_scores)
                coordination_scores.append(coord_score)
            
            # 计算task completion score
            if 'code_quality' in data:
                code_quality = data['code_quality']
                if isinstance(code_quality, dict):
                    quality_scores = [
                        code_quality.get('instruction_following', 0),
                        code_quality.get('executability', 0),
                        code_quality.get('consistency', 0),
                        code_quality.get('quality', 0)
                    ]
                    avg_quality = sum(quality_scores) / len(quality_scores)
                    task_completion_scores.append(avg_quality)
    
    # 计算总平均分数
    final_collaboration = sum(collaboration_scores) / len(collaboration_scores) if collaboration_scores else 0
    final_coordination = sum(coordination_scores) / len(coordination_scores) if coordination_scores else 0
    final_completion = sum(task_completion_scores) / len(task_completion_scores) if task_completion_scores else 0
    
    return {
        'collaboration_score': final_collaboration,
        'coordination_score': final_coordination, 
        'task_completion_score': final_completion
    }

def main():
    file_path = '/home/zhe36/MARBLE/marble/result/development_output.jsonl'
    
    try:
        scores = calculate_scores(file_path)
        print("分数统计结果:")
        print(f"Collaboration Score (包括-1视为0): {scores['collaboration_score']:.2f}")
        print(f"Coordination Score (不包括-1): {scores['coordination_score']:.2f}")
        print(f"Task Completion Score: {scores['task_completion_score']:.2f}")
    except Exception as e:
        print(f"计算失败: {str(e)}")

if __name__ == "__main__":
    main()
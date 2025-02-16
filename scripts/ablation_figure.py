import matplotlib.pyplot as plt

# 文件名中的数字后缀，作为 X 轴刻度
x = [1, 3, 5, 7, 10, 20]

# 各种分数，顺序与 x 保持对应
task_scores = [val * 20 for val in [0, 0.99, 2.16, 3.19, 1.40, 3.62]]
comm_scores = [val * 20 for val in [1.4, 1.2, 2.6, 3.0, 3.0, 2.9]]
plan_scores = [val * 20 for val in [2.7, 3.0, 3.0, 2.9, 3.1, 3.1]]
collab_scores = [val * 20 for val in [2.05, 2.1, 2.8, 2.95, 3.05, 3.0]]

plt.figure(figsize=(8, 5))

# 绘制 Task Score (蓝色)
plt.plot(x, task_scores, marker='o', color='blue', linestyle='-', label='Task Score')
# 绘制 Communication Score (红色)
plt.plot(x, comm_scores, marker='s', color='red', linestyle='--', label='Communication Score')
# 绘制 Planning Score (绿色)
plt.plot(x, plan_scores, marker='^', color='green', linestyle='-.', label='Planning Score')
# 绘制 Collaboration Score (橙色)
plt.plot(x, collab_scores, marker='D', color='orange', linestyle=':', label='Collaboration Score')

# X 轴刻度
plt.xticks(x)
plt.xlabel("Iterations")
plt.ylabel("Score Value")

# 将标题加粗，同时字号稍微增大（比默认大一点）
plt.title("Scores for gpt-4o-mini across different Iterations in MineCraft",
          fontweight="bold", fontsize=14)

# 网格与图例
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='best')

# 自动调整布局并保存
plt.tight_layout()
plt.savefig("scores.pdf")
plt.show()

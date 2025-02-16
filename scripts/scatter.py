import os
import json
import numpy as np
import matplotlib
# 如在无GUI环境下可用 "Agg"，若在本地有图形界面则可保持 "TkAgg"
matplotlib.use("TkAgg")  
import matplotlib.pyplot as plt

def parse_result_json(json_path, x_data, y_data):
    """
    解析单个 result.json 文件，提取 net_score (villager.total - werewolf.total)
    和 result_score 并追加到 x_data / y_data 中。
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    process_scores = data.get("process_scores", {})
    villager_total = process_scores.get("villager", {}).get("total", 0.0)
    werewolf_total = process_scores.get("werewolf", {}).get("total", 0.0)

    net_score = villager_total - werewolf_total
    result_score = data.get("result_score", 0.0)

    x_data.append(net_score)
    y_data.append(result_score)

def collect_data(root_dir):
    """
    从 root_dir 下:
      1) 遍历 6 个子目录 (folder_1)
      2) 每个子目录下 100 个文件夹 (folder_2)
      3) 在 folder_2 中查找以 'fullrun' 开头的文件夹 (folder_3)
      4) 进入该文件夹(或其子文件夹) 查找 result.json
    收集 net_score = villager.total - werewolf.total 与 result_score,
    并返回 (x_data, y_data).
    """
    x_data = []
    y_data = []

    for folder_1 in os.listdir(root_dir):
        path_1 = os.path.join(root_dir, folder_1)
        if not os.path.isdir(path_1):
            continue

        for folder_2 in os.listdir(path_1):
            path_2 = os.path.join(path_1, folder_2)
            if not os.path.isdir(path_2):
                continue

            # 查找 'fullrun' 开头的文件夹
            for folder_3 in os.listdir(path_2):
                if folder_3.startswith("fullrun"):
                    full_run_path = os.path.join(path_2, folder_3)
                    if not os.path.isdir(full_run_path):
                        continue

                    # 在 full_run_path 下找 result.json 或其子文件夹
                    for item in os.listdir(full_run_path):
                        item_path = os.path.join(full_run_path, item)

                        if os.path.isdir(item_path):
                            # 假设子文件夹里有 result.json
                            res_file = os.path.join(item_path, "result.json")
                            if os.path.isfile(res_file):
                                parse_result_json(res_file, x_data, y_data)
                        else:
                            # 如果当前就是 result.json
                            if item == "result.json":
                                parse_result_json(item_path, x_data, y_data)

    return x_data, y_data

def plot_scatter(x_data, y_data, output_pdf="scatter_plot.pdf"):
    """
    绘制散点图 (x=net_score, y=result_score)，
    并添加线性拟合（不显示公式），点使用红色并变小，
    在 y=0 的地方添加一条虚线。
    输出为 PDF 格式。
    """
    # 先过滤掉 y=0 的数据点
    filtered_x = []
    filtered_y = []
    for xx, yy in zip(x_data, y_data):
        if yy != 0:  # 跳过 result_score == 0 的点
            filtered_x.append(xx)
            filtered_y.append(yy)

    if not filtered_x:
        print("No valid data points (y != 0) found; cannot plot.")
        return

    plt.figure(figsize=(8,6))

    # 散点(点大小 s=20，颜色 red)
    plt.scatter(filtered_x, filtered_y, s=20, color="red", alpha=0.6, label="Data points")

    # 线性拟合
    x_arr = np.array(filtered_x)
    y_arr = np.array(filtered_y)
    slope, intercept = np.polyfit(x_arr, y_arr, 1)

    # 生成拟合线
    x_line = np.linspace(min(x_arr), max(x_arr), 100)
    y_line = slope * x_line + intercept
    # 绘制拟合线(不显示公式)
    plt.plot(x_line, y_line, color="blue", lw=2, label="Fit line")

    # 在 y=0 处画一条虚线(axhline)
    plt.axhline(y=0, color="black", linestyle="--", alpha=0.7)

    plt.xlabel("Net Score (Villager.total - Werewolf.total)")
    plt.ylabel("Result Score")
    # 标题加粗
    plt.title("Net Score vs. Result Score", fontweight="bold")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    # 保存为 PDF 格式
    plt.savefig(output_pdf, dpi=150, format="pdf")
    plt.show()

if __name__ == "__main__":
    # 根据你的实际根目录路径替换
    root_directory = r"werewolf_eval"

    x_data, y_data = collect_data(root_directory)
    print(f"Collected {len(x_data)} raw data points.")

    plot_scatter(x_data, y_data, "scatter_plot.pdf")

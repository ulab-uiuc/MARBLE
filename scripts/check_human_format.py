import os
import io
import pandas as pd

filename = r"human_eval\research\Zhe_human_eval_research.csv"

try:
    if filename.endswith(".csv"):
        # 先用 open() + errors="replace" 读入文本，遇到无法解码的字节会替换成 �
        with open(filename, "r", encoding="gbk", errors="replace") as f:
            file_content = f.read()
        # 用 StringIO 将文本包装给 read_csv
        df = pd.read_csv(io.StringIO(file_content))
    else:
        # 如果是 xlsx 或其他格式
        df = pd.read_excel(filename)

except Exception as e:
    print(f"读取文件 {filename} 失败: {e}")
    df = None

# 如果成功读取，就打印前几行 (head) 和基本信息
if df is not None:
    print("DataFrame 的前 40 行:")
    print(df.head(40))
    print("\nDataFrame 基本信息:")
    print(df.info())
else:
    print("DataFrame 为 None，无法输出。")

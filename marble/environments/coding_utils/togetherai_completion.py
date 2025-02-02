import os
from litellm import completion

# 设置 Together AI API 密钥
os.environ["TOGETHERAI_API_KEY"] = "43fc41168adce316bcaf13dd5fdd6db55341b4cd8ec6f8dfaee6567bffa60c31"

def generate_text(prompt):
    try:
        # 创建消息
        messages = [{"role": "user", "content": prompt}]
        
        # 调用 API 进行生成
        # 使用 Llama-2-7B-32K-Instruct 作为示例
        response = completion(
            model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=messages
        )
        
        # 提取生成的内容
        generated_text = response.choices[0].message.content
        return generated_text
    
    except Exception as e:
        print(f"生成过程中出现错误: {str(e)}")
        return None

def main():
    # 测试提示
    prompt = "请用中文写一段关于人工智能的短文。"
    
    print("开始生成内容...")
    result = generate_text(prompt)
    
    if result:
        print("\n生成的内容:")
        print(result)
    else:
        print("\n生成失败")

if __name__ == "__main__":
    main()
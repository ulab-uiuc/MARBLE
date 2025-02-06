import os
from marble.llms.model_prompting import model_prompting

def test_model():
    os.environ["AWS_ACCESS_KEY_ID"] = "AKIA4ZPZVQT7FA5CPBXR"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
    os.environ["AWS_REGION_NAME"] = "us-west-2"
    
    try:
        messages = [{
            "content": "Write me a poem about the blue sky",
            "role": "user"
        }]
        
        response = model_prompting(
            llm_model="bedrock/meta.llama3-1-8b-instruct-v1:0",
            messages=messages,
            return_num=1,
            max_token_num=2048,
            temperature=0.7,
            top_p=1.0
        )
        
        if response:
            print("\nResponse received:")
            print(response[0].content if response[0].content else "No content")
            
            # 打印 token 使用情况
            print("\nToken Usage:")
            for msg in response:
                if hasattr(msg, 'usage'):
                    print(f"Prompt tokens: {msg.usage.prompt_tokens}")
                    print(f"Completion tokens: {msg.usage.completion_tokens}")
                    print(f"Total tokens: {msg.usage.total_tokens}")
        else:
            print("\nNo response received")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Error type:", type(e))
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    test_model()
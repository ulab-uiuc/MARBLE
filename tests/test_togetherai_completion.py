import os
from litellm import completion

os.environ["TOGETHERAI_API_KEY"] = "YOUR_API_KEY"

def generate_text(prompt):
    try:
        messages = [{"role": "user", "content": prompt}]
        
        response = completion(
            model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=messages
        )
        
        generated_text = response.choices[0].message.content
        return generated_text
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def main():
    prompt = "Please write a short essay about artificial intelligence."
    
    print("Starting content generation...")
    result = generate_text(prompt)
    
    if result:
        print("\nGenerated content:")
        print(result)
    else:
        print("\nGeneration failed")

if __name__ == "__main__":
    main()
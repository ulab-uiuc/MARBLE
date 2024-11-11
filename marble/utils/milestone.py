import yaml
import time

def generate_task_milestones(task_description, client):
    """
    Generate milestones for a given task by calling the GPT tool.
    
    Args:
        task_description (str): The description of the main task to break down.
        client: The OpenAI client instance.
        
    Returns:
        list or None: Returns a list of milestones if successful, otherwise None.
    """
    
    # Load the prompt data from YAML file
    try:
        with open("marble/utils/milestone_prompt.yaml", 'r') as file:
            prompt_data = yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: milestone_prompt.yaml file not found.")
        return None
    
    # Extract system and user prompts and tool configuration
    system_prompt = prompt_data['prompts']['task_breakdown']['sys_prompt']
    user_template = prompt_data['prompts']['task_breakdown']['user']
    tool = prompt_data['tools'][0]
    
    # Format the user prompt with the task description
    user_prompt = user_template.replace("<<task_description>>", task_description)
    
    # Prepare the messages for the GPT tool call
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    
    # Define the tool call function with retry mechanism
    rounds = 0
    while rounds < 3:
        rounds += 1
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  
                messages=messages,
                tools=[tool],
                tool_choice="required",
                temperature=0.0,
                n=1,
            )
            return response.choices[0].message.tool_calls
        except Exception as e:
            print(f"Attempt {rounds}: Error in generating milestones - {e}")
            time.sleep(5)
    
    print("Error: Chat Completion failed too many times.")
    return None
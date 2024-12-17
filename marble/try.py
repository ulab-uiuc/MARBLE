from openai import OpenAI

client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    # Get the Novita AI API Key by referring to: https://docs/get-started/quickstart.html#_2-manage-api-key
    api_key="17fc07ac-e3e8-4bcb-85fe-cfd24f423bd5",
)

model = "meta-llama/llama-3.1-8b-instruct"
stream = True  # or False
max_tokens = 512

completion_res = client.completions.create(
    model=model,
    prompt="A chat between a curious user and an artificial intelligence assistant.\nYou are a cooking assistant.\nBe edgy in your cooking ideas.\nUSER: How do I make pasta?\nASSISTANT: First, boil water. Then, add pasta to the boiling water. Cook for 8-10 minutes or until al dente. Drain and serve!\nUSER: How do I make it better?\nASSISTANT:",
    stream=stream,
    max_tokens=max_tokens,
)

if stream:
    for chunk in completion_res:
        print(chunk.choices[0].text or "", end="")
else:
    print(completion_res.choices[0].text)

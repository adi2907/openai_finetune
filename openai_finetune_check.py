import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Check if the API key is being loaded correctly
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key not found in environment variables")
model_name = os.getenv("OPENAI_FINE_TUNED_MODEL")
# Set API key
client = OpenAI(
    api_key=api_key,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "A state government introduces a scheme to promote electric vehicle (EV) adoption. Under this scheme, EV manufacturers receive a fixed amount for each vehicle sold. Should this amount be considered a subsidy or an incentive for GST purposes?Will it be taxable? Explain your reasoning",
        }
    ],
    model=model_name,
)

print(chat_completion.choices[0].message.content)

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if the API key is being loaded correctly
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API Key not found in environment variables")

from openai import OpenAI

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)


# Prepare the dataset file path
training_file_path = "corrected_fine_tune.jsonl"

# Upload the file for fine-tuning
with open(training_file_path, "rb") as f:
    response = client.files.create(
        file=f,
        purpose="fine-tune"
    )
# Start fine-tuning with the uploaded file
fine_tune_response = client.fine_tuning.jobs.create(
    model="gpt-4o-mini-2024-07-18",
    training_file=response.id
)

# Output the fine-tuning job details
print(fine_tune_response)


# ChatGPT Fine-Tuning for Legal Reasoning: Working on GST case dataset

## Introduction

This project demonstrates how to fine-tune a ChatGPT model (specifically GPT-4o-mini) to improve its legal reasoning capabilities using a custom dataset of GST (Goods and Services Tax) appellate judgements.

## Background

The inspiration for this project came from a personal experience with a GST-related legal issue. While ChatGPT could summarize the problem, it couldn't provide specific legal advice or precedents. This led to the idea of fine-tuning ChatGPT to reason more like a lawyer.

## Approach

The fine-tuning process consists of four main steps:

1. Data Collection
2. Dataset Creation
3. Model Selection and Fine-Tuning
4. Testing and Evaluation

### 1. Data Collection

- Source: GST appellate judgements from [GST Council website](https://www.gstcouncil.gov.in/appellate-orders)
- Process: Downloaded PDFs and converted to text using OCR

### 2. Dataset Creation

- Format: Conversational Q&A pairs in JSONL format
- Method: Used ChatGPT to generate synthetic data, focusing on legal reasoning
- Prompt Example:
  ```
  Here's a GST Judgement attached. 
  • Generate a set of question-and-answer (Q&A) pairs focusing on the legal reasoning and principles applied in the judgment.
  • Create hypothetical scenarios where similar legal reasoning would apply.
  • Important: Include a final takeaway Q&A like 'What is the key takeaway from this ruling for businesses manufacturing etc"
  ```

### 3. Model Selection and Fine-Tuning

- Model: GPT-4o-mini
- Platform: OpenAI API
- Code snippet for fine-tuning:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Check if the API key is being loaded correctly
api_key = os.getenv("OPENAI_API_KEY")

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
```

### 4. Testing and Evaluation

Given a judgement which was fed as a dataset


A cooperative bank sought to classify performance-based incentives received under a government loan scheme as tax-exempt subsidies. The Gujarat Appellate Authority for Advance Ruling rejected this claim, ruling that these incentives were taxable under GST as consideration for services rendered, not subsidies.

Compared responses from the base model and fine-tuned model using a sample scenario based on the above judgement

**Scenario**: A state government introduces a scheme to promote electric vehicle (EV) adoption. Under this scheme, EV manufacturers receive a fixed amount for each vehicle sold. Should this amount be considered a subsidy or an incentive for GST purposes?

**Base Model Response**: Likely considered subsidies, not incentives. Not included in taxable value for GST calculations.

**Fine-tuned Model Response**: Considered an incentive, not a subsidy. Taxable under GST as it's paid directly to suppliers without reducing consumer prices.

The fine-tuned model demonstrated improved legal reasoning aligned with GST appellate judgements.

## Conclusion

This project shows promising results in enhancing ChatGPT's legal reasoning capabilities through fine-tuning. However, further training and reinforcement learning may be necessary for more consistent and precise legal analysis.

## Future Work

- Expand the dataset with more diverse legal cases
- Experiment with different fine-tuning techniques and models especially on open source LLMs


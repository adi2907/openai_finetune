TLDR: In this short intro to ChatGPT fine-tuning, I show how a 4o-mini model can become better in legal reasoning using my own custom dataset. The fine-tuned model having learnt from a legal dataset is better able to analyse new questions.

A 30-page GST letter about my former startup arrived, threatening legal action over a 6-year-old service tax issue. As any engineer, using OCR and ChatGPT, figured it related to a service tax exemption (even though all docs were submitted earlier). Though the original amount was small, interest had inflated it. This seems part of an effort by the humble taxman to resolve old cases before a Supreme Court deadline, targeting small businesses to boost government revenue.

Well ChatGPT did summarise the issue with the caveat that I need to consult with a tax lawyer. It also didn't tell me if I'm in the wrong or right on this case and if there are any precedents to help me. It got me thinking - why isn't the best model yet able to give basic advice on legal cases the same way it freely dispenses advice on medical cases.

I thought let me try and make ChatGPT reason like a lawyer.To improve it, typically two methods are used - fine-tuning and RAG. Think of fine-tuning as sending AI to law school. We'll feed a ton of legal documents and cases and it'd come out speaking legalese. In contrast, RAG is more like giving the Large Language Model (LLM) a smart legal assistant instead of cramming that knowledge into its brain. I chose the first approach viz making ChatGPT a lawyer

Now within fine-tuning also multiple approaches are there - both in models (open source LLama vs closed source ChatGPT/Claude) and platforms (Colab, Unsloth, Local system). As a base case, I typically use fine-tuning on ChatGPT itself to get started as its straightforward and one can uncover gains pretty quickly.

Fine-tuning on ChatGPT is a 4 part process 
1. Get the data or documents you want to fine-tune with 
2. Build a  dataset of Q&A pairs from the documents
3. Choose a ChatGPT model and run fine-tuning
4. Test it against some same questions

1. Get the data or documents you want to fine-tune with 
I have used the appellate judgements of GST case laws published on the website to get all the judgements in the last year https://www.gstcouncil.gov.in/appellate-orders
One can download all the pdfs. I have uploaded the summary of the judgements here.  These are scanned documents and I have shared a simple OCR code to convert them into docx format for easier readability

2. Build a  dataset of Q&A pairs from the documents
One needs to build a conversational assistant type dataset in the format from the judgements
```
{"messages": [{"role": "user", "content": "What was the main issue in the case"}, {"role": "assistant", "content": "The main issue was the classification of the product 'Crackle' for GST purposes"}]}
```

The best way to generate this dataset will be to use chatgpt itself to generate them using the judgements. Its called 'synthetic data generation' and is the default method for building LLMs. 

However the prompt to generate the dataset is tricky as I want the LLM to reason like a lawyer not become a parrot. In which case, fine-tuning doesn't make sense. Finally homed into a prompt, key parts are mentioned below

```
Here’s a GST Judgement attached. 

• Generate a set of question-and-answer (Q&A) pairs focusing on the legal reasoning and principles applied in the judgment.
• Create hypothetical scenarios where similar legal reasoning would apply.
• Important: Include a final takeaway Q&A like ‘What is the key takeaway from this ruling for businesses manufacturing etc”
```

This gave reasonably good dataset mainly focussing on reasoning. Converted to jsonl format which is used by openai to finetune. Can check the entire dataset here and the judgement summaries here

3. Choose a ChatGPT model and run fine-tuning
This is always the easier part once the data is ready. One will need an Openai API key. I chose GPT -4o-mini for the model. The following 10 lines of code will help you create a custom LLM. Always blows my mind to how easy all code has become 

```
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

4. Test it against some same questions
Once the fine-turning is done - took some 10 min for me - lets try feeding both the base model and fine-tuned model the same questions.

Here is a judgement summary


A cooperative bank sought to classify performance-based incentives received under a government loan scheme as tax-exempt subsidies. The Gujarat Appellate Authority for Advance Ruling rejected this claim, ruling that these incentives were taxable under GST as consideration for services rendered, not subsidies. Link here

Here's a question am posing to both the base models and finetuned models
A state government introduces a scheme to promote electric vehicle (EV) adoption. Under this scheme, EV manufacturers receive a fixed amount for each vehicle sold. Should this amount be considered a subsidy or an incentive for GST purposes? Explain your reasoning.

The answer - based on the judgement should be - 'classified as incentive and hence taxable'

Here's the response from the base model
Fixed payments to EV manufacturers under a government scheme are likely considered subsidies, not incentives, for GST purposes. As subsidies, these payments would not be included in the taxable value for GST calculations and are generally not subject to GST.

Now here's the response from the fine-tuned model
Under GST law, subsidies reduce consumer costs, while incentives reward suppliers for meeting targets. The payment to EV manufacturers is considered an incentive, not a subsidy, as it's paid directly to suppliers without reducing consumer prices.

Clearly the fine-tuned model is able to identify the issue better having gained some experience with the appellate judgement. This is very exciting and shows how with a reasonably good dataset, LLMs can start thinking like lawyers. However LLMs are notoriously imprecise and keep changing their answers hence a lot of training data with reinforcement learning etc needs to be used. But as a starting point, this shows quite a bit of promise

import requests
import json
import re
import os
from dotenv import load_dotenv
from structuredAgent import structuredAgent
from llmconnector import connector
from unstructuredAgent import search_documents


# Load env vars from .env file
load_dotenv()

# Read the variables
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")


# Step 1: User input
user_input = input(" Enter your medical question or story: ")

# Step 2: Formulate the prompt with richer examples
prompt = f"""
You are a classifier that determines whether a user question for a university chatbot is about "structured" data, "unstructured" information, or a "hybrid" of both.

Your task is to output ONLY one of these three categories wrapped inside <final_answer> tags:
- structured → questions about data stored in structured databases like timetables, bus schedules, or cafe menus.
- unstructured → questions about university policies, procedures, or general information found in documents or FAQs.
- hybrid → questions containing both structured and unstructured information requests in the same input.

Examples:
- "What time is the math lecture on Monday?" → <final_answer>structured</final_answer>
- "When is the bus arriving at the main gate?" → <final_answer>structured</final_answer>
- "What is today's cafe menu?" → <final_answer>structured</final_answer>
- "What are the exam dates for this semester?" → <final_answer>structured</final_answer>

- "How do I apply for medical leave if I missed an exam?" → <final_answer>unstructured</final_answer>
- "Who do I contact for scholarship information?" → <final_answer>unstructured</final_answer>
- "What are the rules for exam conduct?" → <final_answer>unstructured</final_answer>
- "Can I take a leave of absence for personal reasons?" → <final_answer>unstructured</final_answer>
- "What is the process for requesting disability accommodations?" → <final_answer>unstructured</final_answer>
- "What is the grading policy for this course?" → <final_answer>unstructured</final_answer>
- "What is the procedure for requesting a transcript?" → <final_answer>unstructured</final_answer>
- "What are the requirements for graduation?" → <final_answer>unstructured</final_answer>
- "What topics are covered in the DSA module?" → <final_answer>unstructured</final_answer>

- "When is the next chemistry exam and how do I request a medical leave?" → <final_answer>hybrid</final_answer>
- "I missed my exam last week because of illness. When is the makeup exam scheduled?" → <final_answer>hybrid</final_answer>
- "What time is the bus coming, and what documents do I need to graduate?" → <final_answer>hybrid</final_answer>
- "Is the cafeteria open late on exam days and who do I contact for disability accommodations?" → <final_answer>hybrid</final_answer>
- "When is the next bus and what is the grading policy?" → <final_answer>hybrid</final_answer>

Now classify this input:
"{user_input}"

"""

# Step 3: Send request to LLM
response = connector(prompt)

# Step 4: Parse and extract classification
result = response.json()
raw_output = result.get("response", "")

# Print raw output for debugging
# print("\n📦 Raw LLM Output:\n", raw_output)

# Step 5: Extract <final_answer>
match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)




# --------- AGENT FUNCTIONS --------- 
def call_structured_agent(user_input):
    print("\n🤖 [structured AGENT]: Answering structured question...")
    res=structuredAgent(user_input)  # Call the structured agent function
    print("\n✅ Structured Agent Response:\n", res)
    

def call_unstructured_agent(user_input):
    print("\n [unstructured AGENT]: Understanding symptoms and reasoning...")
    response= search_documents(user_input)  # Call the unstructured agent function
    print("\n✅ Unstructured Agent Response:\n", response)

def call_hybrid_agent(user_input):
    print("\n🔀 [HYBRID AGENT]: Handling both symptom story and question...")
    # You can call both agents or do smarter hybrid logic
  





if match:
    final_answer = match.group(1).strip()
    print("\n✅ Final Answer Extracted:")
    print(final_answer)

# --------- ROUTING TO AGENTS ---------
    if final_answer == "structured":
        call_structured_agent(user_input)
    elif final_answer == "unstructured":
        call_unstructured_agent(user_input)
    elif final_answer == "hybrid":
        call_hybrid_agent(user_input)
    else:
        print("⚠️ Unknown classification.")
else:
    print("\n❌ No <final_answer> tag found in the response.")



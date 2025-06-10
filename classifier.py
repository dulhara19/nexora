import requests
import json
import re
import os
from dotenv import load_dotenv
from meditron import calling_meditron 
from llmagent import calling_llmagent
from neragent import calling_neragent
from app import MedicalKG

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
- "How do I apply for medical leave if I missed an exam?" → <final_answer>unstructured</final_answer>
- "Who do I contact for scholarship information?" → <final_answer>unstructured</final_answer>
- "What are the rules for exam conduct?" → <final_answer>unstructured</final_answer>
- "Can I take a leave of absence for personal reasons?" → <final_answer>unstructured</final_answer>

- "When is the next chemistry exam and how do I request a medical leave?" → <final_answer>hybrid</final_answer>
- "I missed my exam last week because of illness. When is the makeup exam scheduled?" → <final_answer>hybrid</final_answer>
- "What time is the bus coming, and what documents do I need to graduate?" → <final_answer>hybrid</final_answer>
- "Is the cafeteria open late on exam days and who do I contact for disability accommodations?" → <final_answer>hybrid</final_answer>
- "When is the next bus and what is the grading policy?" → <final_answer>hybrid</final_answer>

Now classify this input:
"{user_input}"

"""

# Step 3: Send request to LLM
url = 'http://localhost:11434/api/generate'
headers = {'Content-Type': 'application/json'}
data = {
    'model': 'deepseek-r1:8b',
    'prompt': prompt,
    'stream': False,  # Not using streaming
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# Step 4: Parse and extract classification
result = response.json()
raw_output = result.get("response", "")

# Print raw output for debugging
print("\n📦 Raw LLM Output:\n", raw_output)

# Step 5: Extract <final_answer>
match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)




# # --------- AGENT FUNCTIONS --------- 
# def info_question_agent(user_input):
#     print("\n🤖 [INFO AGENT]: Answering factual medical question...")
    
#     answer = calling_meditron(user_input)
#     print(f"🔍 Processing info question: '{user_input}'")
#         # Here you would call your Meditron model or any other LLM to get the answer
#         # For now, we just simulate a response
#     print(answer)
    

# def symptom_story_agent(user_input):
#     print("\n🧬 [SYMPTOM AGENT]: Understanding symptoms and reasoning...")
#     answer=calling_llmagent(user_input)
#     entities=calling_neragent(answer)
#     # ✅ Create instance of MedicalKG before calling the method
#     kg = MedicalKG(uri="bolt://localhost:7687", user="neo4j", password=PASSWORD)
    
#     dis = kg.get_diseases_by_symptoms(entities)
#     print(f"🩺 Diagnosing from: '{user_input}'")
#     print(f"💡 Extracted entities: {entities}")
#     print(f"🔬 possible diseas: {dis}")


# def hybrid_agent(user_input):
#     print("\n🔀 [HYBRID AGENT]: Handling both symptom story and question...")
#     # You can call both agents or do smarter hybrid logic
#     info_question_agent(user_input)
#     symptom_story_agent(user_input)





if match:
    final_answer = match.group(1).strip()
    print("\n✅ Final Answer Extracted:")
    print(final_answer)

# # --------- ROUTING TO AGENTS ---------
#     if final_answer == "info_question":
#         info_question_agent(user_input)
#     elif final_answer == "symptom_story":
#         symptom_story_agent(user_input)
#     elif final_answer == "hybrid":
#         hybrid_agent(user_input)
#     else:
#         print("⚠️ Unknown classification.")
# else:
#     print("\n❌ No <final_answer> tag found in the response.")



import json
import re
from structuredAgent import structuredAgent
from llmconnector import connector
from unstructuredAgent import search_documents
from hybridresponsecreator import hybridresponsecreator
from datetime import datetime

date_time=datetime.now() 

def hybridclassifier(user_input):
    prompt = f"""You are a highly intelligent university chatbot preprocessor. A user may ask story-like hybrid questions that contain multiple sub-questions. Your task is to:

1. Analyze the input and break it down into individual **structured** and **unstructured** questions.
2. Output a **JSON object** with two keys:
    - "structured": a list of structured questions (only about bus schedules, timetables, cafe menus)
    - "unstructured": a list of unstructured questions (about university policies, modules, procedures, staff, etc.)

📌 Example:

Input: "tell me the lunch menu today, when is the OOP class, and how can I apply for leave?"
Output:
{{
  "structured": [
    "What is the lunch menu today?",
    "When is the OOP class?"
  ],
  "unstructured": [
    "How can I apply for leave?"
  ]
}}

Input: "{user_input}"
Now return only a valid JSON object with double quotes on keys and values. No explanations, only the JSON.
"""

    response = connector(prompt)
    result = response.json()
    raw_output = result.get("response", "")
    # print("🔍 Raw LLM Output:\n", raw_output)

    # ✅ Extract only the JSON block using more precise pattern
    match = re.search(r"{[\s\S]*?}", raw_output)
    if not match:
        return {"error": "No JSON found in LLM response."}

    json_block = match.group(0).strip()

    try:
        parsed = json.loads(json_block)
        structured_questions = parsed.get("structured", [])
        unstructured_questions = parsed.get("unstructured", [])
        
        print("\n🔍 Structured Questions:", structured_questions)
        print("🔍 Unstructured Questions:", unstructured_questions)

        structured_answers = []
        for q in structured_questions:
            print(f"\n✅ Structured Q: {q}")
            structured_answers.append(structuredAgent(q))


        unstructured_answers = []
        for q in unstructured_questions:
            print(f"\n✅ Unstructured Q: {q}")
            unstructured_answers.append(search_documents(q))
        
        response=hybridresponsecreator(structured_questions,unstructured_questions, structured_answers,unstructured_answers,date_time)
        
        result = response.json()
        raw_output = result.get("response", "")
       
      #----debugging output
      # Print raw output for debugging
      # print("\n✅ Raw LLM Output:\n", raw_output)


      # Step 5: Extract <final_answer>
        match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)
        if match:
          final_answer = match.group(1).strip()
          print("\n✅ Final Answer Extracted from hybrid Agent")
    
          return final_answer

    except json.JSONDecodeError as e:
        return {"error": f"JSON decoding failed: {str(e)}"}


# res_from_hybridagent=hybridclassifier("what is the lunch menu today, when is the OOP class, and how can I apply for leave? and also tell me who is the head of the computer science department?")

# print("✅final question response object: ",res_from_hybridagent)
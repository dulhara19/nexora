import re
from structuredAgent import structuredAgent
from llmconnector import connector
from unstructuredAgent import search_documents
from vectorresponsecreator import create_response_from_semantic_context

def hybridclassifier(user_input):

 prompt = f"""
You are a highly intelligent AI system designed to analyze and understand educational queries. A user may ask hybrid story type questions containing unstructured and structured questions. Your job is to:

    Identify the parts in query for structured, unstructured. For structured questions are only about time tables, bus schedules, or cafe menus, Unstructured questions are more open-ended and may involve reasoning or storytelling such as university policies, procedures, modules, subjects, degree or general information(not included :timetables,cafe menus, bus schedules)

    - split the input into two clear questions:

        - Wrap the structured one inside <structured>...</structured>

        - Wrap the unstructured one inside <unstructured>...</unstructured>

    - If the input is purely structured, just wrap the entire question with <structured> tags.

    - If the input is purely unstructured, wrap it with <unstructured> tags.

    - DO NOT provide answers — just return the properly tagged questions.

Examples:

Hybrid Input:
"tell me what is the bus schedule today and What is the module code for OOP and who is Ms Yasanthika at NSBM?"
✅ Output:

<structured>what is the bus schedule today?</structured>  
<unstructured>What is the module code for OOP?,Who is Ms Yasanthika at NSBM?</unstructured>  

Hybrid Input:
"tell me when the bus to kadawatha arraiving at the main gate and Give me the duration and credits of the DSA module"
✅ Output:

<structured>when the bus to kadawatha arraiving at the main gate?</structured>  
<unstructured>Give me the duration and credits of the DSA module?</unstructured>  

Hybrid Input:
"Can you guide me on how to approach algorithm problems? plus tell me what is the cafe menu for today"
✅ Output:

<unstructured>Can you guide me on how to approach algorithm problems?,what is the cafe menu for today</unstructured> 
<structured>what is the cafe menu for today?</structured>
Now classify this input:
"{user_input}"

"""

    # Send request to LLM
 response = connector(prompt)

    # Parse and extract classification
 result = response.json()
 raw_output = result.get("response", "")

    # debugging---
    # Print raw output for debugging
    # print("\n📦 Raw LLM Output:\n", raw_output)

    # Extract <final_answer>
 match1 = re.search(r"<structured>\s*(.*?)\s*</structured>", raw_output, re.DOTALL | re.IGNORECASE)

 match2 = re.search(r"<unstructured>\s*(.*?)\s*</unstructured>", raw_output, re.DOTALL | re.IGNORECASE)

 if match1:
        structured_final_answer = match1.group(1).strip()
        print("\n✅structured Final Answer Extracted from hybrid classifier:")
        print(structured_final_answer)
        final_structured_res=structuredAgent(structured_final_answer)
        print("\n✅ Structured Agent Response:\n", final_structured_res)
 else:
        final_structured_res = "No structured question found."    

 if match2:
        unstructured_final_answer = match1.group(1).strip()
        print("\n✅unstructured Final Answer Extracted from hybrid classifier:")
        print(unstructured_final_answer)
        res2= search_documents(unstructured_final_answer)
        final_unstructured_res=create_response_from_semantic_context(res2, unstructured_final_answer, "current_time")
        print("\n✅ Unstructured Response from hybrid classifier:", final_unstructured_res)

 return f"{final_structured_res} \n {final_unstructured_res}"  # Return both structured and unstructured responses











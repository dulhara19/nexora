import re
from structuredAgent import structuredAgent
from llmconnector import connector
from unstructuredAgent import search_documents
from vectorresponsecreator import create_response_from_semantic_context

def hybridclassifier(user_input):

 prompt = f"""
You are a highly intelligent AI system designed to analyze and understand educational queries. A user may ask structured, unstructured, or hybrid questions. Your job is to:

    Identify if the query is structured, unstructured, or a hybrid of both.

    If it’s hybrid, split the input into two clear questions:

        Wrap the structured one inside <structured>...</structured>

        Wrap the unstructured one inside <unstructured>...</unstructured>

    If the input is purely structured, just wrap the entire question with <structured> tags.

    If the input is purely unstructured, wrap it with <unstructured> tags.

    Maintain original language (Sinhala, Tamil, or English) when wrapping, do not translate.

    DO NOT provide answers — just return the properly tagged questions.

Examples:

Hybrid Input:
"What is the module code for OOP and how can I get better at programming?"
✅ Output:

<structured>What is the module code for OOP?</structured>  
<unstructured>How can I get better at programming?</unstructured>  

Structured Input:
"Give me the duration and credits of the DSA module"
✅ Output:

<structured>Give me the duration and credits of the DSA module</structured>  

Unstructured Input:
"Can you guide me on how to approach algorithm problems?"
✅ Output:

<unstructured>Can you guide me on how to approach algorithm problems?</unstructured>  
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
        final_res=structuredAgent(structured_final_answer)
        return final_res
        

 if match2:
        unstructured_final_answer = match1.group(1).strip()
        print("\n✅unstructured Final Answer Extracted from hybrid classifier:")
        print(unstructured_final_answer)
        res2= search_documents(unstructured_final_answer)
        final_res=create_response_from_semantic_context(res2, unstructured_final_answer, "current_time")
        return final_res

 











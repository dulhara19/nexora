## MULTI AGENTIC RAG
![Alt Text](/src/images/fig2.png)
1. User Input
The process starts with the user, who can provide input either by text or voice (SST = Speech-to-Text).
2. Classifier/Router
The input is sent to the Classifier/Router.
This component determines if the question is about:
Structured data (e.g., timetables, bus schedules)
Unstructured data (e.g., policies, FAQs)
Hybrid (both types)
3. Agents
Based on classification, the router sends the query to one of three agents:
AGENT1 (Structured): Handles queries that require database access.
AGENT2 (Unstructured): Handles queries that require searching through documents using embeddings and vector similarity.
AGENT3 (Hybrid): (Planned) Handles queries that need both structured and unstructured data.
4. Structured Path
If structured, the agent queries the MySQL DB for relevant data.
The result is processed and sent to an LLM (Large Language Model) for response generation.
5. Unstructured Path
If unstructured, the agent uses an Embedding Model to encode the query.
The encoded query is used to perform a similarity search in the Vector DB (e.g., ChromaDB).
The most relevant document chunks are retrieved as context.
The context and query are sent to the LLM for response generation.
6. Hybrid Path
For hybrid queries, both structured and unstructured agents may be involved, and their outputs are combined before being sent to the LLM.
7. LLM (Large Language Model)
The LLM receives the context and query, and generates a friendly, conversational response.
8. Response
The response is returned to the user as text.
Optionally, the response can be converted to speech using TTS (Text-to-Speech) for voice output.
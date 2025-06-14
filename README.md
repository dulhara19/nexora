## Nexora University Chatbot (ADVANCED MULTI AGENTIC RAG SYSTEM)
Nexora is an AI-powered university chatbot that intelligently classifies student questions and provides answers using structured data (like timetables, bus schedules, cafe menus) or unstructured information (like policies, FAQs, and documents). It supports both text and speech input/output.

<div display="flex">
<img src="/report/fig2.png"  width="50%" alt="powerbi report"><img src="/report/fig3.png"  width="50%" alt="powerbi report"></div>

## Features
- **Multi Language Support**
Supported Sinhala,Tamil 
- **Automatic Question Classification:** Distinguishes between structured, unstructured, and hybrid queries.
- **Structured Data Agent:** Converts natural language to SQL, queries the database, and generates friendly responses.
- **Unstructured Data Agent:** Uses semantic search over documents and answers using context-aware LLM prompts.
- **Hybrid Agent (Planned):** Handles queries needing both structured and unstructured data.
- **Speech-to-Text & Text-to-Speech:** Voice input and output for accessibility.
- **FastAPI Backend:** Simple API endpoint for chatbot interaction.
---
## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dulhara19/nexora.git
   cd nexora
   

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Set up environment variables:**
   ```bash
     DB_HOST=your_host
     DB_USER=your_user
     DB_PASSWORD=your_password
     DB_NAME=your_db
   ```
4. **Start the FastAPI server:**
   ```bash
   python app.py

5. **Usage - API Endpoint:**

  ```bash
   Send a POST request to /ask with a JSON body:    
   {
     "message": "When is the next bus to Kadawatha?"
   } 
   ``` 

6. **Speech Input:**
Uncomment and use the speech_to_text() function in classifier.py for voice input.

### Notes

- **Database**:
Requires a MySQL database with tables: timetables, bus_schedules, cafe_menus.

- **Vector DB:**
Uses ChromaDB for semantic search over unstructured documents.

- **LLM:**
Connects to a local LLM API (see llmconnector.py).
- in the project deepseekr1:8b 4k used(locally setup using ollama)
- Embedding Model : all-MiniLM-L6-v2
- Built with FastAPI, ChromaDB, LangChain, Sentence Transformers, and Ollama (or compatible LLM). 

Create a .env file with your database credentials and any required API keys:

![high level architecture](/src/images/fig2.png)
for store structured data like time tables, bus schedules and cafe menus we have used MYSQL, and for other unstructured data we used CromaDB(vectordb). 

1. User Input
 - The process starts with the user, who can provide input either by text or voice (SST = Speech-to-Text).
2. Classifier/Router
- The input is sent to the Classifier/Router.
- This component determines if the question is about:
- Structured data (e.g., timetables, bus schedules)
- Unstructured data (e.g., policies, FAQs)
- Hybrid (both types)
3. Agents
- Based on classification, the router sends the query to one of - three agents:
- AGENT1 (Structured): Handles queries that require database access.
- AGENT2 (Unstructured): Handles queries that require searching through documents using embeddings and vector similarity.
- AGENT3 (Hybrid): Handles queries that need both structured and unstructured data.
4. Structured Path
- If structured, the agent queries the MySQL DB for relevant data.
The result is processed and sent to an LLM (Large Language Model) for response generation.
5. Unstructured Path
- If unstructured, the agent uses an Embedding Model to encode the query.
- The encoded query is used to perform a similarity search in the Vector DB (e.g., ChromaDB).
- The most relevant document chunks are retrieved as context.
- The context and query are sent to the LLM for response generation.
6. Hybrid Path
- For hybrid queries, both structured and unstructured agents may be involved, and their outputs are combined before being sent to the LLM.
7. LLM (Large Language Model)
- The LLM receives the context and query, and generates a friendly, conversational response.
8. Response
- The response is returned to the user as text.
Optionally, the response can be converted to speech using TTS (Text-to-Speech) for voice output.

---
to see furthur details please check report folder :)


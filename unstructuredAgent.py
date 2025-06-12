import chromadb
import uuid
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import CharacterTextSplitter
from vectorresponsecreator import create_response_from_semantic_context 
from datetime import datetime
import re

current_time = datetime.now().time() 

# ✅ Create persistent Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # ← THIS IS THE FIX

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def upload_documents(file_paths, collection_name="unistructured"):
    collection = chroma_client.get_or_create_collection(name=collection_name)
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            full_text = f.read()
            chunks = text_splitter.split_text(full_text)
            embeddings = embedding_model.encode(chunks).tolist()
            ids = [str(uuid.uuid4()) for _ in chunks]
            collection.add(documents=chunks, embeddings=embeddings, ids=ids)

    print(f"✅ Uploaded {len(file_paths)} file(s) into collection '{collection_name}'")

# handling raw output into llm friendly output-----
def format_chroma_results(raw_results, top_k: int = 3, distance_cutoff: float = 1.2) -> str:
    """
    Convert Chroma `collection.query()` output into a single plain-text context
    for the LLM.

    Args:
        raw_results (dict): The dict returned by `collection.query`.
        top_k (int): How many chunks to keep (already sorted by similarity).
        distance_cutoff (float): Drop chunks whose distance is above this value.

    Returns:
        str: Cleaned context, chunks separated by `\n\n---\n\n`
    """
    cleaned_chunks = []
    docs      = raw_results["documents"][0]
    distances = raw_results["distances"][0]

    for doc, dist in zip(docs[:top_k], distances[:top_k]):
        if dist <= distance_cutoff:
            # Strip excess whitespace, keep original new-lines inside each chunk
            chunk = "\n".join(line.strip() for line in doc.splitlines() if line.strip())
            cleaned_chunks.append(chunk)

    return "\n\n---\n\n".join(cleaned_chunks) if cleaned_chunks else "NO_RELEVANT_CONTEXT"


def search_documents(query, collection_name="unistructured", top_k=3):
    collection = chroma_client.get_collection(name=collection_name)
    query_embedding = embedding_model.encode([query])[0]
    context = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    formatted_context=format_chroma_results(context)

    #----debugging output
    # print(formatted_context)
    # for i, doc in enumerate(context["documents"][0]):
    #     print(f"\nResult {i+1}:\n{doc}")

    response_from_llm=create_response_from_semantic_context(formatted_context,query,current_time)
    result = response_from_llm.json()
    raw_output = result.get("response", "")
       
      #----debugging output
      # Print raw output for debugging
      # print("\n✅ Raw LLM Output:\n", raw_output)

      # Step 5: Extract <final_answer>
    match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)
    if match:
        final_answer = match.group(1).strip()
        print("\n✅ Final Answer Extracted:")
        # print(final_answer)
    return final_answer         


# upload_documents(["./src/text_files/"]) # ✅ Use relative or full path
# search_documents("Complexity Analysis (Big-O) covered in the DSA module?")

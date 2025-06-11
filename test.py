import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import CharacterTextSplitter
import uuid

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

def search_documents(query, collection_name="unistructured", top_k=3):
    collection = chroma_client.get_collection(name=collection_name)
    query_embedding = embedding_model.encode([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    for i, doc in enumerate(results["documents"][0]):
        print(f"\nResult {i+1}:\n{doc}")

# upload_documents(["./src/text_files/dsa.txt"])  # ✅ Use relative or full path
# search_documents("What topics are covered in the DSA module?")

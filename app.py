# app.py (new file)
from fastapi import FastAPI, Request
from pydantic import BaseModel
from classifier import classify_and_route  # wrap your classifier logic as a function

app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    result = classify_and_route(query.message)
    return {"response": result}

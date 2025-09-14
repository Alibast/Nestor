from fastapi import FastAPI
from pydantic import BaseModel
from nestor.dialogue.manager import DialogueManager

app = FastAPI(title="Nestor API")
dm = DialogueManager()

class Query(BaseModel):
    message: str
    chakra: str | None = None

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/respond")
def respond(q: Query):
    return {"reply": dm.respond(q.message)}

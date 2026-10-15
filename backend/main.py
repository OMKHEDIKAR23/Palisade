from fastapi import FastAPI
from pydantic import BaseModel
from backend.services.memory_graph import add_memory, get_memories
from backend.services.defense import quarantine_memory
from backend.services.detector import detect_threat
from backend.services.guard import guard_memory
from backend.services.memory_graph import link_derived_memory
from backend.services.memory_graph import trace_derived_memories


app = FastAPI(title="Palisade")


class MemoryInput(BaseModel):
    content: str
    source: str
    trust: float = 1.0


@app.get("/")
def home():
    return {"message": "Palisade is running"}


@app.get("/health")
def health():
    return {"api": "healthy"}


@app.post("/memories")
def create_memory(memory: MemoryInput):
    return add_memory(memory.content, memory.source, memory.trust)


@app.get("/memories")
def list_memories():
    return get_memories()

@app.post("/memories/{memory_id}/quarantine")
def quarantine(memory_id: str, reason: str):
    return quarantine_memory(memory_id, reason)

@app.post("/memories/scan")
def scan_memory(content: str):
    return detect_threat(content)

@app.post("/memories/guard")
def guarded_memory(memory: MemoryInput):
    return guard_memory(memory.content, memory.source, memory.trust)

@app.post("/memories/link")
def link_memories(parent_id: str, child_id: str):
    return link_derived_memory(parent_id, child_id)

@app.get("/memories/{memory_id}/derived")
def trace_memories(memory_id: str):
    return trace_derived_memories(memory_id)
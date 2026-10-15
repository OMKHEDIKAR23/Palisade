from backend.services.detector import detect_threat
from backend.services.defense import quarantine_cascade
from backend.services.memory_graph import add_memory


def guard_memory(content: str, source: str, trust: float = 1.0):
    threat = detect_threat(content)

    if threat["suspicious"]:
        memory = add_memory(content, source, trust)

        quarantine = quarantine_cascade(
            memory["id"],
            threat["reason"],
        )

        return {
            "blocked": True,
            "threat": threat,
            "quarantine": quarantine,
        }

    memory = add_memory(content, source, trust)

    return {
        "blocked": False,
        "memory": memory,
    }
from falkordb import FalkorDB

db = FalkorDB(host="localhost", port=6379)
graph = db.select_graph("palisade")


def quarantine_memory(memory_id: str, reason: str):
    result = graph.query(
        """
        MATCH (m:Memory {id: $id})
        SET m.status = 'quarantined',
            m.quarantine_reason = $reason
        RETURN m.id, m.status
        """,
        {"id": memory_id, "reason": reason},
    )

    if not result.result_set:
        return {"error": "Memory not found"}

    return {
        "id": result.result_set[0][0],
        "status": result.result_set[0][1],
        "reason": reason,
    }
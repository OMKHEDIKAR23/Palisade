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

def quarantine_cascade(memory_id: str, reason: str):
    result = graph.query(
        """
        MATCH (root:Memory {id: $id})
        OPTIONAL MATCH (root)-[:DERIVED_INTO*1..10]->(child:Memory)
        WITH collect(DISTINCT root) + collect(DISTINCT child) AS memories
        UNWIND memories AS m
        SET m.status = 'quarantined',
            m.quarantine_reason = $reason
        RETURN collect(m.id)
        """,
        {"id": memory_id, "reason": reason},
    )

    if not result.result_set or not result.result_set[0][0]:
        return {"error": "Memory not found"}

    return {
        "quarantined_ids": result.result_set[0][0],
        "reason": reason,
    }
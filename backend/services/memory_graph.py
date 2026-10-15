from uuid import uuid4
from falkordb import FalkorDB

db = FalkorDB(host="localhost", port=6379)
graph = db.select_graph("palisade")


def add_memory(content: str, source: str, trust: float = 1.0):
    memory_id = str(uuid4())

    graph.query(
        """
        MERGE (s:Source {name: $source})
        CREATE (m:Memory {
            id: $id,
            content: $content,
            trust: $trust,
            status: 'active'
        })
        CREATE (m)-[:ORIGINATED_FROM]->(s)
        """,
        {
            "id": memory_id,
            "content": content,
            "source": source,
            "trust": trust,
        },
    )

    return {"id": memory_id, "status": "stored"}


def get_memories():
    result = graph.query(
        """
        MATCH (m:Memory)-[:ORIGINATED_FROM]->(s:Source)
        RETURN m.id, m.content, s.name, m.trust, m.status
        """
    )

    return [
        {
            "id": row[0],
            "content": row[1],
            "source": row[2],
            "trust": row[3],
            "status": row[4],
        }
        for row in result.result_set
    ]

def link_derived_memory(parent_id: str, child_id: str):
    result = graph.query(
        """
        MATCH (parent:Memory {id: $parent_id})
        MATCH (child:Memory {id: $child_id})
        MERGE (parent)-[:DERIVED_INTO]->(child)
        RETURN parent.id, child.id
        """,
        {
            "parent_id": parent_id,
            "child_id": child_id,
        },
    )

    if not result.result_set:
        return {"error": "Parent or child memory not found"}

    return {
        "parent_id": result.result_set[0][0],
        "child_id": result.result_set[0][1],
        "relationship": "DERIVED_INTO",
    }

def trace_derived_memories(memory_id: str):
    result = graph.query(
        """
        MATCH (parent:Memory {id: $id})-[:DERIVED_INTO*1..10]->(child:Memory)
        RETURN DISTINCT child.id, child.content, child.status
        """,
        {"id": memory_id},
    )

    return [
        {
            "id": row[0],
            "content": row[1],
            "status": row[2],
        }
        for row in result.result_set
    ]
from knowledge_base.build_knowledge_base import KnowledgeBaseBuilder

def test_merge_records():
    builder = KnowledgeBaseBuilder()


    chunks = [
        {
            "chunk_id": "CHUNK000001",
            "content": "What is Python?"
        }
    ]

    metadata = [
        {
            "chunk_id": "CHUNK000001",
            "document_id": "DOC000001",
            "topic": "python"
        }
    ]

    result = builder.merge_records(chunks, metadata)

    assert len(result) == 1
    assert result[0]["chunk_id"] == "CHUNK000001"
    assert result[0]["document_id"] == "DOC000001"
    assert result[0]["topic"] == "python"
    assert result[0]["content"] == "What is Python?"


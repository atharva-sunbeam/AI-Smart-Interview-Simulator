from knowledge_base.metadata_builder import MetadataBuilder


def test_generate_chunk_id():
    builder = MetadataBuilder()
    assert builder.generate_chunk_id(1) == "CHUNK000001"


def test_generate_document_id():
    builder = MetadataBuilder()
    assert builder.generate_document_id(1) == "DOC000001"


def test_build_metadata_record():
    builder = MetadataBuilder()

    record = builder.build_metadata_record(
        chunk_id="CHUNK000001",
        document_id="DOC000001",
        source_type="interview_question",
        topic="python",
        content="What is Python?",
    )

    assert record["chunk_id"] == "CHUNK000001"
    assert record["document_id"] == "DOC000001"
    assert record["source_type"] == "interview_question"
    assert record["topic"] == "python"
    assert record["content"] == "What is Python?"
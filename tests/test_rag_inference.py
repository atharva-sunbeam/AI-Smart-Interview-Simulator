from rag_pipeline.rag_inference import RAGInference


def test_generate_answer():
    rag = RAGInference()

    answer = rag.generate_answer(
        query="What is Python?",
        context=["Python is a programming language."]
    )

    assert "Generated answer placeholder" in answer
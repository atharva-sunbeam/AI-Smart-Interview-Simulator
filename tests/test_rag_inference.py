from rag_pipeline.rag_inference import RAGInference


def test_generate_answer():
    rag = RAGInference()

    answer = rag.generate_answer(
        query="What is Python?",
        context=["Python is a programming language."]
    )

    assert "Generated answer placeholder" in answer


def test_build_prompt():
    rag = RAGInference()

    prompt = rag.build_prompt(
        query="What is Python?",
        context=["Python is a programming language."]
    )

    assert "Question:" in prompt
    assert "Context:" in prompt


def test_run():
    rag = RAGInference()

    assert hasattr(rag, "run")
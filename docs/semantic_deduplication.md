# Semantic Deduplication Engine

## Purpose

The Semantic Deduplication Engine removes duplicate interview questions collected from multiple sources.

Sources include:

* GeeksforGeeks
* Stack Overflow
* InterviewBit
* LeetCode
* GitHub Discussions

Since different websites often express the same concept using different wording, traditional duplicate removal techniques are insufficient.

---

# Why Exact Matching Fails

Traditional deduplication compares text literally.

Example:

```text
What is Python?

Explain Python language.

Define Python programming language.
```

Although these questions are semantically identical, exact string matching treats them as different records.

As a result:

* Duplicate questions remain.
* Knowledge base quality decreases.
* RAG retrieval becomes noisy.

---

# Why Semantic Similarity Works

Semantic similarity converts sentences into dense vector representations.

Example:

```text
Question
     ↓
Sentence Transformer
     ↓
Embedding Vector
```

Questions with similar meanings produce nearby vectors in embedding space.

Example:

```text
"What is Python?"
            ↘

      Similar Embeddings

            ↗
"Explain Python language."
```

Cosine similarity is then used to measure semantic closeness.

---

# Architecture

```text
Dataset
    ↓
Load Questions
    ↓
Sentence Transformer
    ↓
Generate Embeddings
    ↓
Cosine Similarity
    ↓
Detect Duplicates
    ↓
Remove Duplicates
    ↓
Save Clean Dataset
```

---

# Embedding Model

Model:

```text
all-MiniLM-L6-v2
```

Advantages:

* Lightweight
* Fast inference
* High semantic quality
* Widely used in production RAG systems

---

# Similarity Metric

Metric:

```text
Cosine Similarity
```

Formula:

```text
Similarity(A, B)

= (A · B)

  ─────────────
  ||A|| ||B||
```

Range:

```text
0 → Completely different

1 → Identical meaning
```

---

# Threshold Selection

Current threshold:

```text
0.90
```

Reason:

* High precision.
* Avoids accidental removal of distinct questions.
* Keeps only highly similar questions.

Examples:

```text
Similarity = 0.95

→ Remove duplicate.

Similarity = 0.55

→ Keep both questions.
```

---

# Output

Input:

```text
1000 questions
```

Output:

```text
750 unique questions
```

Benefits:

* Higher quality knowledge base
* Reduced storage
* Faster retrieval
* Improved RAG performance

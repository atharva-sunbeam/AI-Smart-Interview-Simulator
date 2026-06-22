# Dataset Quality Metrics

## Purpose

The quality of a Retrieval-Augmented Generation (RAG) system depends heavily on the quality of the underlying dataset.

Poor-quality data leads to:

* Poor retrieval
* Incorrect answers
* Duplicate embeddings
* Reduced interview quality

To ensure high-quality datasets, the following metrics will be monitored.

---

# 1. Completeness

## Definition

Measures whether the dataset contains all expected information.

## Examples

Good:

* Question present
* Proper text content
* No missing entries

Bad:

* Empty lines
* Truncated questions
* Missing content

## Why It Matters

Incomplete data reduces the amount of useful information available to the retrieval system.

---

# 2. Uniqueness

## Definition

Measures the amount of duplicate content in the dataset.

## Examples

Good:

What is Python?

What is a Python decorator?

Bad:

What is Python?

What is Python?

What is Python?

## Why It Matters

Duplicate questions:

* Waste storage
* Create duplicate embeddings
* Bias retrieval results

---

# 3. Consistency

## Definition

Measures whether the dataset follows a standard format.

## Examples

Good:

What is Python?

Explain list comprehension.

What is polymorphism?

Bad:

PYTHON

What is Python?

*** List Comprehension ***

## Why It Matters

Consistent formatting improves downstream cleaning and chunking.

---

# 4. Validity

## Definition

Measures whether entries represent genuine interview questions.

## Examples

Valid:

What is a Python generator?

Explain decorators in Python.

Invalid:

Download PDF

Resources

Conclusion

Related Articles

## Why It Matters

Invalid entries introduce noise into the knowledge base and reduce retrieval quality.

---

# Validation Metrics

The dataset validation script currently measures:

* Total Questions
* Unique Questions
* Duplicate Questions
* Duplicate Percentage
* Empty Lines
* Short Questions
* Long Questions
* Average Length

These metrics help identify issues before the cleaning pipeline begins.

---

# Future Quality Checks

Additional checks may include:

* Non-question detection
* HTML artifact detection
* URL detection
* Special character detection
* Duplicate normalization

---

# Final Decision

All datasets must pass quality validation before entering the cleaning pipeline.

Data quality issues should be fixed during the cleaning phase before embeddings are generated.

# Question Quality Rules

## Purpose

This document defines the minimum quality standards for interview questions stored in the knowledge base.

---

# Minimum Question Length

A valid question should contain at least:

* 10 characters

Examples:

Valid:

* What is Python?
* Explain Kafka.

Invalid:

* Python
* SQL
* OOPS

---

# Maximum Question Length

A valid question should not exceed:

* 500 characters

Reason:
Very long entries are often paragraphs, explanations, or improperly scraped content rather than questions.

---

# Valid Question Patterns

Questions should generally begin with one of the following patterns:

### Definition Questions

* What is ...
* What are ...

Examples:

* What is Python?
* What are generators in Python?

---

### Explanation Questions

* Explain ...
* Describe ...

Examples:

* Explain multithreading in Python.
* Describe Kafka architecture.

---

### Comparison Questions

* Difference between ...
* Compare ...
* How does ... differ from ...

Examples:

* Difference between list and tuple.
* Compare SQL and NoSQL databases.

---

### Scenario-Based Questions

* How would you ...
* How do you ...
* How can ...

Examples:

* How would you optimize a SQL query?
* How do you handle Kafka consumer failures?

---

### Technical Concept Questions

Examples:

* Define polymorphism.
* Explain ACID properties.
* Describe Spark transformations.

---

# Invalid Patterns

Remove entries that are:

### Website Navigation

* Login
* Sign Up
* Register

### Page Metadata

* Download PDF
* Resources
* Related Articles
* Conclusion

### Section Headings

* Python Interview Questions
* SQL Interview Questions
* Advanced Questions

### Empty Content

* Blank lines
* Whitespace-only entries

---

# Quality Checklist

A question is considered valid if:

* It is not empty.
* It is not navigation text.
* It is not a section heading.
* It is not duplicated.
* Length is between 10 and 500 characters.
* It contains meaningful interview-related content.

Only questions satisfying all conditions should be included in the final knowledge base.

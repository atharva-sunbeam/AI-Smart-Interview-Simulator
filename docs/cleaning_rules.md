# Data Cleaning Rules

## Purpose

This document defines the standard cleaning rules applied to collected interview questions before they are added to the knowledge base.

---

# Rule 1: Remove Non-Question Content

The following entries do not provide interview knowledge and should be removed.

### Examples

Remove:

* Download PDF
* Resources
* Conclusion
* Related Articles
* Table of Contents
* Recommended Reading
* Share Article
* Next Article
* Previous Article

---

# Rule 2: Remove Section Titles

Section headings are useful for website organization but should not be stored as interview questions.

### Examples

Remove:

* Python Interview Questions
* Python OOPS Interview Questions
* Advanced Python Interview Questions
* SQL Interview Questions
* Data Structures Interview Questions

---

# Rule 3: Remove Navigation Text

Website navigation elements should not appear in the dataset.

### Examples

Remove:

* Login
* Sign Up
* Register
* Home
* Dashboard
* Courses
* Tutorials
* Contact Us
* About Us

---

# Rule 4: Remove Empty Records

Delete blank lines and whitespace-only entries.

### Examples

Remove:

* ""
* " "
* Multiple consecutive empty lines

---

# Rule 5: Remove Duplicate Questions

Only one copy of a question should remain.

### Example

Before:

What is Python?

What is Python?

After:

What is Python?

---

# Rule 6: Normalize Formatting

* Remove leading and trailing whitespace.
* Convert multiple spaces into a single space.
* Preserve original question wording whenever possible.

---

# Rule 7: Preserve Actual Questions

Questions containing useful interview content must be retained.

### Examples

Keep:

* What is Python?
* Explain Python decorators.
* What is a list comprehension in Python?
* What are ACID properties in DBMS?
* Explain Kafka partitions.

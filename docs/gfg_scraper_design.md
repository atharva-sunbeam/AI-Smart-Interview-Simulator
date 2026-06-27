# GeeksforGeeks Scraper Design

## Purpose

The GeeksforGeeks scraper automatically collects technical interview questions and answers from GeeksforGeeks articles.

The collected data is later used for:

* Knowledge Base Creation
* RAG Retrieval
* Question Generation
* Dataset Expansion

---

# Architecture

```text
GeeksforGeeks URL
            ↓
HTTP Request
            ↓
HTML Download
            ↓
BeautifulSoup Parsing
            ↓
Question Extraction
            ↓
Answer Extraction
            ↓
Structured Dataset
            ↓
CSV Storage
```

---

# Components

## fetch_page()

Responsibilities:

* Send HTTP request
* Download webpage HTML
* Return raw HTML

Uses:

* requests

---

## extract_questions_answers()

Responsibilities:

* Parse HTML using BeautifulSoup
* Identify question headings
* Extract associated answer text
* Build structured records

Output Format:

```text
question
answer
topic
source
url
difficulty
```

---

## save_dataset()

Responsibilities:

* Create CSV dataset
* Store extracted records

Output:

```text
datasets/raw/gfg_python_qa.csv
```

---

# Parsing Logic

Typical GeeksforGeeks structure:

```html
<h2>Question?</h2>

<p>Answer paragraph</p>

<h2>Next Question?</h2>
```

Algorithm:

1. Find all h2 and h3 tags.
2. Treat headings containing '?' as questions.
3. Traverse sibling elements.
4. Stop extraction when next heading appears.
5. Store question-answer pair.

---

# HTML Structure Used

Elements:

* h2
* h3
* p
* ul
* li

These elements usually contain interview content.

---

# Limitations

1. Website HTML structure may change.
2. Dynamic JavaScript content is not supported.
3. Some answers may span multiple sections.
4. Duplicate questions may appear.
5. Anti-scraping mechanisms may block requests.

Future Improvements:

* Selenium integration
* Duplicate removal
* Automatic topic classification
* Multi-page crawling
* Difficulty prediction

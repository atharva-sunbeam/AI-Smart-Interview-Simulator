import os
import re

# Ensure output directory exists
os.makedirs("datasets/cleaned", exist_ok=True)

ROLES = ["python", "sql", "data_engineer", "ml"]

def clean_text(text):
    """
    Standardize whitespace and remove markdown styling or leading numberings.
    """
    if not text:
        return ""
    # Remove leading number patterns e.g. "1. ", "Question: ", "Q: ", "10) "
    text = re.sub(r'^(?:QUESTION\s*\d*:\s*|ANSWER\s*\d*:\s*|Q\s*:\s*|A\s*:\s*|\d+\.\s*|\d+\)\s*)', '', text, flags=re.IGNORECASE)
    # Strip markdown bold/italics
    text = re.sub(r'\*\*|__', '', text)
    # Standardize whitespace (replace multiple spaces with single space)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_file(role):
    raw_path = f"datasets/raw/{role}_questions.txt"
    cleaned_path = f"datasets/cleaned/{role}_questions.txt"
    
    if not os.path.exists(raw_path):
        print(f"Raw file not found: {raw_path}")
        return

    print(f"Cleaning raw questions for: {role}")
    
    with open(raw_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split Q&A blocks using the equal sign separator
    blocks = content.split("========================================")
    
    cleaned_blocks = []
    seen_questions = set()
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        # Split block into question and answer
        lines = block.split('\n')
        question = ""
        answer_parts = []
        
        is_answering = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Identify where the answer starts
            if re.match(r'^ANSWER\s*\d*:', line, re.IGNORECASE) or re.match(r'^A\s*:', line, re.IGNORECASE):
                is_answering = True
            
            if is_answering:
                answer_parts.append(line)
            else:
                # Accumulate question text
                if question:
                    question += " " + line
                else:
                    question = line
        
        # Clean both parts
        q_cleaned = clean_text(question)
        a_cleaned = clean_text(" ".join(answer_parts))
        
        if q_cleaned and a_cleaned:
            # Check for duplicates based on a normalized question string
            q_norm = re.sub(r'\W+', '', q_cleaned.lower())
            if q_norm not in seen_questions:
                seen_questions.add(q_norm)
                cleaned_blocks.append((q_cleaned, a_cleaned))

    # Write cleaned blocks to target file
    with open(cleaned_path, "w", encoding="utf-8") as f:
        for q, a in cleaned_blocks:
            f.write(f"Q: {q}\n")
            f.write(f"A: {a}\n")
            f.write("-" * 40 + "\n")
            
    print(f"  Processed {len(blocks)-1} raw entries. Wrote {len(cleaned_blocks)} unique cleaned entries.")

def main():
    for role in ROLES:
        process_file(role)
    print("\n[SUCCESS] Cleaning process complete.")

if __name__ == "__main__":
    main()

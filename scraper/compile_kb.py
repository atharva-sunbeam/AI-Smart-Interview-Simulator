"""
Compiles all modular JSON files under `knowledge/` into `datasets/processed/knowledge_base.csv`
for ChromaDB RAG Vector Store indexing.
"""

import os
import pandas as pd
from agents.knowledge_manager import KnowledgeManager

def compile_knowledge_base():
    print("[CompileKB] Initializing KnowledgeManager and gathering JSON question pools...")
    km = KnowledgeManager()
    df = km.export_to_dataframe()

    if df.empty:
        print("[CompileKB Warning] No questions found in knowledge base!")
        return

    output_dir = "datasets/processed"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "knowledge_base.csv")

    df.drop_duplicates(subset=["Question"], inplace=True)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print("\n" + "="*60)
    print("CONSOLIDATED KNOWLEDGE BASE SUMMARY")
    print("="*60)
    print(f"Total Rows Saved: {len(df)}")
    print("\nDistribution by Role (Top 15):")
    print(df["Role"].value_counts().head(15).to_string())
    print("\nDistribution by Difficulty:")
    print(df["Difficulty"].value_counts().to_string())
    print(f"\nSaved Compiled CSV to: {os.path.abspath(output_path)}")
    print("="*60)

if __name__ == "__main__":
    compile_knowledge_base()

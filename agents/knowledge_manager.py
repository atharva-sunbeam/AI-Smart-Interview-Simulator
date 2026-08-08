import os
import json
import random
from agents.role_catalog import get_related_roles

class KnowledgeManager:
    """
    Modular JSON Knowledge Base Manager for all Engineering Roles.
    Supports dynamic question loading, difficulty filtering, topic matching,
    and shared tech stack question retrieval.
    """
    def __init__(self, base_dir="knowledge"):
        self.base_dir = base_dir
        self._cache = {}

    def _get_role_key(self, role_name):
        """Converts human role name to clean directory key format."""
        return role_name.lower().replace(" ", "_").replace("/", "_").replace("-", "_").replace("(", "").replace(")", "").strip()

    def load_role_difficulty_json(self, role, difficulty):
        """Loads JSON question pool for a specific role and difficulty tier."""
        role_key = self._get_role_key(role)
        diff_key = difficulty.lower()

        cache_key = f"{role_key}_{diff_key}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        file_path = os.path.join(self.base_dir, role_key, f"{diff_key}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._cache[cache_key] = data
                    return data
            except Exception as e:
                print(f"[KnowledgeManager Error] Failed loading {file_path}: {e}")

        self._cache[cache_key] = []
        return []

    def get_questions_for_role(self, role, difficulty, topic=None, excluded_questions=None):
        """
        Retrieves questions matching target `role`, `difficulty`, and optional `topic`.
        Includes cross-course shared tech stack fallback querying sister roles in the same cluster.
        """
        excluded = set(excluded_questions) if excluded_questions else set()

        # Step 1: Load primary role question pool
        pool = self.load_role_difficulty_json(role, difficulty)
        candidates = []

        for q in pool:
            q_text = q.get("question", "").strip()
            if not q_text or q_text in excluded:
                continue

            q_topic = q.get("topic", "General")
            if topic:
                topic_lower = topic.lower()
                q_topic_lower = q_topic.lower()
                if topic_lower in q_topic_lower or q_topic_lower in topic_lower or any(w in q_topic_lower for w in topic_lower.split() if len(w) > 3):
                    candidates.append(q)
            else:
                candidates.append(q)

        # Step 2: Cross-Course Shared Tech Stack Pool Expansion
        # If candidates pool is low or for rich tech stack sharing, pull from sister roles
        if len(candidates) < 5:
            sister_roles = get_related_roles(role)
            for sister_role in sister_roles:
                sister_pool = self.load_role_difficulty_json(sister_role, difficulty)
                for q in sister_pool:
                    q_text = q.get("question", "").strip()
                    if not q_text or q_text in excluded:
                        continue

                    q_topic = q.get("topic", "General")
                    if topic:
                        topic_lower = topic.lower()
                        q_topic_lower = q_topic.lower()
                        if topic_lower in q_topic_lower or q_topic_lower in topic_lower or any(w in q_topic_lower for w in topic_lower.split() if len(w) > 3):
                            candidates.append(q)
                    else:
                        candidates.append(q)

                    if len(candidates) >= 15:
                        break

                if len(candidates) >= 15:
                    break

        return candidates

if __name__ == "__main__":
    km = KnowledgeManager()
    qs = km.get_questions_for_role("Data Analyst", "Easy", topic="Python")
    print(f"Loaded {len(qs)} questions for Data Analyst (Python topic) including sister course pools.")

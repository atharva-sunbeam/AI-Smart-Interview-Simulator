import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))


class LLMFactory:
    """
    Centralized LLM Factory serving both LangChain and CrewAI model instances.
    Provides automatic failover: Groq API -> Local Ollama Server -> Fallback Heuristics.
    """
    GROQ_DEFAULT_MODEL = "openai/gpt-oss-120b"
    OLLAMA_DEFAULT_MODEL = "llama3.1:latest"
    
    def __init__(self, provider="auto", model_name=None, api_key=None, host="http://localhost:11434"):
        self.provider = provider
        self.model_name = model_name or self.GROQ_DEFAULT_MODEL
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")
        self.host = host
        self.active_provider = "offline"
        self._detect_provider()

    def _detect_provider(self):
        # 1. Test Groq API connectivity if key exists
        if self.api_key:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            models_to_test = [self.model_name, "openai/gpt-oss-120b", "groq/compound", "qwen/qwen3.6-27b"]
            for model in models_to_test:
                payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
                try:
                    res = requests.post(url, headers=headers, json=payload, timeout=4)
                    if res.status_code == 200:
                        self.active_provider = "groq"
                        self.model_name = model
                        print(f"[LLMFactory] Configured Groq API ({self.model_name}).")
                        return
                except Exception as e:
                    print(f"[LLMFactory] Groq API check ({model}) failed: {e}")

        # 2. Test Local Ollama connectivity
        try:
            res = requests.get(f"{self.host}/api/tags", timeout=2)
            if res.status_code == 200:
                self.active_provider = "ollama"
                tags_data = res.json()
                models = [m.get("name") for m in tags_data.get("models", []) if "embed" not in m.get("name", "")]
                if models:
                    self.model_name = models[0]
                else:
                    self.model_name = self.OLLAMA_DEFAULT_MODEL
                print(f"[LLMFactory] Configured Ollama Local ({self.model_name}).")
                return
        except Exception:
            pass

        print("[LLMFactory] Operating in Smart Offline Mode.")
        self.active_provider = "offline"

    def get_langchain_llm(self):
        """Returns a LangChain-compatible LLM instance."""
        if self.active_provider == "groq" and self.api_key:
            try:
                from langchain_community.chat_models import ChatGroq
                return ChatGroq(
                    temperature=0.7,
                    model_name=self.model_name,
                    groq_api_key=self.api_key
                )
            except Exception:
                try:
                    from langchain.chat_models import init_chat_model
                    return init_chat_model(model=f"groq:{self.model_name}", api_key=self.api_key)
                except Exception as e:
                    print(f"[LLMFactory LangChain Error] {e}")
                    
        if self.active_provider == "ollama":
            try:
                from langchain_community.chat_models.ollama import ChatOllama
                return ChatOllama(model=self.model_name, base_url=self.host)
            except Exception:
                try:
                    from langchain_ollama import ChatOllama
                    return ChatOllama(model=self.model_name, base_url=self.host)
                except Exception as e:
                    print(f"[LLMFactory LangChain Ollama Error] {e}")

        return None

    def get_crewai_llm(self):
        """Returns a CrewAI-compatible LLM instance (`crewai.LLM`)."""
        if self.active_provider == "offline":
            return None
            
        try:
            from crewai import LLM
            if self.active_provider == "groq" and self.api_key:
                target_model = self.model_name
                if target_model.startswith("openai/"):
                    model_str = f"openai/{target_model}"
                else:
                    model_str = f"openai/openai/{target_model}"
                return LLM(
                    model=model_str,
                    api_key=self.api_key,
                    base_url="https://api.groq.com/openai/v1",
                    temperature=0.7
                )
            elif self.active_provider == "ollama":
                return LLM(
                    model=f"ollama/{self.model_name}",
                    base_url=self.host,
                    temperature=0.7
                )
        except Exception as e:
            print(f"[LLMFactory CrewAI Error] {e}")
        return None

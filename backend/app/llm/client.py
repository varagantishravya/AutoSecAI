import os
import time
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class GroqClientMock:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("WARNING: GROQ_API_KEY not found in .env file. Please add it!")
            
        self.groq = OpenAI(
            api_key=self.api_key or "DUMMY_KEY",
            base_url="https://api.groq.com/openai/v1"
        )
    
    def chat(self, model, messages, max_retries: int = 4):
        groq_model = os.getenv("GROQ_MODEL", "groq/compound-mini")
        current_messages = messages

        for attempt in range(max_retries):
            try:
                response = self.groq.chat.completions.create(
                    model=groq_model,
                    messages=current_messages,
                    temperature=0.0,
                    seed=42
                )
                return {
                    "message": {
                        "content": response.choices[0].message.content
                    }
                }
            except Exception as e:
                err_str = str(e)
                # Rate limit (429) retry handling
                if "429" in err_str or "rate_limit" in err_str:
                    wait_match = re.search(r"try again in (\d+(?:\.\d+)?)s", err_str, re.IGNORECASE)
                    wait_time = float(wait_match.group(1)) + 1.5 if wait_match else (attempt + 1) * 3.0
                    print(f"Rate limit (429) hit. Waiting {wait_time:.1f}s before retry (Attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue

                # Request Too Large (413) truncation handling
                if "413" in err_str or "request_too_large" in err_str or "too large" in err_str:
                    print(f"Request Entity Too Large (413). Truncating patch input (Attempt {attempt + 1}/{max_retries})...")
                    truncated_messages = []
                    for msg in current_messages:
                        content = msg.get("content", "")
                        if len(content) > 3000:
                            content = content[:3000] + "\n... [Truncated due to context size limit] ..."
                        truncated_messages.append({"role": msg.get("role", "user"), "content": content})
                    current_messages = truncated_messages
                    time.sleep(1.0)
                    continue

                # Secondary model fallback on final attempt
                if attempt == max_retries - 1:
                    print(f"Primary model '{groq_model}' failed ({e}). Retrying with secondary model 'groq/compound'...")
                    try:
                        response = self.groq.chat.completions.create(
                            model="groq/compound",
                            messages=current_messages,
                            temperature=0.0,
                            seed=42
                        )
                        return {
                            "message": {
                                "content": response.choices[0].message.content
                            }
                        }
                    except Exception as final_err:
                        raise final_err

                time.sleep(2.0)

        raise RuntimeError("LLM request failed after maximum retry attempts.")


client = GroqClientMock()
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
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
    
    def chat(self, model, messages):
        # We ignore the local model ("llama3.2:1b") and force the fast Groq model
        groq_model = "openai/gpt-oss-20b"
        
        response = self.groq.chat.completions.create(
            model=groq_model,
            messages=messages
        )
        
        # Return a dictionary mimicking Ollama's structure
        return {
            "message": {
                "content": response.choices[0].message.content
            }
        }

client = GroqClientMock()
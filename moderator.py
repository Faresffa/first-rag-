import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class Moderator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # On utilise un modèle léger et rapide (safeguard)
        self.model = "llama-3.1-8b-instant" 
        
        with open("prompts/moderator_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def moderate(self, question):
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Analyse cette question : {question}"}
            ],
            model=self.model,
            response_format={"type": "json_object"}
        )
        # On transforme la chaîne JSON en dictionnaire Python
        return json.loads(response.choices[0].message.content)
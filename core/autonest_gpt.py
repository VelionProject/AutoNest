# autonest_gpt.py

import openai
import os

# API-Schlüssel setzen (nur wenn bereit)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Alternativ direkt einfügen

def build_prompt(code_str, project_structure_summary):
    """
    Erstellt den Prompt für GPT, um zu bewerten, wohin der Code gehören sollte.
    """
    return f"""
Du bist ein semantisch orientierter Code-Assistent.

Hier ist ein neuer Codeblock, den der Nutzer einfügen möchte:

```python
{code_str}

import os
from openai import ChatCompletion
from core.autonest_gpt import build_prompt, describe_project_with_gpt

openai_api_key = os.getenv("OPENAI_API_KEY")


def suggest_insertion(code_str, project_path):
    """
    Führt eine semantische Analyse durch und gibt GPT-Vorschlag zurück.
    """
    # Projektbeschreibung erzeugen (strukturbasiert)
    project_summary = describe_project_with_gpt(project_path)

    # Prompt generieren
    prompt = build_prompt(code_str, project_summary)

    # GPT-Aufruf
    messages = [
        {"role": "system", "content": "Du bist ein semantisch denkender Python-Assistent."},
        {"role": "user", "content": prompt}
    ]

    response = ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        api_key=openai_api_key
    )
    return response["choices"][0]["message"]["content"]


# Alias für AutoNest-Kompatibilität
suggest_logic = suggest_insertion


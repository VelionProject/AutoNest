import os

LANG = os.environ.get("AUTONEST_LANG", "de")

_TRANSLATIONS = {
    "en": {
        "Pfad fehlt": "Path missing",
        "Projektbeschreibung": "Project description",
        "Backup wiederherstellen": "Restore backup",
        "Analyse starten": "Start analysis",
        "Code einfügen + sichern": "Insert code + backup",
        "Analyse erforderlich": "Analysis required",
        "Fehlgeschlagen": "Failed",
        "Fehlende Eingaben": "Missing inputs",
    },
    "de": {},
}


def t(text: str) -> str:
    return _TRANSLATIONS.get(LANG, {}).get(text, text)

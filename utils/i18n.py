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
        "Projektverzeichnis": "Project directory",
        "Durchsuchen": "Browse",
        "GPT-Modus aktivieren": "Enable GPT mode",
        "Projekt beschreiben": "Describe project",
        "Neuen Python-Code einfügen": "Insert new Python code",
        "Noch keine Analyse durchgeführt.": "No analysis performed yet.",
        "Fehler": "Error",
        "Erfolg": "Success",
        "Backup-Session wählen:": "Select backup session:",
        "Keine Sessions gefunden.": "No sessions found.",
        "Datei innerhalb der Session:": "File within the session:",
        "Fehlende Auswahl": "Missing selection",
        "Wiederherstellen": "Restore",
        "Bitte zuerst ein Projektverzeichnis wählen.": "Please choose a project directory first.",
        "Fehler bei GPT": "GPT error",
        "Bitte zuerst auf 'Analyse starten' klicken.": "Please click 'Start analysis' first.",
        "Bitte Code und Projektpfad angeben.": "Please provide code and project path.",
        "Bitte Session und Datei wählen.": "Please choose session and file.",
        "Wiederhergestellt": "Restored",
        "Module verwalten": "Manage modules",
        "Speichern": "Save",
        "Modulstatus gespeichert.": "Module status saved.",
    },
    "de": {},
}


def t(text: str) -> str:
    return _TRANSLATIONS.get(LANG, {}).get(text, text)

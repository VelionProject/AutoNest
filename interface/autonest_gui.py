import tkinter as tk
from tkinter import filedialog, messagebox
import os
from core.code_inserter import safe_insert_code
from core.autonest_semantics import suggest
from backup.backup_manager import list_backup_sessions, restore_file_from_session
from backup.memory_context_manager import save_context_entry, load_recent_entries
from utils.logger import get_logger
from utils.i18n import t
from utils.config import load_config, save_config
from plugins import list_plugins

logger = get_logger(__name__)


class AutoNestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoNest 0.2")
        self.root.geometry("820x700")

        self.config = load_config()

        self.project_path = tk.StringVar(value=self.config.get("default_project_path", ""))
        self.use_gpt = tk.BooleanVar(value=self.config.get("use_gpt", False))
        self.suggestion = None

        self.build_gui()

    def build_gui(self):
        frame_top = tk.LabelFrame(self.root, text=t("Projektverzeichnis"), padx=10, pady=5)
        frame_top.pack(fill="x", padx=10, pady=5)

        path_entry = tk.Entry(frame_top, textvariable=self.project_path, width=70)
        path_entry.pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(frame_top, text=t("Durchsuchen"), command=self.browse_folder).pack(side=tk.LEFT)

        gpt_toggle = tk.Checkbutton(
            self.root, text=t("GPT-Modus aktivieren"), variable=self.use_gpt
        )
        gpt_toggle.pack(anchor="w", padx=15, pady=(0, 5))

        tk.Button(
            self.root,
            text=t("Backup wiederherstellen"),
            command=self.open_restore_window,
        ).pack(anchor="w", padx=15, pady=(0, 10))
        tk.Button(
            self.root,
            text=t("Module verwalten"),
            command=self.open_module_manager,
        ).pack(anchor="w", padx=15, pady=(0, 5))
        tk.Button(
            self.root,
            text=t("Projekt beschreiben"),
            command=self.analyse_project_description,
        ).pack(anchor="w", padx=15, pady=(0, 5))
        tk.Button(
            self.root,
            text=t("Zuletzt eingefügt"),
            command=self.open_recent_entries,
        ).pack(anchor="w", padx=15, pady=(0, 5))

        frame_code = tk.LabelFrame(self.root, text=t("Neuen Python-Code einfügen"), padx=10, pady=5)
        frame_code.pack(fill="both", expand=True, padx=10, pady=5)

        self.code_text = tk.Text(frame_code, height=15)
        self.code_text.pack(fill="both", expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text=t("Analyse starten"), command=self.analyse_code).pack(
            side=tk.LEFT, padx=10
        )
        tk.Button(button_frame, text=t("Code einfügen + sichern"), command=self.insert_code).pack(
            side=tk.LEFT
        )

        self.result_label = tk.Label(
            self.root,
            text=t("Noch keine Analyse durchgeführt."),
            fg="gray",
            font=("Arial", 10, "italic"),
        )
        self.result_label.pack(pady=(10, 0))

    def analyse_project_description(self):
        path = self.project_path.get().strip()
        if not path:
            messagebox.showwarning(
                t("Pfad fehlt"), t("Bitte zuerst ein Projektverzeichnis wählen.")
            )
            return

        if self.use_gpt.get():
            # GPT-Modus verwenden
            try:
                from core.autonest_gpt import describe_project_with_gpt

                description = describe_project_with_gpt(path)
            except Exception as e:
                messagebox.showerror(t("Fehler bei GPT"), f"Analyse nicht möglich:\n{str(e)}")
                return
        else:
            # Lokale Analyse
            from core.project_scanner import describe_project_locally

            description = describe_project_locally(path)

        # Ausgabe im Pop-up
        messagebox.showinfo(t("Projektbeschreibung"), description)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.project_path.set(folder)

    def analyse_code(self):
        code = self.code_text.get("1.0", tk.END).strip()
        path = self.project_path.get().strip()

        if not code or not path:
            messagebox.showerror(t("Fehlende Eingaben"), t("Bitte Code und Projektpfad angeben."))
            return

        os.environ["AUTONEST_USE_GPT"] = "1" if self.use_gpt.get() else "0"

        try:
            self.suggestion = suggest(code, path)
        except Exception as e:
            self.result_label.config(text=f"Analysefehler: {str(e)}", fg="red")
            return

        modus = self.suggestion.get("vermuteter_modus", "").lower()
        sicherheit = self.suggestion.get("sicherheit", "unbekannt").lower()
        datei = self.suggestion.get("ziel_datei", "–")
        funktion = self.suggestion.get("ziel_funktion", "–")

        symbol = "❌"
        if sicherheit == "hoch":
            color = "orange" if modus == "erweitern" else "green"
            symbol = "✓"
        elif sicherheit == "mittel":
            color = "blue"
            symbol = "⚠"
        else:
            color = "red"
            symbol = "❌"

        status_text = f"{symbol}  Modus: {modus.upper()}  |  Datei: {datei}  |  Funktion: {funktion}  |  Sicherheit: {sicherheit.upper()}"

        self.result_label.config(text=status_text, fg=color, font=("Arial", 10, "bold"))

    def insert_code(self):
        if not self.suggestion:
            messagebox.showwarning(
                t("Analyse erforderlich"), t("Bitte zuerst auf 'Analyse starten' klicken.")
            )
            return

        code = self.code_text.get("1.0", tk.END).strip()
        path = self.project_path.get().strip()
        modus = self.suggestion.get("vermuteter_modus", "neu")

        try:
            result = safe_insert_code(code, path, modus=modus)
        except Exception as e:
            messagebox.showerror(t("Fehlgeschlagen"), f"Einfügefehler: {str(e)}")
            return

        if "error" in result:
            messagebox.showerror(t("Fehler"), result["error"])
        else:
            save_context_entry(path, self.suggestion, code)
            messagebox.showinfo(
                t("Erfolg"),
                f"Code erfolgreich eingefügt!\n\nDatei: {result['datei']}\nModus: {modus}\nBackup: {result['backup_session']}",
            )

    def open_restore_window(self):
        restore_win = tk.Toplevel(self.root)
        restore_win.title("Backup wiederherstellen")
        restore_win.geometry("500x300")

        tk.Label(restore_win, text=t("Backup-Session wählen:")).pack(pady=5)
        session_var = tk.StringVar()
        sessions = list_backup_sessions()
        if not sessions:
            tk.Label(restore_win, text=t("Keine Sessions gefunden."), fg="red").pack()
            return
        session_dropdown = tk.OptionMenu(restore_win, session_var, *sessions)
        session_dropdown.pack(pady=5)

        tk.Label(restore_win, text=t("Datei innerhalb der Session:")).pack(pady=5)
        file_var = tk.StringVar()
        file_dropdown = tk.OptionMenu(restore_win, file_var, "")
        file_dropdown.pack(pady=5)

        def update_files(*args):
            session = session_var.get()
            path = os.path.join(".autonest_backups", session)
            try:
                files = os.listdir(path)
            except FileNotFoundError:
                files = []
            menu = file_dropdown["menu"]
            menu.delete(0, "end")
            for f in files:
                menu.add_command(label=f, command=lambda value=f: file_var.set(value))

        session_var.trace("w", update_files)

        def restore_action():
            session = session_var.get()
            file = file_var.get()
            if not session or not file:
                messagebox.showwarning(t("Fehlende Auswahl"), t("Bitte Session und Datei wählen."))
                return
            result = restore_file_from_session(session, file)
            messagebox.showinfo(t("Wiederhergestellt"), result)

        tk.Button(restore_win, text=t("Wiederherstellen"), command=restore_action).pack(pady=15)

    def open_recent_entries(self):
        path = self.project_path.get().strip()
        if not path:
            messagebox.showwarning(t("Pfad fehlt"), t("Bitte zuerst ein Projektverzeichnis wählen."))
            return

        entries = load_recent_entries(path)
        win = tk.Toplevel(self.root)
        win.title(t("Zuletzt eingefügt"))
        win.geometry("600x300")

        if not entries:
            tk.Label(win, text=t("Keine Einträge gefunden."), fg="red").pack(pady=10)
            return

        txt = tk.Text(win, wrap="word")
        txt.pack(fill="both", expand=True)
        for entry in entries:
            header = f"{entry['timestamp']} - {entry['file_target']}::{entry['function_target']} [{entry['mode']}]"
            txt.insert("end", header + "\n")
            txt.insert("end", entry["raw_code"] + "\n\n")
        txt.config(state="disabled")

    def open_module_manager(self):
        win = tk.Toplevel(self.root)
        win.title(t("Module verwalten"))
        win.geometry("300x300")

        vars_ = {}
        modules = self.config.get("modules", {})
        for name in list_plugins():
            var = tk.BooleanVar(value=modules.get(name, True))
            vars_[name] = var
            tk.Checkbutton(win, text=name, variable=var).pack(anchor="w")

        def save():
            for name, var in vars_.items():
                modules[name] = var.get()
            self.config["modules"] = modules
            save_config(self.config)
            messagebox.showinfo(t("Erfolg"), t("Modulstatus gespeichert."))
            win.destroy()

        tk.Button(win, text=t("Speichern"), command=save).pack(pady=10)


def main():
    root = tk.Tk()
    app = AutoNestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

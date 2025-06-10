import tkinter as tk
from tkinter import filedialog, messagebox
import os
import logging

from core.code_inserter import safe_insert_code
from core.autonest_semantics import suggest
from backup.backup_manager import list_backup_sessions, restore_file_from_session
from backup.memory_context_manager import save_context_entry, load_recent_entries
from utils.logger import get_logger
from utils.i18n import t
from utils.config import load_config, save_config
from plugins import list_plugins

logger = get_logger(__name__)


class TextHandler(logging.Handler):
    """Logging handler that writes log messages into a Tkinter Text widget."""

    def __init__(self, text_widget: tk.Text):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", msg + "\n")
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")


class AutoNestGUI:
    """Main application window for interacting with AutoNest."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AutoNest v0.1 – Python Coding Assistant")
        self.root.geometry("900x700")

        self.config = load_config()

        self.project_path = tk.StringVar(value=self.config.get("default_project_path", ""))
        self.model_var = tk.StringVar(value=self.config.get("model", "GPT-4o"))

        self.suggestion = None

        self.build_gui()

    def build_gui(self) -> None:
        """Construct all UI components."""

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        # Sidebar with navigation buttons
        sidebar = tk.Frame(container, width=150, bg="#f5f5f5")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main_area = tk.Frame(container)
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frames = {}
        self.frames["modules"] = self._build_module_frame()
        self.frames["project"] = self._build_project_frame()
        self.frames["code"] = self._build_code_frame()
        self.frames["logs"] = self._build_logs_frame()

        for name, frame in self.frames.items():
            frame.pack_forget()

        tk.Button(
            sidebar, text=t("Module Status"), command=lambda: self.show_frame("modules")
        ).pack(fill="x")
        tk.Button(
            sidebar, text=t("Manage Projects"), command=lambda: self.show_frame("project")
        ).pack(fill="x")
        tk.Button(sidebar, text=t("Insert Code"), command=lambda: self.show_frame("code")).pack(
            fill="x"
        )
        tk.Button(sidebar, text=t("Logs"), command=lambda: self.show_frame("logs")).pack(fill="x")

        self.footer_var = tk.StringVar()
        footer = tk.Label(self.root, textvariable=self.footer_var, anchor="w")
        footer.pack(fill="x", side=tk.BOTTOM)
        self.project_path.trace("w", lambda *_: self._update_footer())
        self._update_footer()

        self.show_frame("code")

        # attach logger after log frame exists
        handler = TextHandler(self.log_text)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logging.getLogger().addHandler(handler)

    def analyse_project_description(self):
        path = self.project_path.get().strip()
        if not path:
            messagebox.showwarning(
                t("Pfad fehlt"), t("Bitte zuerst ein Projektverzeichnis wählen.")
            )
            return

        if self.model_var.get() == "GPT-4o":
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

    def analyse_code(self) -> None:
        code = self.code_text.get("1.0", tk.END).strip()
        path = self.project_path.get().strip()

        if not code or not path:
            messagebox.showerror(t("Fehlende Eingaben"), t("Bitte Code und Projektpfad angeben."))
            return

        os.environ["AUTONEST_MODEL"] = self.model_var.get()

        try:
            self.suggestion = suggest(code, path)
        except Exception as e:
            self.results_panel.configure(state="normal")
            self.results_panel.delete("1.0", tk.END)
            self.results_panel.insert("end", f"Analysefehler: {str(e)}")
            self.results_panel.configure(state="disabled")
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

        status_text = (
            f"{symbol}  Modus: {modus.upper()}  |  Datei: {datei}  |  Funktion: {funktion}  |  "
            f"Sicherheit: {sicherheit.upper()}"
        )

        self.results_panel.configure(state="normal")
        self.results_panel.delete("1.0", tk.END)
        self.results_panel.insert("end", status_text)
        self.results_panel.configure(state="disabled")

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
                (
                    "Code erfolgreich eingefügt!\n\n"
                    f"Datei: {result['datei']}\nModus: {modus}\n"
                    f"Backup: {result['backup_session']}"
                ),
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
            messagebox.showwarning(
                t("Pfad fehlt"), t("Bitte zuerst ein Projektverzeichnis wählen.")
            )
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
            header = (
                f"{entry['timestamp']} - {entry['file_target']}::"
                f"{entry['function_target']} [{entry['mode']}]"
            )
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

    # --- UI construction helpers ---
    def _build_project_frame(self) -> tk.Frame:
        frame = tk.Frame(self.main_area)

        top = tk.LabelFrame(frame, text=t("Projektverzeichnis"), padx=10, pady=5)
        top.pack(fill="x", padx=10, pady=5)

        tk.Entry(top, textvariable=self.project_path, width=70).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(top, text=t("Durchsuchen"), command=self.browse_folder).pack(side=tk.LEFT)

        settings = tk.LabelFrame(frame, text=t("Einstellungen"), padx=10, pady=5)
        settings.pack(fill="x", padx=10, pady=5)

        tk.Label(settings, text=t("AI Modell:"), anchor="w").pack(side=tk.LEFT)
        tk.OptionMenu(settings, self.model_var, "GPT-4o", "Codex").pack(side=tk.LEFT)
        tk.Button(settings, text=t("Aktualisieren"), command=self.save_settings).pack(
            side=tk.LEFT, padx=5
        )

        tk.Button(
            frame, text=t("Projekt beschreiben"), command=self.analyse_project_description
        ).pack(anchor="w", padx=15, pady=(10, 5))
        tk.Button(frame, text=t("Zuletzt eingefügt"), command=self.open_recent_entries).pack(
            anchor="w", padx=15, pady=(0, 5)
        )
        tk.Button(frame, text=t("Backup wiederherstellen"), command=self.open_restore_window).pack(
            anchor="w", padx=15, pady=(0, 5)
        )

        return frame

    def _build_module_frame(self) -> tk.Frame:
        frame = tk.Frame(self.main_area)

        vars_ = {}
        modules = self.config.get("modules", {})
        for name in list_plugins():
            var = tk.BooleanVar(value=modules.get(name, True))
            vars_[name] = var
            tk.Checkbutton(frame, text=name, variable=var).pack(anchor="w")

        tk.Button(frame, text=t("Speichern"), command=lambda: self._save_modules(vars_)).pack(
            pady=10
        )

        return frame

    def _save_modules(self, vars_: dict) -> None:
        modules = self.config.get("modules", {})
        for name, var in vars_.items():
            modules[name] = var.get()
        self.config["modules"] = modules
        save_config(self.config)
        messagebox.showinfo(t("Erfolg"), t("Modulstatus gespeichert."))

    def _build_code_frame(self) -> tk.Frame:
        frame = tk.Frame(self.main_area)

        code_area = tk.LabelFrame(frame, text=t("Neuen Python-Code einfügen"), padx=10, pady=5)
        code_area.pack(fill="both", expand=True, padx=10, pady=5)

        self.code_text = tk.Text(code_area, height=15)
        self.code_text.pack(fill="both", expand=True)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text=t("Execute Code"), command=self.analyse_code).pack(
            side=tk.LEFT, padx=10
        )
        tk.Button(button_frame, text=t("Insert"), command=self.insert_code).pack(side=tk.LEFT)
        tk.Button(
            button_frame, text=t("View Results"), command=lambda: self.show_frame("logs")
        ).pack(side=tk.LEFT, padx=10)

        self.results_panel = tk.Text(frame, height=4, state="disabled")
        self.results_panel.pack(fill="x", padx=10, pady=(5, 0))

        return frame

    def _build_logs_frame(self) -> tk.Frame:
        frame = tk.Frame(self.main_area)
        self.log_text = tk.Text(frame, state="disabled")
        self.log_text.pack(fill="both", expand=True)
        return frame

    def show_frame(self, name: str) -> None:
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def _update_footer(self) -> None:
        self.footer_var.set(f"Projekt: {self.project_path.get()} | AutoNest v0.1")

    def save_settings(self) -> None:
        self.config["default_project_path"] = self.project_path.get()
        self.config["model"] = self.model_var.get()
        save_config(self.config)
        self._update_footer()


def main():
    root = tk.Tk()
    app = AutoNestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

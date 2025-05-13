import tkinter as tk
from tkinter import filedialog, messagebox
import os
from code_inserter import safe_insert_code
from autonest_semantics import suggest
from backup_gui import open_restore_window
from project_registry import register_project, get_last_project, load_registry

class AutoNestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoNest 0.2 – Intelligenter Code-Inserter")
        self.root.geometry("880x740")

        self.project_path = tk.StringVar()
        self.use_gpt = tk.BooleanVar()
        self.suggestion = None

        last_project = get_last_project()
        if last_project:
            self.project_path.set(last_project)

        self.build_gui()

    def build_gui(self):
        frame_top = tk.LabelFrame(self.root, text="Projektverzeichnis", padx=10, pady=5)
        frame_top.pack(fill="x", padx=10, pady=5)

        path_entry = tk.Entry(frame_top, textvariable=self.project_path, width=70)
        path_entry.pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(frame_top, text="Durchsuchen", command=self.browse_folder).pack(side=tk.LEFT)

        gpt_toggle = tk.Checkbutton(self.root, text="GPT-Modus aktivieren", variable=self.use_gpt)
        gpt_toggle.pack(anchor="w", padx=15, pady=(0, 5))

        tk.Button(self.root, text="Backup wiederherstellen", command=lambda: open_restore_window(self.root)).pack(anchor="w", padx=15, pady=(0, 10))
        tk.Button(self.root, text="Projekt beschreiben", command=self.analyse_project_description).pack(anchor="w", padx=15, pady=(0, 5))

        self.build_recent_projects_section()

        frame_code = tk.LabelFrame(self.root, text="Neuen Python-Code einfügen", padx=10, pady=5)
        frame_code.pack(fill="both", expand=True, padx=10, pady=5)

        self.code_text = tk.Text(frame_code, height=15)
        self.code_text.pack(fill="both", expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Analyse starten", command=self.analyse_code).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Code einfügen + sichern", command=self.insert_code).pack(side=tk.LEFT)

        self.result_label = tk.Label(self.root, text="Noch keine Analyse durchgeführt.", fg="gray", font=("Arial", 10, "italic"))
        self.result_label.pack(pady=(10, 0))

    def build_recent_projects_section(self):
        frame = tk.LabelFrame(self.root, text="Letzte Projekte", padx=10, pady=5)
        frame.pack(fill="both", padx=10, pady=5, expand=False)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.project_listbox = tk.Listbox(frame, height=5, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
        self.project_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.project_listbox.yview)

        # Lade Projekte
        history = load_registry().get("history", [])
        for path in history:
            name = os.path.basename(path.rstrip("/\\"))
            display = f"{name}  [{path}]"
            self.project_listbox.insert(tk.END, display)

        # Tooltip bei Hover (könnte später ergänzt werden)
        def on_double_click(event):
            selection = self.project_listbox.curselection()
            if selection:
                text = self.project_listbox.get(selection[0])
                path = text.split("[")[-1].rstrip("]")
                self.project_path.set(path)
                register_project(path)

        self.project_listbox.bind("<Double-Button-1>", on_double_click)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.project_path.set(folder)
            register_project(folder)

    def analyse_code(self):
        code = self.code_text.get("1.0", tk.END).strip()
        path = self.project_path.get().strip()

        if not code or not path:
            messagebox.showerror("Fehlende Eingaben", "Bitte Code und Projektpfad angeben.")
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

        status_text = (
            f"{symbol}  Modus: {modus.upper()}  |  Datei: {datei}  |  Funktion: {funktion}  |  Sicherheit: {sicherheit.upper()}"
        )

        self.result_label.config(text=status_text, fg=color, font=("Arial", 10, "bold"))

    def insert_code(self):
        if not self.suggestion:
            messagebox.showwarning("Analyse erforderlich", "Bitte zuerst auf 'Analyse starten' klicken.")
            return

        code = self.code_text.get("1.0", tk.END).strip()
        path = self.project_path.get().strip()
        modus = self.suggestion.get("vermuteter_modus", "neu")

        try:
            result = safe_insert_code(code, path, modus=modus)
        except Exception as e:
            messagebox.showerror("Fehlgeschlagen", f"Einfügefehler: {str(e)}")
            return

        if "error" in result:
            messagebox.showerror("Fehler", result["error"])
        else:
            messagebox.showinfo(
                "Erfolg",
                f"Code erfolgreich eingefügt!\n\nDatei: {result['datei']}\nModus: {modus}\nBackup: {result['backup_session']}"
            )

    def analyse_project_description(self):
        path = self.project_path.get().strip()
        if not path:
            messagebox.showwarning("Pfad fehlt", "Bitte zuerst ein Projektverzeichnis wählen.")
            return

        if self.use_gpt.get():
            try:
                from autonest_gpt import describe_project_with_gpt
                description = describe_project_with_gpt(path)
            except Exception as e:
                messagebox.showerror("Fehler bei GPT", f"Analyse nicht möglich:\n{str(e)}")
                return
        else:
            from project_scanner import describe_project_locally
            description = describe_project_locally(path)

        messagebox.showinfo("Projektbeschreibung", description)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoNestGUI(root)
    root.mainloop()

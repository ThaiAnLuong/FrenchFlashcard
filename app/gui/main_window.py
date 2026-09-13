import tkinter as tk
from tkinter import filedialog, messagebox

from app.gui.vocabulary_list import VocabularyList
from app.gui.vocabulary_input import VocabularyInput
from app.services.backup_manager import BackupManager


class MainWindow:
    def __init__(self, root, manager, settings):
        self.root = root
        self.manager = manager
        self.settings = settings
        self.backup_manager = BackupManager()

        self.root.title("French Flashcard")
        self.root.geometry("1000x700+500+100")
        self.root.minsize(800, 600)
        self.root.configure(bg="#767676")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="French Flashcard",
            font=("Arial", 24)
        )

        title.pack(
            pady=50
        )

        list_button = tk.Button(
            self.root,
            text="List Vocabulary",
            width=25,
            command=self.open_vocabulary_list
        )

        list_button.pack(
            pady=10
        )

        input_button = tk.Button(
            self.root,
            text="Input One Word",
            width=25,
            command=self.open_vocabulary_input
        )

        input_button.pack(
            pady=10
        )

        csv_button = tk.Button(
            self.root,
            text="Input CSV File",
            width=25,
            command=self.import_csv
        )

        csv_button.pack(
            pady=10
        )

        export_button = tk.Button(
            self.root,
            text="Export Backup (.zip)",
            width=25,
            command=self.export_backup
        )

        export_button.pack(
            pady=10
        )

        import_button = tk.Button(
            self.root,
            text="Import Backup (.zip)",
            width=25,
            command=self.import_backup
        )

        import_button.pack(
            pady=10
        )

    def open_vocabulary_list(self):
        VocabularyList(
            self.root,
            self.manager,
            self.settings
        )

    def open_vocabulary_input(self):
        VocabularyInput(
            self.root,
            self.manager
        )

    def import_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            count = self.manager.import_csv(
                file_path
            )

            messagebox.showinfo(
                "Import Complete",
                f"{count} vocabulary item(s) imported successfully."
            )

        except Exception as error:
            messagebox.showerror(
                "Import Error",
                str(error)
            )

    def export_backup(self):
        file_path = filedialog.asksaveasfilename(
            title="Export FrenchFlashcard Backup",
            defaultextension=".zip",
            filetypes=[
                ("FrenchFlashcard Backup", "*.zip"),
                ("ZIP Files", "*.zip")
            ]
        )

        if not file_path:
            return

        try:
            self.manager.save()
            self.backup_manager.export_backup(file_path)

            messagebox.showinfo(
                "Export Complete",
                "FrenchFlashcard backup exported successfully."
            )
        except Exception as error:
            messagebox.showerror(
                "Export Error",
                str(error)
            )

    def import_backup(self):
        file_path = filedialog.askopenfilename(
            title="Select FrenchFlashcard Backup",
            filetypes=[
                ("FrenchFlashcard Backup", "*.zip"),
                ("ZIP Files", "*.zip")
            ]
        )

        if not file_path:
            return

        try:
            backup_file = self.backup_manager.create_pre_import_backup()

            result = self.backup_manager.import_backup(
                file_path,
                self.manager,
                self.settings
            )

            messagebox.showinfo(
                "Import Complete",
                (
                    "Backup merged successfully.\n\n"
                    f"Added: {result['added']}\n"
                    f"Updated: {result['updated']}\n"
                    f"Deleted: {result['deleted']}\n"
                    f"Skipped: {result['skipped']}\n\n"
                    f"Safety backup: {backup_file}"
                )
            )
        except Exception as error:
            messagebox.showerror(
                "Import Error",
                str(error)
            )

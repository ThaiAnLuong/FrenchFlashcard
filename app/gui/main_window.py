import tkinter as tk
from tkinter import filedialog, messagebox

from app.gui.vocabulary_list import VocabularyList
from app.gui.vocabulary_input import VocabularyInput


class MainWindow:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        self.root.title("French Flashcard")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#767676")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="French Flashcard",
            font=("Arial", 24)
        )
        title.pack(pady=50)

        list_button = tk.Button(
            self.root,
            text="List Vocabulary",
            width=25,
            command=self.open_vocabulary_list
        )
        list_button.pack(pady=10)

        input_button = tk.Button(
            self.root,
            text="Input One Word",
            width=25,
            command=self.open_vocabulary_input
        )
        input_button.pack(pady=10)

        csv_button = tk.Button(
            self.root,
            text="Input CSV File",
            width=25,
            command=self.import_csv
        )
        csv_button.pack(pady=10)

    def open_vocabulary_list(self):
        VocabularyList(
            self.root,
            self.manager
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
            count = self.manager.import_csv(file_path)

            messagebox.showinfo(
                "Import Complete",
                f"{count} vocabulary item(s) imported successfully."
            )

        except Exception as error:
            messagebox.showerror(
                "Import Error",
                str(error)
            )
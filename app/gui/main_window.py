import tkinter as tk

from app.gui.vocabulary_list import VocabularyList


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
            width=25
        )

        input_button.pack(pady=10)

        csv_button = tk.Button(
            self.root,
            text="Input CSV File",
            width=25
        )

        csv_button.pack(pady=10)

    def open_vocabulary_list(self):
        VocabularyList(
            self.root,
            self.manager
        )
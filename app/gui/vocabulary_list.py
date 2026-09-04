import tkinter as tk
from tkinter import messagebox, ttk

from app.gui.vocabulary_input import VocabularyInput


class VocabularyList:
    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager

        self.current_sort = "newest"
        self.current_vocabulary_list = []

        self.window = tk.Toplevel(parent)
        self.window.title("Vocabulary List")
        self.window.geometry("900x600")

        self.create_widgets()
        self.show_newest()

    def create_widgets(self):
        title = tk.Label(
            self.window,
            text="Vocabulary",
            font=("Arial", 24)
        )
        title.pack(pady=20)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        newest_button = tk.Button(
            button_frame,
            text="Newest",
            width=15,
            command=self.show_newest
        )
        newest_button.pack(side=tk.LEFT, padx=5)

        az_button = tk.Button(
            button_frame,
            text="A-Z",
            width=15,
            command=self.show_a_z
        )
        az_button.pack(side=tk.LEFT, padx=5)

        edit_button = tk.Button(
            button_frame,
            text="Edit",
            width=15,
            command=self.edit_selected
        )
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(
            button_frame,
            text="Delete",
            width=15,
            command=self.delete_selected
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        table_frame = tk.Frame(self.window)
        table_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=30,
            pady=20
        )

        columns = [
            "word",
            "meaning",
            "gender",
            "pronunciation",
            "type"
        ]

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "word",
            text="Word"
        )

        self.tree.heading(
            "meaning",
            text="Meaning"
        )

        self.tree.heading(
            "gender",
            text="Gender"
        )

        self.tree.heading(
            "pronunciation",
            text="Pronunciation"
        )

        self.tree.heading(
            "type",
            text="Type"
        )

        self.tree.column(
            "word",
            width=150
        )

        self.tree.column(
            "meaning",
            width=180
        )

        self.tree.column(
            "gender",
            width=80
        )

        self.tree.column(
            "pronunciation",
            width=180
        )

        self.tree.column(
            "type",
            width=120
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

    def show_newest(self):
        self.current_sort = "newest"

        vocabulary_list = self.manager.sort_newest()
        self.update_list(vocabulary_list)

    def show_a_z(self):
        self.current_sort = "a_z"

        vocabulary_list = self.manager.sort_a_z()
        self.update_list(vocabulary_list)

    def update_list(self, vocabulary_list):
        self.current_vocabulary_list = vocabulary_list

        for item in self.tree.get_children():
            self.tree.delete(item)

        for vocabulary in vocabulary_list:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    vocabulary.word,
                    vocabulary.get("meaning"),
                    vocabulary.get("gender"),
                    vocabulary.get("pronunciation"),
                    vocabulary.get("type")
                )
            )

    def get_selected_vocabulary(self):
        selection = self.tree.selection()

        if not selection:
            return None

        item_id = selection[0]

        index = self.tree.index(item_id)

        return self.current_vocabulary_list[index]

    def edit_selected(self):
        vocabulary = self.get_selected_vocabulary()

        if vocabulary is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a vocabulary first."
            )
            return

        VocabularyInput(
            self.window,
            self.manager,
            vocabulary
        )

        self.window.wait_window()

        if self.current_sort == "a_z":
            self.show_a_z()
        else:
            self.show_newest()

    def delete_selected(self):
        vocabulary = self.get_selected_vocabulary()

        if vocabulary is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a vocabulary first."
            )
            return

        confirmed = messagebox.askyesno(
            "Delete Vocabulary",
            f"Delete '{vocabulary.word}'?"
        )

        if confirmed:
            self.manager.delete(vocabulary)
            self.manager.save()

            if self.current_sort == "a_z":
                self.show_a_z()
            else:
                self.show_newest()

            self.window.lift()
            self.window.focus_force()
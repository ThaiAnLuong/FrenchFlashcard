import tkinter as tk
from tkinter import messagebox


class VocabularyList:
    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager

        self.current_sort = "newest"
        self.current_vocabulary_list = []

        self.window = tk.Toplevel(parent)
        self.window.title("Vocabulary List")
        self.window.geometry("800x600")

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

        self.listbox = tk.Listbox(
            self.window,
            font=("Arial", 16)
        )
        self.listbox.pack(
            fill=tk.BOTH,
            expand=True,
            padx=40,
            pady=20
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

        self.listbox.delete(0, tk.END)

        for vocabulary in vocabulary_list:
            self.listbox.insert(
                tk.END,
                vocabulary.word
            )

    def get_selected_vocabulary(self):
        selection = self.listbox.curselection()

        if not selection:
            return None

        index = selection[0]

        return self.current_vocabulary_list[index]

    def edit_selected(self):
        vocabulary = self.get_selected_vocabulary()

        if vocabulary is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a vocabulary first."
            )
            return

        print("Edit:", vocabulary.word)

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
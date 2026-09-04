import tkinter as tk
from tkinter import messagebox

from app.models.vocabulary import Vocabulary


class VocabularyInput:
    def __init__(self, parent, manager, vocabulary=None):
        self.parent = parent
        self.manager = manager
        self.vocabulary = vocabulary

        self.entries = {}

        self.window = tk.Toplevel(parent)

        if vocabulary is None:
            self.window.title("Input Vocabulary")
        else:
            self.window.title("Edit Vocabulary")

        self.window.geometry("700x600")

        self.create_widgets()

    def create_widgets(self):
        title_text = (
            "Input Vocabulary"
            if self.vocabulary is None
            else "Edit Vocabulary"
        )

        title = tk.Label(
            self.window,
            text=title_text,
            font=("Arial", 24)
        )
        title.pack(pady=20)

        form_frame = tk.Frame(self.window)
        form_frame.pack(
            padx=40,
            pady=10,
            fill=tk.X
        )

        # Word field
        self.create_field(
            form_frame,
            "word",
            0
        )

        # Other fields
        for index, field_name in enumerate(
            self.manager.field_names,
            start=1
        ):
            self.create_field(
                form_frame,
                field_name,
                index
            )

        save_button = tk.Button(
            self.window,
            text="Save",
            width=20,
            command=self.save
        )
        save_button.pack(pady=20)

        cancel_button = tk.Button(
            self.window,
            text="Cancel",
            width=20,
            command=self.window.destroy
        )
        cancel_button.pack()

        if self.vocabulary is not None:
            self.load_vocabulary()

    def create_field(self, parent, field_name, row):
        label = tk.Label(
            parent,
            text=f"{field_name}:"
        )

        label.grid(
            row=row,
            column=0,
            sticky="w",
            pady=5
        )

        entry = tk.Entry(
            parent,
            font=("Arial", 14)
        )

        entry.grid(
            row=row,
            column=1,
            sticky="ew",
            pady=5
        )

        parent.columnconfigure(
            1,
            weight=1
        )

        self.entries[field_name] = entry

    def load_vocabulary(self):
        self.entries["word"].insert(
            0,
            self.vocabulary.word
        )

        for field_name in self.manager.field_names:
            value = self.vocabulary.get(field_name)

            if value != "#":
                self.entries[field_name].insert(
                    0,
                    value
                )

    def save(self):
        word = self.entries["word"].get().strip()

        if word == "":
            messagebox.showwarning(
                "Invalid Vocabulary",
                "Word cannot be empty."
            )
            return

        data = {}

        for field_name in self.manager.field_names:
            value = self.entries[field_name].get().strip()

            if value == "":
                value = "#"

            data[field_name] = value

        # New vocabulary
        if self.vocabulary is None:
            vocabulary = Vocabulary(
                word=word,
                data=data
            )

            self.manager.add(vocabulary)

            messagebox.showinfo(
                "Saved",
                "Vocabulary added successfully."
            )

        # Edit existing vocabulary
        else:
            self.manager.edit(
                self.vocabulary,
                word=word,
                data=data
            )

            messagebox.showinfo(
                "Saved",
                "Vocabulary updated successfully."
            )

        self.manager.save()

        self.window.destroy()
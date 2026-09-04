import tkinter as tk
from tkinter import messagebox

from app.models.vocabulary import Vocabulary


class VocabularyInput:
    def __init__(
        self,
        parent,
        manager,
        vocabulary=None,
        on_close=None
    ):
        self.parent = parent
        self.manager = manager
        self.vocabulary = vocabulary
        self.on_close = on_close

        self.entries = {}

        self.window = tk.Toplevel(parent)

        if vocabulary is None:
            self.window.title("Input Vocabulary")
        else:
            self.window.title("Edit Vocabulary")

        self.window.geometry("800x750")
        self.window.minsize(700, 600)

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

        title.pack(
            pady=20
        )

        # =========================
        # Scrollable form
        # =========================

        container = tk.Frame(
            self.window
        )

        container.pack(
            fill=tk.BOTH,
            expand=True,
            padx=30,
            pady=10
        )

        canvas = tk.Canvas(
            container
        )

        scrollbar = tk.Scrollbar(
            container,
            orient=tk.VERTICAL,
            command=canvas.yview
        )

        form_frame = tk.Frame(
            canvas
        )

        form_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=form_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        # =========================
        # Word
        # =========================

        self.create_field(
            form_frame,
            "Word",
            0
        )

        # =========================
        # Dynamic fields
        # =========================

        for index, field_name in enumerate(
            self.manager.field_names,
            start=1
        ):
            self.create_field(
                form_frame,
                field_name,
                index
            )

        # =========================
        # Buttons
        # =========================

        button_frame = tk.Frame(
            self.window
        )

        button_frame.pack(
            pady=15
        )

        save_button = tk.Button(
            button_frame,
            text="Save",
            width=20,
            command=self.save
        )

        save_button.pack(
            side=tk.LEFT,
            padx=5
        )

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            width=20,
            command=self.cancel
            
        )

        cancel_button.pack(
            side=tk.LEFT,
            padx=5
        )

        # =========================
        # Load existing vocabulary
        # =========================

        if self.vocabulary is not None:
            self.load_vocabulary()

    def create_field(self, parent, field_name, row):
        label = tk.Label(
            parent,
            text=f"{field_name}:",
            font=("Arial", 11),
            anchor="w"
        )

        label.grid(
            row=row,
            column=0,
            sticky="w",
            padx=10,
            pady=6
        )

        entry = tk.Entry(
            parent,
            font=("Arial", 13)
        )

        entry.grid(
            row=row,
            column=1,
            sticky="ew",
            padx=10,
            pady=6
        )

        parent.columnconfigure(
            1,
            weight=1
        )

        self.entries[field_name] = entry

    def load_vocabulary(self):
        # Word
        self.entries["Word"].insert(
            0,
            self.vocabulary.word
        )

        # Other fields
        for field_name in self.manager.field_names:
            value = self.vocabulary.get(field_name)

            self.entries[field_name].insert(
                0,
                value
            )
            
            
    def cancel(self):
        self.window.destroy()

        if self.on_close is not None:
            self.on_close()
            
            
    def save(self):
        # =========================
        # Get Word
        # =========================

        word = self.entries["Word"].get().strip()

        if word == "":
            messagebox.showwarning(
                "Invalid Vocabulary",
                "Word cannot be empty."
            )
            return

        # =========================
        # Get vocabulary data
        # =========================

        data = {}

        for field_name in self.manager.field_names:
            value = self.entries[field_name].get().strip()

            # Blank → "-"
            if value == "":
                value = "-"

            data[field_name] = value

        # =========================
        # New vocabulary
        # =========================

        if self.vocabulary is None:
            vocabulary = Vocabulary(
                word=word,
                data=data
            )

            self.manager.add(
                vocabulary
            )

            messagebox.showinfo(
                "Saved",
                "Vocabulary added successfully."
            )

        # =========================
        # Edit vocabulary
        # =========================

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

        # =========================
        # Save database
        # =========================

        self.manager.save()

        self.window.destroy()
        
        if self.on_close is not None:
            self.on_close()
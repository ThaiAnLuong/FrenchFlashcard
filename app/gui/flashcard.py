import tkinter as tk
from tkinter import messagebox

from app.services.study_session import StudySession
from app.services.image_manager import ImageManager


class Flashcard:
    def __init__(
        self,
        parent,
        manager,
        vocabulary_list,
        start_vocabulary=None,
        settings=None,
        on_practice_changed=None,
        study_mode="all",
        
    
    ):
        self.parent = parent
        self.manager = manager
        self.settings = settings
        self.on_practice_changed = on_practice_changed
        self.study_mode = study_mode
        
        self.image_manager = ImageManager()
        self.current_image = None
        

        # Keep the complete list
        self.all_vocabulary_list = vocabulary_list



        # Create initial study list
        study_list = self.get_study_list()

        self.session = StudySession(
            study_list,
            start_vocabulary
        )

        self.is_flipped = False

        self.window = tk.Toplevel(parent)
        self.window.title("Flashcard")
        self.window.geometry("1200x880+350+100")
        self.window.minsize(900,700)

        self.create_widgets()
        self.show_front()

    def get_study_list(self):
        if self.study_mode == "all":
            return self.all_vocabulary_list

        if self.settings is None:
            return []

        practice_ids = self.settings.get_practice_ids()

        return [
            vocabulary
            for vocabulary in self.all_vocabulary_list
            if vocabulary.id in practice_ids
        ]

    def create_widgets(self):
        # =========================
        # Title
        # =========================


        self.progress_label = tk.Label(
        self.window,
        text="0 / 0",
        font=("Arial", 12, "bold")
        )

        self.progress_label.pack(pady=5)

        # =========================
        # Study mode
        # =========================

        mode_frame = tk.Frame(
            self.window
        )

        mode_frame.pack(
            pady=5
        )

        mode_label = tk.Label(
            mode_frame,
            text="Study:",
            font=("Arial", 12)
        )

        mode_label.pack(
            side=tk.LEFT,
            padx=5
        )

        self.all_button = tk.Button(
            mode_frame,
            text="All",
            width=12,
            command=self.study_all
        )

        self.all_button.pack(
            side=tk.LEFT,
            padx=3
        )

        self.practice_button = tk.Button(
            mode_frame,
            text="Practice",
            width=12,
            command=self.study_practice
        )

        self.practice_button.pack(
            side=tk.LEFT,
            padx=3
        )

        # =========================
        # Card
        # =========================

        self.card_frame = tk.Frame(
            self.window,
            bd=2,
            relief=tk.RIDGE
        )

        self.card_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=40,
            pady=20
        )

        self.content_frame = tk.Frame(
            self.card_frame
        )

        self.content_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=20
        )

        # =========================
        # Navigation
        # =========================

        navigation_frame = tk.Frame(
            self.window
        )

        navigation_frame.pack(
            pady=5
        )

        previous_button = tk.Button(
            navigation_frame,
            text="Previous",
            width=12,
            command=self.previous
        )

        previous_button.pack(
            side=tk.LEFT,
            padx=3
        )

        random_button = tk.Button(
            navigation_frame,
            text="Random",
            width=12,
            command=self.random
        )

        random_button.pack(
            side=tk.LEFT,
            padx=3
        )

        next_button = tk.Button(
            navigation_frame,
            text="Next",
            width=12,
            command=self.next
        )

        next_button.pack(
            side=tk.LEFT,
            padx=3
        )

        
        
        
        # =========================
        # Flip / Close / add practice
        # =========================

        button_frame = tk.Frame(
            self.window
        )
        button_frame.pack(
            pady=5
        )

        self.practice_toggle_button = tk.Button(
            button_frame,
            width=25,
            command=self.toggle_practice
        )
        self.practice_toggle_button.pack(
            padx=5
        )

        self.flip_button = tk.Button(
            button_frame,
            text="Flip",
            width=20,
            command=self.flip
        )

        self.flip_button.pack(
            side=tk.LEFT,
            padx=5
        )


    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_practice_button(self):
        vocabulary = self.session.current()

        if vocabulary is None:
            return

        if self.settings is None:
            self.practice_toggle_button.config(
                text="Practice unavailable",
                state=tk.DISABLED
            )
            return

        if self.settings.is_in_practice(
            vocabulary.id
        ):
            self.practice_toggle_button.config(
                text="Remove from Practice"
            )
        else:
            self.practice_toggle_button.config(
                text="Add to Practice"
            )

    def toggle_practice(self):
        vocabulary = self.session.current()

        if vocabulary is None:
            return

        if self.settings is None:
            return

        vocabulary_id = vocabulary.id

        if self.settings.is_in_practice(
            vocabulary_id
        ):
            # Remove from Practice
            self.settings.remove_practice(
                vocabulary_id
            )

            if self.study_mode == "practice":

                study_list = self.get_practice_list()

                if not study_list:
                    

                    if self.on_practice_changed is not None:
                        self.on_practice_changed()
                        
                    self.window.destroy()

                    return

                else:
                    # Keep the same position if possible.
                    old_index = self.session.current_index

                    if old_index >= len(study_list):
                        old_index = len(study_list) - 1

                    next_vocabulary = study_list[
                        old_index
                    ]

                    self.session = StudySession(
                        study_list,
                        next_vocabulary
                    )

                    self.show_front()

            else:
                self.update_practice_button()

            # Refresh Vocabulary List.
            if self.on_practice_changed is not None:
                self.on_practice_changed()

            return

        # Add to Practice
        self.settings.add_practice(
            vocabulary_id
        )

        self.update_practice_button()

        # Refresh Vocabulary List.
        if self.on_practice_changed is not None:
            self.on_practice_changed()

    def study_all(self):
        study_list = self.all_vocabulary_list

        if not study_list:
            messagebox.showinfo(
                "No Vocabulary",
                "There are no vocabulary items to study."
            )
            return

        current_vocabulary = self.session.current()

        self.study_mode = "all"

        if current_vocabulary in study_list:
            start_vocabulary = current_vocabulary
        else:
            start_vocabulary = study_list[0]

        self.session = StudySession(
            study_list,
            start_vocabulary
        )

        self.show_front()

    def study_practice(self):
        study_list = self.get_practice_list()

        if not study_list:
            messagebox.showinfo(
                "Practice Empty",
                "There are no vocabulary items in Practice yet."
            )
            return

        current_vocabulary = self.session.current()

        self.study_mode = "practice"

        if current_vocabulary in study_list:
            start_vocabulary = current_vocabulary
        else:
            start_vocabulary = study_list[0]

        self.session = StudySession(
            study_list,
            start_vocabulary
        )

        self.show_front()

    def get_practice_list(self):
        if self.settings is None:
            return []

        practice_ids = self.settings.get_practice_ids()

        return [
            vocabulary
            for vocabulary in self.all_vocabulary_list
            if vocabulary.id in practice_ids
        ]

    def show_front(self):
        self.is_flipped = False

        self.clear_content()
        
        self.update_progress()

        vocabulary = self.session.current()

        if vocabulary is None:
            return

        word_label = tk.Label(
            self.content_frame,
            text=vocabulary.word,
            font=("Arial", 50, "bold"),
            wraplength=1200
        )

        word_label.pack(
            expand=True
        )

        self.flip_button.config(
            text="Flip"
        )

        self.update_practice_button()

    
    def show_back(self):
        self.is_flipped = True

        self.clear_content()

        vocabulary = self.session.current()

        if vocabulary is None:
            return

        # =========================
        # Word
        # =========================

        word_label = tk.Label(
            self.content_frame,
            text=vocabulary.word,
            font=("Arial", 26, "bold"),
            wraplength=1200
        )

        word_label.pack(
            
        )

        # =========================
        # Main content
        # =========================

        main_frame = tk.Frame(
            self.content_frame
        )

        main_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=10
        )

        # =========================
        # Left side - Information
        # =========================

        info_container = tk.Frame(
            main_frame
        )

        info_container.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # Scrollable information

        canvas = tk.Canvas(
            info_container
        )

        scrollbar = tk.Scrollbar(
            info_container,
            orient=tk.VERTICAL,
            command=canvas.yview
        )

        info_frame = tk.Frame(
            canvas
        )

        info_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=info_frame,
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
        # Vocabulary fields
        # =========================

        for field_name in self.manager.field_names:
            value = vocabulary.get(
                field_name
            )

            field_frame = tk.Frame(
                info_frame
            )

            field_frame.pack(
                fill=tk.X,
                padx=20,
                pady=5
            )

            field_label = tk.Label(
                field_frame,
                text=f"{field_name}:",
                font=("Arial", 11, "bold"),
                anchor="w",
                width=20
            )

            field_label.pack(
                side=tk.LEFT
            )

            value_label = tk.Label(
                field_frame,
                text=value,
                font=("Arial", 11),
                anchor="w",
                justify=tk.LEFT,
                wraplength=600
            )

            value_label.pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=True
            )

        # =========================
        # Right side - Image
        # =========================

        image_frame = tk.Frame(
            main_frame,
            width=500,
            height=400,
            relief=tk.GROOVE,
            borderwidth=2
        )

        image_frame.pack(
            side=tk.RIGHT,
            padx=(20, 0)
        )

        image_frame.pack_propagate(
            False
        )

        self.current_image = self.load_image(vocabulary)

        if self.current_image is not None:
            image_label = tk.Label(
                image_frame,
                image=self.current_image
            )

            image_label.pack(
                expand=True
            )

        else:
            choose_image_button = tk.Button(
                image_frame,
                text="Choose Image",
                command=lambda: self.choose_image(
                    vocabulary
                )
            )

            choose_image_button.pack(expand=True)

        # =========================
        # Bottom controls
        # =========================

        self.flip_button.config(
            text="Flip Back"
        )

        self.update_practice_button()
    def load_image(self, vocabulary):
        try:
            image_path = (
                self.image_manager.get_existing_image(
                    vocabulary.id
                )
            )

            if image_path is None:
                return None

            return self.image_manager.create_photo_image(
                image_path,
                max_width=500,
                max_height=400
            )

        except Exception as error:
            print("IMAGE ERROR:", error)
            return None
    
    def flip(self):
        if self.is_flipped:
            self.show_front()
        else:
            self.show_back()

    def next(self):
        self.session.next()

        self.show_front()

    def previous(self):
        self.session.previous()

        self.show_front()

    def random(self):
        self.session.random()

        self.show_front()
        
        
    def update_progress(self):
        total = self.session.count()

        if total == 0:
            self.progress_label.config(
                text="0 / 0"
            )
            return

        current = self.session.current_index + 1

        self.progress_label.config(
            text=f"{current} / {total}"
        )
        
    def choose_image(self, vocabulary):
        image_path = self.image_manager.select_and_save_image(
            self.window,
            vocabulary.id
        )

        if image_path is None:
            return

        print("IMAGE SAVED:", image_path)

        messagebox.showinfo(
            "Image Saved",
            "Image saved successfully.",
            parent=self.window
        )
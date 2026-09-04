import tkinter as tk
from tkinter import messagebox


from app.gui.vocabulary_input import VocabularyInput
from app.gui.flashcard import Flashcard


class VocabularyList:
    def __init__(
        self,
        parent,
        manager,
        settings
    ):
        self.parent = parent
        self.manager = manager
        self.settings = settings

        self.current_sort = "newest"
        self.current_vocabulary_list = []

        self.selected_row = None
        self.row_items = {}
        self.mouse_over_table = False

        # Load saved column visibility
        saved_settings = self.settings.load()

        saved_visible_fields = saved_settings.get(
            "visible_fields",
            []
        )

        if saved_visible_fields:
            self.visible_fields = [
                field
                for field in self.manager.field_names
                if field in saved_visible_fields
            ]
        else:
            self.visible_fields = [
                *self.manager.field_names
            ]

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Vocabulary List"
        )

        self.window.geometry(
            "1600x900+190+90"
        )

        self.window.minsize(
            900,
            500
        )

        self.create_widgets()

        self.show_newest()

    # ==================================================
    # WIDGETS
    # ==================================================

    def create_widgets(self):

        # ----------------------------------------------
        # Title
        # ----------------------------------------------

        title = tk.Label(
            self.window,
            text="Vocabulary",
            font=("Arial", 24)
        )

        title.pack(
            pady=20
        )

        # ----------------------------------------------
        # Buttons
        # ----------------------------------------------

        button_frame = tk.Frame(
            self.window
        )

        button_frame.pack(
            pady=10
        )

        newest_button = tk.Button(
            button_frame,
            text="Newest",
            width=12,
            command=self.show_newest
        )

        newest_button.pack(
            side=tk.LEFT,
            padx=3
        )

        az_button = tk.Button(
            button_frame,
            text="A-Z",
            width=12,
            command=self.show_a_z
        )

        az_button.pack(
            side=tk.LEFT,
            padx=3
        )

        edit_button = tk.Button(
            button_frame,
            text="Edit",
            width=12,
            command=self.edit_selected
        )

        edit_button.pack(
            side=tk.LEFT,
            padx=3
        )

        delete_button = tk.Button(
            button_frame,
            text="Delete",
            width=12,
            command=self.delete_selected
        )

        delete_button.pack(
            side=tk.LEFT,
            padx=3
        )

        flashcard_button = tk.Button(
            button_frame,
            text="Flashcard",
            width=12,
            command=self.open_flashcard
        )

        flashcard_button.pack(
            side=tk.LEFT,
            padx=3
        )

        self.practice_button = tk.Button(
            button_frame,
            text="Add to Practice",
            width=16,
            command=self.add_selected_to_practice
        )

        self.practice_button.pack(
            side=tk.LEFT,
            padx=3
        )

        learn_button = tk.Button(
            button_frame,
            text="Learn Saved Word",
            width=16,
            command=self.learn_selected
        )

        learn_button.pack(
            side=tk.LEFT,
            padx=3
        )

        columns_button = tk.Button(
            button_frame,
            text="Columns",
            width=12,
            command=self.open_columns
        )

        columns_button.pack(
            side=tk.LEFT,
            padx=3
        )

        # ----------------------------------------------
        # Table frame
        # ----------------------------------------------

        table_frame = tk.Frame(
            self.window
        )

        table_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=30,
            pady=20
        )

        self.table_frame = table_frame

        # ----------------------------------------------
        # Canvas
        # ----------------------------------------------

        self.canvas = tk.Canvas(
            table_frame,
            bg="white",
            highlightthickness=0
        )

        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # ----------------------------------------------
        # Vertical scrollbar
        # ----------------------------------------------

        scrollbar_y = tk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        # ----------------------------------------------
        # Horizontal scrollbar
        # ----------------------------------------------

        scrollbar_x = tk.Scrollbar(
            table_frame,
            orient=tk.HORIZONTAL,
            command=self.canvas.xview
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # ----------------------------------------------
        # Scroll configuration
        # ----------------------------------------------

        self.canvas.configure(
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------
        # Mouse wheel
        # ----------------------------------------------

        self.canvas.bind(
            "<Enter>",
            self.mouse_enter_table
        )

        self.canvas.bind(
            "<Leave>",
            self.mouse_leave_table
        )

        self.root_bind_mousewheel()

        # ----------------------------------------------
        # Initial button state
        # ----------------------------------------------

        self.update_practice_button()

    # ==================================================
    # MOUSE WHEEL
    # ==================================================

    def root_bind_mousewheel(self):

        self.window.bind(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.window.bind(
            "<Shift-MouseWheel>",
            self.on_shift_mousewheel
        )

    def mouse_enter_table(self, event):

        self.mouse_over_table = True

    def mouse_leave_table(self, event):

        self.mouse_over_table = False

    def on_mousewheel(self, event):

        if not self.mouse_over_table:
            return

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

        return "break"

    def on_shift_mousewheel(self, event):

        if not self.mouse_over_table:
            return

        self.canvas.xview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

        return "break"

    # ==================================================
    # TABLE
    # ==================================================

    def create_table(self):

        self.row_items = {}

        column_widths = {
            "Word": 180,
            "Type": 90,
            "Meaning VI": 180,
            "Meaning EN": 180,
            "Gender": 80,
            "Masculine": 150,
            "Feminine": 150,
            "Plural": 180,
            "Imparfait": 130,
            "Past (PC)": 130,
            "Present": 130,
            "Futur simple": 130,
            "Conditionnel": 130,
            "Example (FR)": 320,
            "Example (VI)": 320,
            "Ghi chú": 200
        }

        headers = [
            "Word",
            *self.visible_fields
        ]

        header_height = 45
        row_height = 45

        self.column_widths = []

        # ----------------------------------------------
        # Clear canvas
        # ----------------------------------------------

        self.canvas.delete(
            "all"
        )

        # ----------------------------------------------
        # Header
        # ----------------------------------------------

        x = 0

        for header in headers:

            width = column_widths.get(
                header,
                150
            )

            self.column_widths.append(
                width
            )

            self.canvas.create_rectangle(
                x,
                0,
                x + width,
                header_height,
                outline="black",
                width=1,
                fill="lightgray"
            )

            self.canvas.create_text(
                x + 10,
                header_height / 2,
                text=header,
                anchor="w",
                font=("Arial", 11, "bold")
            )

            x += width

        # ----------------------------------------------
        # Rows
        # ----------------------------------------------

        for row_index, vocabulary in enumerate(
            self.current_vocabulary_list
        ):

            self.draw_row(
                row_index,
                vocabulary,
                headers,
                header_height,
                row_height
            )

        # ----------------------------------------------
        # Scroll region
        # ----------------------------------------------

        total_width = sum(
            self.column_widths
        )

        total_height = (
            header_height
            +
            len(self.current_vocabulary_list)
            * row_height
        )

        self.canvas.configure(
            scrollregion=(
                0,
                0,
                total_width,
                total_height
            )
        )

    # ==================================================
    # DRAW ROW
    # ==================================================

    def draw_row(
        self,
        row_index,
        vocabulary,
        headers,
        header_height,
        row_height
    ):

        y = (
            header_height
            +
            row_index * row_height
        )

        self.row_items[row_index] = {
            "backgrounds": []
        }

        values = []

        for field_name in headers:

            if field_name == "Word":
                value = vocabulary.word
            else:
                value = vocabulary.get(
                    field_name
                )

            values.append(
                value
            )

        x = 0

        for column_index, value in enumerate(
            values
        ):

            width = self.column_widths[
                column_index
            ]

            # ------------------------------------------
            # Background
            # ------------------------------------------

            rectangle_id = self.canvas.create_rectangle(
                x,
                y,
                x + width,
                y + row_height,
                outline="",
                fill="white"
            )

            self.row_items[
                row_index
            ]["backgrounds"].append(
                rectangle_id
            )

            # ------------------------------------------
            # Text
            # ------------------------------------------

            text_color = self.get_text_color(
                headers[column_index],
                value,
                vocabulary
            )

            text_id = self.canvas.create_text(
                x + 10,
                y + row_height / 2,
                text=value,
                anchor="w",
                fill=text_color,
                font=("Arial", 11)
            )

            # ------------------------------------------
            # Vertical border
            # ------------------------------------------

            vertical_border_id = self.canvas.create_line(
                x + width,
                y,
                x + width,
                y + row_height,
                fill="#D0D0D0",
                width=1
            )

            # ------------------------------------------
            # Horizontal border
            # ------------------------------------------

            horizontal_border_id = self.canvas.create_line(
                x,
                y + row_height,
                x + width,
                y + row_height,
                fill="black",
                width=2
            )

            # ------------------------------------------
            # Click
            # ------------------------------------------

            self.canvas.tag_bind(
                rectangle_id,
                "<Button-1>",
                lambda event, index=row_index:
                    self.select_row(index)
            )

            self.canvas.tag_bind(
                text_id,
                "<Button-1>",
                lambda event, index=row_index:
                    self.select_row(index)
            )

            self.canvas.tag_bind(
                vertical_border_id,
                "<Button-1>",
                lambda event, index=row_index:
                    self.select_row(index)
            )

            self.canvas.tag_bind(
                horizontal_border_id,
                "<Button-1>",
                lambda event, index=row_index:
                    self.select_row(index)
            )

            # ------------------------------------------
            # Double click
            # ------------------------------------------

            self.canvas.tag_bind(
                rectangle_id,
                "<Double-Button-1>",
                lambda event, index=row_index:
                    self.double_click_row(index)
            )

            self.canvas.tag_bind(
                text_id,
                "<Double-Button-1>",
                lambda event, index=row_index:
                    self.double_click_row(index)
            )

            x += width

    # ==================================================
    # CELL COLORS
    # ==================================================

    def get_text_color(
        self,
        field_name,
        value,
        vocabulary
    ):

        # ----------------------------------------------
        # Practice
        # ----------------------------------------------

        if field_name == "Word":

            if self.settings.is_in_practice(
                vocabulary.id
            ):
                return "red"

            return "black"

        # ----------------------------------------------
        # Type
        # ----------------------------------------------

        if field_name == "Type":

            if value == "noun":
                return "blue"

            if value == "verb":
                return "orange"

        # ----------------------------------------------
        # Gender
        # ----------------------------------------------

        if field_name == "Gender":

            if value == "m":
                return "blue"

            if value == "f":
                return "red"

        return "black"

    # ==================================================
    # SELECT
    # ==================================================

    def select_row(
        self,
        row_index
    ):

        # Remove old selection

        if self.selected_row is not None:

            self.set_row_background(
                self.selected_row,
                "white"
            )

        # New selection

        self.selected_row = row_index

        self.set_row_background(
            row_index,
            "#E3F2FD"
        )

        self.update_practice_button()

    def set_row_background(
        self,
        row_index,
        background
    ):

        if row_index not in self.row_items:
            return

        backgrounds = self.row_items[
            row_index
        ]["backgrounds"]

        for rectangle_id in backgrounds:

            self.canvas.itemconfig(
                rectangle_id,
                fill=background
            )

    # ==================================================
    # SELECTED VOCABULARY
    # ==================================================

    def get_selected_vocabulary(self):

        if self.selected_row is None:
            return None

        if self.selected_row >= len(
            self.current_vocabulary_list
        ):
            return None

        return self.current_vocabulary_list[
            self.selected_row
        ]

    # ==================================================
    # PRACTICE BUTTON
    # ==================================================

    def update_practice_button(self):

        if not hasattr(
            self,
            "practice_button"
        ):
            return

        vocabulary = (
            self.get_selected_vocabulary()
        )

        if vocabulary is None:

            self.practice_button.config(
                text="Add to Practice"
            )

            return

        if self.settings.is_in_practice(
            vocabulary.id
        ):

            self.practice_button.config(
                text="Remove from Practice"
            )

        else:

            self.practice_button.config(
                text="Add to Practice"
            )

    def add_selected_to_practice(self):

        vocabulary = (
            self.get_selected_vocabulary()
        )

        if vocabulary is None:
            return

        if self.settings.is_in_practice(
            vocabulary.id
        ):

            self.settings.remove_practice(
                vocabulary.id
            )

        else:

            self.settings.add_practice(
                vocabulary.id
            )

        # Update only the Word color

        if self.selected_row is not None:

            headers = [
                "Word",
                *self.visible_fields
            ]

            word_column_index = 0

            # Find the Word background
            # and redraw its text

            self.refresh_row(
                self.selected_row
            )

        self.update_practice_button()

        # Restore selection

        if self.selected_row is not None:

            self.set_row_background(
                self.selected_row,
                "#E3F2FD"
            )

    # ==================================================
    # REFRESH ROW
    # ==================================================

    def refresh_row(
        self,
        row_index
    ):

        if row_index >= len(
            self.current_vocabulary_list
        ):
            return

        vocabulary = (
            self.current_vocabulary_list[
                row_index
            ]
        )

        headers = [
            "Word",
            *self.visible_fields
        ]

        # Redraw complete table is safer
        # for now because cell text colors
        # are controlled individually.

        self.create_table()

        # Restore selected row

        if row_index < len(
            self.current_vocabulary_list
        ):

            self.selected_row = row_index

            self.set_row_background(
                row_index,
                "#E3F2FD"
            )

    # ==================================================
    # SORTING
    # ==================================================

    def show_newest(self):

        self.current_sort = "newest"

        self.current_vocabulary_list = (
            self.manager.sort_newest()
        )

        self.selected_row = None

        self.create_table()

        self.update_practice_button()

    def show_a_z(self):

        self.current_sort = "a_z"

        self.current_vocabulary_list = (
            self.manager.sort_a_z()
        )

        self.selected_row = None

        self.create_table()

        self.update_practice_button()

    # ==================================================
    # EDIT
    # ==================================================

    def edit_selected(self):
        vocabulary = self.get_selected_vocabulary()

        if vocabulary is None:
            messagebox.showwarning(
                "No Selection",
                "Please select a vocabulary first.",
                parent=self.window
            )

            self.window.lift()
            self.window.focus_force()
            return

        VocabularyInput(
            self.window,
            self.manager,
            vocabulary,
            on_close=self.refresh_after_edit
        )

    
    #refresh
    def refresh_after_edit(self):
        self.selected_row = None

        if self.current_sort == "a_z":
            self.show_a_z()
        else:
            self.show_newest()

        self.window.lift()
        self.window.focus_force()
        
    # ==================================================
    # DELETE
    # ==================================================

    def delete_selected(self):

        vocabulary = (
            self.get_selected_vocabulary()
        )

        if vocabulary is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a vocabulary first."
            )

            self.window.lift()
            self.window.focus_force()

            return

        confirmed = messagebox.askyesno(
            "Delete Vocabulary",
            f"Delete '{vocabulary.word}'?",
            parent=self.window
        )

        if not confirmed:

            self.window.lift()
            self.window.focus_force()

            return

        self.manager.delete(
            vocabulary
        )

        self.manager.save()

        # Remove from Practice too
        if self.settings.is_in_practice(
            vocabulary.id
        ):

            self.settings.remove_practice(
                vocabulary.id
            )

        self.selected_row = None

        if self.current_sort == "a_z":
            self.show_a_z()
        else:
            self.show_newest()

        # Return focus to Vocabulary List
        self.window.lift()
        self.window.focus_force()

    # ==================================================
    # FLASHCARD
    # ==================================================

    def open_flashcard(self):

        vocabulary_list = (
            self.manager.get_all()
        )

        if not vocabulary_list:

            messagebox.showwarning(
                "No Vocabulary",
                "There are no vocabulary items to study."
            )

            return

        Flashcard(
            self.window,
            self.manager,
            vocabulary_list,
            None,
            self.settings
        )

    # ==================================================
    # LEARN SAVED WORD
    # ==================================================

    def learn_selected(self):

        vocabulary = (
            self.get_selected_vocabulary()
        )

        if vocabulary is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a vocabulary first.",
                parent=self.window
            )

            self.window.lift()
            self.window.focus_force()

            return

        practice_ids = (
            self.settings.get_practice_ids()
        )

        vocabulary_list = [
            item
            for item in self.manager.get_all()
            if item.id in practice_ids
        ]

        if not vocabulary_list:

            messagebox.showinfo(
                "Practice Empty",
                "There are no vocabulary items in Practice.",
                parent=self.window
            )

            self.window.lift()
            self.window.focus_force()

            return

        if vocabulary.id not in practice_ids:

            messagebox.showwarning(
                "Not in Practice",
                f"'{vocabulary.word}' is not in Practice.",
                parent=self.window
            )

            self.window.lift()
            self.window.focus_force()

            return

        Flashcard(
            self.window,
            self.manager,
            vocabulary_list,
            None,
            self.settings,
            on_practice_changed=self.refresh_after_practice_change,
            study_mode="practice"
        )

    
    
    def refresh_after_practice_change(self):
        self.create_table()



    # ==================================================
    # DOUBLE CLICK
    # ==================================================

    def double_click_row(
        self,
        row_index
    ):

        self.select_row(
            row_index
        )

        self.edit_selected()

    # ==================================================
    # COLUMNS
    # ==================================================

    def open_columns(self):

        ColumnsWindow(
            self.window,
            self.manager,
            self.visible_fields,
            self.apply_columns
        )

    def apply_columns(
        self,
        visible_fields
    ):

        self.visible_fields = (
            visible_fields
        )

        self.settings.set_visible_fields(
            self.visible_fields
        )

        self.selected_row = None

        self.create_table()

        self.update_practice_button()


# ======================================================
# COLUMNS WINDOW
# ======================================================

class ColumnsWindow:

    def __init__(
        self,
        parent,
        manager,
        current_visible_fields,
        callback
    ):

        self.parent = parent
        self.manager = manager
        self.callback = callback

        self.window = tk.Toplevel(
            parent
        )

        self.window.title(
            "Show / Hide Columns"
        )

        self.window.geometry(
            "400x650"
        )

        self.window.resizable(
            False,
            False
        )

        self.variables = {}

        self.create_widgets(
            current_visible_fields
        )

    def create_widgets(
        self,
        current_visible_fields
    ):

        title = tk.Label(
            self.window,
            text="Show / Hide Columns",
            font=("Arial", 18)
        )

        title.pack(
            pady=20
        )

        container = tk.Frame(
            self.window
        )

        container.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20
        )

        canvas = tk.Canvas(
            container
        )

        scrollbar = tk.Scrollbar(
            container,
            orient=tk.VERTICAL,
            command=canvas.yview
        )

        checkbox_frame = tk.Frame(
            canvas
        )

        checkbox_frame.bind(
            "<Configure>",
            lambda event:
                canvas.configure(
                    scrollregion=canvas.bbox(
                        "all"
                    )
                )
        )

        canvas.create_window(
            (0, 0),
            window=checkbox_frame,
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

        # ----------------------------------------------
        # Word
        # ----------------------------------------------

        word_variable = tk.BooleanVar(
            value=True
        )

        word_checkbutton = tk.Checkbutton(
            checkbox_frame,
            text="Word",
            variable=word_variable,
            state=tk.DISABLED,
            anchor="w"
        )

        word_checkbutton.pack(
            fill=tk.X,
            pady=3
        )

        # ----------------------------------------------
        # Other fields
        # ----------------------------------------------

        for field_name in (
            self.manager.field_names
        ):

            variable = tk.BooleanVar(
                value=field_name in current_visible_fields
            )

            self.variables[
                field_name
            ] = variable

            checkbutton = tk.Checkbutton(
                checkbox_frame,
                text=field_name,
                variable=variable,
                anchor="w"
            )

            checkbutton.pack(
                fill=tk.X,
                pady=3
            )

        # ----------------------------------------------
        # Buttons
        # ----------------------------------------------

        button_frame = tk.Frame(
            self.window
        )

        button_frame.pack(
            pady=15
        )

        apply_button = tk.Button(
            button_frame,
            text="Apply",
            width=15,
            command=self.apply
        )

        apply_button.pack(
            side=tk.LEFT,
            padx=5
        )

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            width=15,
            command=self.window.destroy
        )

        cancel_button.pack(
            side=tk.LEFT,
            padx=5
        )

    def apply(self):

        visible_fields = []

        for field_name in (
            self.manager.field_names
        ):

            if self.variables[
                field_name
            ].get():

                visible_fields.append(
                    field_name
                )

        self.callback(
            visible_fields
        )

        self.window.destroy()
import tkinter as tk

from app.data.database import VocabularyDatabase
from app.data.vocabulary_manager import VocabularyManager


class ColorTable:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        self.root.title(
            "French Flashcard - Table Prototype"
        )

        self.root.geometry(
            "1200x650"
        )

        self.selected_row = None
        self.row_items = {}

        self.vocabulary_list = (
            self.manager.sort_newest()
        )

        self.headers = [
            "Word",
            "Type",
            "Meaning VI",
            "Meaning EN",
            "Gender"
        ]

        self.column_widths = [
            200,
            120,
            220,
            220,
            100
        ]

        self.header_height = 45
        self.row_height = 45

        self.create_widgets()

        self.draw_table()

    
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
    # WIDGETS
    # ==================================================

    
    
    
    def create_widgets(self):

        # ----------------------------------------------
        # Table container
        # ----------------------------------------------

        table_frame = tk.Frame(
            self.root
        )

        table_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=20
        )

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
        
         # Mouse wheel only when cursor is over table
        self.canvas.bind(
            "<Enter>",
            self.mouse_enter_table
        )

        self.canvas.bind(
            "<Leave>",
            self.mouse_leave_table
        )

        self.mouse_over_table = False

        # ----------------------------------------------
        # Connect scrollbars
        # ----------------------------------------------

        self.canvas.configure(
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
            
        )
                # Mouse wheel scrolling
        self.root.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.root.bind_all(
            "<Shift-MouseWheel>",
            self.on_shift_mousewheel
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
        # Selected label
        # ----------------------------------------------

        self.selected_label = tk.Label(
            self.root,
            text="Selected: None",
            font=("Arial", 12)
        )

        self.selected_label.pack(
            pady=(0, 15)
        )

    # ==================================================
    # DRAW TABLE
    # ==================================================

    def draw_table(self):

        # ----------------------------------------------
        # Header
        # ----------------------------------------------

        x = 0

        for column_index, header in enumerate(
            self.headers
        ):

            width = self.column_widths[
                column_index
            ]

            self.canvas.create_rectangle(
                x,
                0,
                x + width,
                self.header_height,
                outline="black",
                width=1,
                fill="lightgray"
            )

            self.canvas.create_text(
                x + 10,
                self.header_height / 2,
                text=header,
                anchor="w",
                font=("Arial", 11, "bold")
            )

            x += width

        # ----------------------------------------------
        # Rows
        # ----------------------------------------------

        for row_index, vocabulary in enumerate(
            self.vocabulary_list
        ):

            self.draw_row(
                row_index,
                vocabulary
            )

        # ----------------------------------------------
        # Scroll region
        # ----------------------------------------------

        total_width = sum(
            self.column_widths
        )

        total_height = (
            self.header_height
            +
            len(self.vocabulary_list)
            * self.row_height
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
        vocabulary
    ):

        y = (
            self.header_height
            +
            row_index * self.row_height
        )

        self.row_items[row_index] = {
            "backgrounds": []
        }

        values = [
            vocabulary.word,
            vocabulary.get("Type"),
            vocabulary.get("Meaning VI"),
            vocabulary.get("Meaning EN"),
            vocabulary.get("Gender")
        ]

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
                y + self.row_height,
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
                column_index,
                value
            )

            text_id = self.canvas.create_text(
                x + 10,
                y + self.row_height / 2,
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
                y + self.row_height,
                fill="#D0D0D0",
                width=1
            )

            # ------------------------------------------
            # Horizontal border
            # ------------------------------------------

            horizontal_border_id = self.canvas.create_line(
                x,
                y + self.row_height,
                x + width,
                y + self.row_height,
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
        column_index,
        value
    ):

        # Type
        if column_index == 1:

            if value == "noun":
                return "blue"

            if value == "verb":
                return "orange"

        # Gender
        if column_index == 4:

            if value == "m":
                return "blue"

            if value == "f":
                return "red"

        return "black"

    # ==================================================
    # SELECT ROW
    # ==================================================

    def select_row(
        self,
        row_index
    ):

        # Remove previous selection
        if self.selected_row is not None:

            self.set_row_background(
                self.selected_row,
                "white"
            )

        # Select new row
        self.selected_row = row_index

        self.set_row_background(
            row_index,
            "#E3F2FD"
        )

        vocabulary = (
            self.vocabulary_list[
                row_index
            ]
        )

        self.selected_label.config(
            text=f"Selected: {vocabulary.word}"
        )

    # ==================================================
    # ROW BACKGROUND
    # ==================================================

    def set_row_background(
        self,
        row_index,
        background
    ):

        backgrounds = self.row_items[
            row_index
        ]["backgrounds"]

        for rectangle_id in backgrounds:

            self.canvas.itemconfig(
                rectangle_id,
                fill=background
            )

    # ==================================================
    # DOUBLE CLICK
    # ==================================================

    def double_click_row(
        self,
        row_index
    ):

        vocabulary = (
            self.vocabulary_list[
                row_index
            ]
        )

        self.selected_label.config(
            text=f"Double-clicked: {vocabulary.word}"
        )
    
# ======================================================
# START
# ======================================================

database = VocabularyDatabase(
    "database/vocabulary.json"
)

manager = VocabularyManager(
    database
)

manager.load()

root = tk.Tk()

app = ColorTable(
    root,
    manager
)

root.mainloop()
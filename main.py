import tkinter as tk

from app.data.database import VocabularyDatabase
from app.data.settings import Settings
from app.data.vocabulary_manager import VocabularyManager
from app.gui.main_window import MainWindow


database = VocabularyDatabase(
    "database/vocabulary.json"
)

settings = Settings(
    "database/settings.json"
)

manager = VocabularyManager(
    database
)

manager.load()

root = tk.Tk()

app = MainWindow(
    root,
    manager,
    settings
)

root.mainloop()
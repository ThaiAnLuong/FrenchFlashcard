import os
import shutil
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk


class ImageManager:
    def __init__(self, image_directory="data/images"):
        self.image_directory = image_directory

        os.makedirs(
            self.image_directory,
            exist_ok=True
        )

    def get_image_path(
        self,
        vocabulary_id,
        extension
    ):
        return os.path.join(
            self.image_directory,
            f"{vocabulary_id}{extension}"
        )

    def get_existing_image(
        self,
        vocabulary_id
    ):
        if not os.path.exists(
            self.image_directory
        ):
            return None

        for file_name in os.listdir(
            self.image_directory
        ):
            name, extension = os.path.splitext(
                file_name
            )

            if name == vocabulary_id:
                return os.path.join(
                    self.image_directory,
                    file_name
                )

        return None

    def select_and_save_image(
        self,
        parent,
        vocabulary_id
    ):
        file_path = filedialog.askopenfilename(
            parent=parent,
            title="Select Image",
            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg *.gif *.bmp"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return None

        _, extension = os.path.splitext(
            file_path
        )

        extension = extension.lower()

        destination = self.get_image_path(
            vocabulary_id,
            extension
        )

        shutil.copy2(
            file_path,
            destination
        )

        return destination

    def create_photo_image(
        self,
        file_path,
        max_width=500,
        max_height=400
    ):
        if not file_path:
            return None

        if not os.path.exists(
            file_path
        ):
            return None

        image = Image.open(
            file_path
        )

        image.thumbnail(
            (max_width, max_height),
            Image.Resampling.LANCZOS
        )

        return ImageTk.PhotoImage(
            image
        )
        
    def delete_image(self, vocabulary_id):
        image_path = self.get_existing_image(
            vocabulary_id
        )

        if image_path is None:
            return

        os.remove(
            image_path
        )
import os
import tkinter as tk

import requests


class ImageManager:
    def __init__(self, image_directory="data/images"):
        self.image_directory = image_directory

        os.makedirs(
            self.image_directory,
            exist_ok=True
        )

    def download_image(self, url):
        response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "FrenchFlashcard/1.0 "
                    "(vocabulary learning application)"
                )
            },
            timeout=10
        )

        response.raise_for_status()

        return response.content

    def create_photo_image(self, image_data):
        photo_image = tk.PhotoImage(
            data=image_data
        )

        return photo_image
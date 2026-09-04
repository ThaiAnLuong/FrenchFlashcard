import json
import os


class Settings:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        if not os.path.exists(self.file_path):
            return {
                "visible_fields": [],
                "practice_ids": []
            }

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:
            settings = json.load(file)

        if "visible_fields" not in settings:
            settings["visible_fields"] = []

        if "practice_ids" not in settings:
            settings["practice_ids"] = []

        return settings

    def save(self, settings):
        folder = os.path.dirname(
            self.file_path
        )

        if folder:
            os.makedirs(
                folder,
                exist_ok=True
            )

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                settings,
                file,
                ensure_ascii=False,
                indent=4
            )

    def set_visible_fields(self, visible_fields):
        settings = self.load()

        settings["visible_fields"] = visible_fields

        self.save(settings)

    def get_practice_ids(self):
        settings = self.load()

        return settings.get(
            "practice_ids",
            []
        )

    def add_practice(self, vocabulary_id):
        settings = self.load()

        practice_ids = settings.get(
            "practice_ids",
            []
        )

        if vocabulary_id not in practice_ids:
            practice_ids.append(
                vocabulary_id
            )

        settings["practice_ids"] = practice_ids

        self.save(settings)

    def remove_practice(self, vocabulary_id):
        settings = self.load()

        practice_ids = settings.get(
            "practice_ids",
            []
        )

        if vocabulary_id in practice_ids:
            practice_ids.remove(
                vocabulary_id
            )

        settings["practice_ids"] = practice_ids

        self.save(settings)

    def is_in_practice(self, vocabulary_id):
        practice_ids = self.get_practice_ids()

        return vocabulary_id in practice_ids
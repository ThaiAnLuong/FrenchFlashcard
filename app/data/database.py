import json
import os

from app.models.vocabulary import Vocabulary


class VocabularyDatabase:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, vocabulary_list):
        data = []

        for vocabulary in vocabulary_list:
            data.append({
                "id": vocabulary.id,
                "word": vocabulary.word,
                "data": vocabulary.data,
                "created_at": vocabulary.created_at
            })

        folder = os.path.dirname(self.file_path)

        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def load(self):
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        vocabulary_list = []

        for item in data:
            vocabulary = Vocabulary(
                word=item["word"],
                data=item["data"],
                vocabulary_id=item.get("id"),
                created_at=item.get("created_at")
            )

            vocabulary_list.append(vocabulary)

        return vocabulary_list
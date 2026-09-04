import uuid
from datetime import datetime


class Vocabulary:
    def __init__(self, word, data=None, vocabulary_id=None, created_at=None):
        self.id = vocabulary_id if vocabulary_id else str(uuid.uuid4())
        self.word = word
        self.data = data if data is not None else {}
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def get(self, key):
        return self.data.get(key, "#")

    def set(self, key, value):
        if value is None or value.strip() == "":
            value = "#"

        self.data[key] = value

    def __str__(self):
        return self.word
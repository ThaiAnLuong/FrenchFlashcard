from app.data.csv_handler import load_csv


class VocabularyManager:
    def __init__(self, database):
        self.vocabulary_list = []
        self.database = database

        self.field_names = [
            "meaning",
            "gender",
            "pronunciation"
            "type"
        ]

    def add(self, vocabulary):
        self.vocabulary_list.append(vocabulary)

    def delete(self, vocabulary):
        if vocabulary in self.vocabulary_list:
            self.vocabulary_list.remove(vocabulary)

    def edit(self, vocabulary, word=None, data=None):
        if vocabulary not in self.vocabulary_list:
            return

        if word is not None:
            vocabulary.word = word

        if data is not None:
            vocabulary.data = data

    def get_all(self):
        return self.vocabulary_list

    def sort_a_z(self):
        return sorted(
            self.vocabulary_list,
            key=lambda vocabulary: vocabulary.word.lower()
        )

    def sort_newest(self):
        return sorted(
            self.vocabulary_list,
            key=lambda vocabulary: vocabulary.created_at,
            reverse=True
        )

    def count(self):
        return len(self.vocabulary_list)

    def clear(self):
        self.vocabulary_list.clear()

    def replace_all(self, vocabulary_list):
        self.vocabulary_list = vocabulary_list

    def save(self):
        self.database.save(self.vocabulary_list)

    def load(self):
        vocabulary_list = self.database.load()

        self.replace_all(vocabulary_list)

        field_names = []

        for vocabulary in vocabulary_list:
            for field_name in vocabulary.data.keys():
                if field_name not in field_names:
                    field_names.append(field_name)

        if field_names:
            self.field_names = field_names

    def import_csv(self, file_path):
        vocabulary_list, field_names = load_csv(file_path)

        for vocabulary in vocabulary_list:
            self.add(vocabulary)

        if field_names:
            self.field_names = field_names

        self.save()

        return len(vocabulary_list)
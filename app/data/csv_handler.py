import csv

from app.models.vocabulary import Vocabulary


def load_csv(file_path):
    vocabulary_list = []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(
                "CSV file is empty or has no header."
            )

        if "word" not in reader.fieldnames:
            raise ValueError(
                "CSV file must contain a 'word' column."
            )

        for row_number, row in enumerate(reader, start=2):
            word = row["word"]

            if word is None or word.strip() == "":
                raise ValueError(
                    f"Row {row_number}: 'word' cannot be empty."
                )

            data = {}

            for key, value in row.items():
                if key == "word":
                    continue

                if value is None or value.strip() == "":
                    value = "#"

                data[key] = value

            vocabulary = Vocabulary(
                word.strip(),
                data
            )

            vocabulary_list.append(vocabulary)

    return vocabulary_list
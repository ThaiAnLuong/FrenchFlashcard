import csv

from app.models.vocabulary import Vocabulary


def load_csv(file_path):
    vocabulary_list = []
    field_names = []

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(
                "CSV file is empty or has no header."
            )

        if "word" not in reader.fieldnames:
            raise ValueError(
                "CSV file must contain a 'word' column."
            )

        field_names = [
            field
            for field in reader.fieldnames
            if field != "word"
        ]

        for row_number, row in enumerate(reader, start=2):
            word = row["word"]

            if word is None or word.strip() == "":
                raise ValueError(
                    f"Row {row_number}: 'word' cannot be empty."
                )

            data = {}

            for field_name in field_names:
                value = row.get(field_name)

                if value is None or value.strip() == "":
                    value = "#"

                data[field_name] = value.strip()

            vocabulary = Vocabulary(
                word.strip(),
                data
            )

            vocabulary_list.append(vocabulary)

    return vocabulary_list, field_names
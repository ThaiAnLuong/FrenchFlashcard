import csv

from app.models.vocabulary import Vocabulary


FIELD_NAMES = [
    "Type",
    "Meaning VI",
    "Meaning EN",
    "Gender",
    "Masculine",
    "Feminine",
    "Plural",
    "Imparfait",
    "Past (PC)",
    "Present",
    "Futur simple",
    "Conditionnel",
    "Example (FR)",
    "Example (VI)",
    "Ghi chú"
]


def load_csv(file_path):
    vocabulary_list = []

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

        # Clean CSV header names
        csv_field_names = []

        for field in reader.fieldnames:
            if field is None:
                continue

            field = field.strip()

            if field != "":
                csv_field_names.append(field)

        # Word is required
        if "Word" not in csv_field_names:
            raise ValueError(
                "CSV file must contain a 'Word' column."
            )

        # Check for unsupported fields
        unsupported_fields = [
            field
            for field in csv_field_names
            if field != "Word"
            and field not in FIELD_NAMES
        ]

        if unsupported_fields:
            raise ValueError(
                "Unsupported CSV field(s): "
                + ", ".join(unsupported_fields)
            )

        # Use the standard field order
        data_field_names = [
            field
            for field in FIELD_NAMES
            if field in csv_field_names
        ]

        for row_number, row in enumerate(
            reader,
            start=2
        ):
            # Check whether the entire row is empty
            row_is_empty = True

            for value in row.values():
                if value is not None and value.strip() != "":
                    row_is_empty = False
                    break

            if row_is_empty:
                continue

            # Get Word
            word = row.get("Word")

            if word is None or word.strip() == "":
                raise ValueError(
                    f"Row {row_number}: 'Word' cannot be empty."
                )

            word = word.strip()

            # Create vocabulary data
            data = {}

            for field_name in data_field_names:
                value = row.get(field_name)

                if value is None or value.strip() == "":
                    value = "-"
                else:
                    value = value.strip()

                data[field_name] = value

            vocabulary = Vocabulary(
                word=word,
                data=data
            )

            vocabulary_list.append(
                vocabulary
            )

    return vocabulary_list, data_field_names
import random


class StudySession:
    def __init__(
        self,
        vocabulary_list,
        start_vocabulary=None
    ):
        self.vocabulary_list = vocabulary_list
        self.current_index = 0

        if start_vocabulary is not None:
            self.set_current(
                start_vocabulary
            )

    def current(self):
        if not self.vocabulary_list:
            return None

        return self.vocabulary_list[
            self.current_index
        ]

    def set_current(self, vocabulary):
        if vocabulary in self.vocabulary_list:
            self.current_index = (
                self.vocabulary_list.index(
                    vocabulary
                )
            )

    def next(self):
        if not self.vocabulary_list:
            return None

        self.current_index += 1

        if self.current_index >= len(
            self.vocabulary_list
        ):
            self.current_index = 0

        return self.current()

    def previous(self):
        if not self.vocabulary_list:
            return None

        self.current_index -= 1

        if self.current_index < 0:
            self.current_index = (
                len(self.vocabulary_list) - 1
            )

        return self.current()

    def random(self):
        if not self.vocabulary_list:
            return None

        self.current_index = random.randrange(
            len(self.vocabulary_list)
        )

        return self.current()

    def count(self):
        return len(
            self.vocabulary_list
        )
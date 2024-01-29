from __future__ import annotations
from random import choice


class StressData:
    stress_table: dict[str, str]
    specifications: dict[str, str]

    def __init__(self, stress_table: dict[str, str], specifications: dict[str, str]):
        self.stress_table = stress_table
        self.specifications = specifications

    def generate_task(self) -> str:
        word = choice(tuple(self.stress_table.keys()))
        if word in self.specifications:
            word += " " + self.specifications[word]
        return word

    def stress(self, word: str):
        word = word.lower()
        return self.stress_table[word]

    def is_correct(self, stressed_word: str):
        word_key = stressed_word.lower()
        return self.stress_table[word_key] == stressed_word

    @classmethod
    def from_file(cls, path: str) -> StressData:
        obj = cls({}, {})
        with open(path, mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                word, *other = line.strip().split()
                word_key = word.lower()
                if other:
                    specification = " ".join(other)
                    obj.specifications[word_key] = specification
                obj.stress_table[word.lower()] = word
        return obj

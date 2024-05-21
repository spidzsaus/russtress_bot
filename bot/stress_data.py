from __future__ import annotations
from random import choice
from dataclasses import dataclass

from bot.utils import hide_yo


@dataclass
class Task:
    text: str
    is_variable: bool = False
    variable_id: int = None

    def __str__(self) -> str:
        return self.text


class StressData:
    stress_table: dict[str | tuple[str, int], str]
    specifications: dict[str, str]
    variable_stresses: list[str]

    def __init__(
        self,
        stress_table: dict[str, str],
        specifications: dict[str, str],
        variable_stresses: list[str],
    ):
        self.stress_table = stress_table
        self.specifications = specifications
        self.variable_stresses = variable_stresses

    def contains(self, word: str) -> bool:
        return (
            word.lower() in self.stress_table or word.lower() in self.variable_stresses
        )

    def generate_task(self) -> Task:
        word = choice(tuple(self.stress_table.keys()))
        match word:
            case (str(), int()):
                return_word = word[0]
                variable_id = word[1]
                if word in self.specifications:
                    return_word += " " + self.specifications[word]
                return Task(
                    text=hide_yo(return_word), is_variable=True, variable_id=variable_id
                )
            case _:
                if word in self.specifications:
                    word += " " + self.specifications[word]
                return Task(text=hide_yo(word))

    def stress(self, word: str, variable_id: int = None) -> str:
        word = word.lower()
        if variable_id is None and self.is_variable(word):
            return ", или ".join(
                f"{self.stress_table[key]} {spec}"
                for key, spec in self.specifications.items()
                if key[0].lower() == word
            )
        if variable_id is None:
            return self.stress_table[word]
        return self.stress_table[(word, variable_id)]

    def is_variable(self, word: str):
        return word.lower() in self.variable_stresses

    def deduct_variable_id(self, msg_text: str, target_word: str):
        # i hate this but like duh
        specifications_and_ids = (
            (value, key[1])
            for key, value in self.specifications.items()
            if key[0].lower() == target_word
        )
        for spec, id in specifications_and_ids:
            if spec in msg_text:
                return id
        return None

    def is_correct(self, stressed_word: str, variable_id: int = None) -> bool:
        word_key = stressed_word.lower()
        if variable_id is not None:
            word_key = (word_key, variable_id)
        elif variable_id is None and self.is_variable(word_key):
            # something weird happened but ok
            check = stressed_word in self.stress_table.values()
            yo_check = stressed_word in map(hide_yo, self.stress_table.values())
            return check or yo_check

        check = self.stress_table[word_key] == stressed_word
        yo_check = hide_yo(self.stress_table[word_key]) == stressed_word
        return check or yo_check

    @classmethod
    def from_file(cls, path: str) -> StressData:
        obj = cls({}, {}, [])
        variable_stresses_ids = {}

        with open(path, mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                word, *other = line.strip().split()
                word_key = word.lower()

                if word_key in obj.variable_stresses:
                    word_key = (word_key, variable_stresses_ids[word_key] + 1)
                    variable_stresses_ids[word_key] += 1

                if word_key in obj.stress_table:
                    obj.variable_stresses.append(word_key)
                    variable_stresses_ids[word_key] = 1
                    spec = obj.specifications.get(word_key, None)
                    stress = obj.stress_table.get(word_key)
                    del obj.stress_table[word_key]
                    del obj.specifications[word_key]

                    if spec is not None:
                        obj.specifications[(word_key, 0)] = spec
                    obj.stress_table[(word_key, 0)] = stress
                    word_key = (word_key, 1)

                if other:
                    specification = " ".join(other)
                    obj.specifications[word_key] = specification
                obj.stress_table[word_key] = word
                if "ё" in word_key:
                    obj.stress_table[hide_yo(word_key)] = word
        return obj

class Language:
    intro: tuple[str] = (
        "Привет. Короче, я пишу слово, а ты пишешь, как в нём правильно должны стоять ударения."
        " Ударение обозначай заглавной буквой, все остальные буквы кроме ударной гласной пиши"
        " строчными (ответы, начинающиеся с заглавной буквы, тоже принимаются)\nПоооогнали\n\n{task}",
    )
    visual_praise: str = "🔥🔥🔥"
    right_answer: tuple[str] = (
        "МЕГАХОРОШ{praise}\n\n{task}",
        "УЛЬТРАМЕГАХОРОШ{praise}\n\n{task}",
        "Ну ведь можешь, когда хочешь!{praise}\n\n{task}",
    )
    wrong_answer: tuple[str] = (
        "skill issue.\nправильный ответ *{right_answer}*\n\n{task}",
        "знаю, тупо, но\nправильный ответ *{right_answer}*\n\n{task}",
        "увы и ах!\nправильный ответ *{right_answer}*\n\n{task}",
    )
    wildcard: tuple[str] = ("Что-то не то. Попробуем ещё раз.\n\n{task}",)

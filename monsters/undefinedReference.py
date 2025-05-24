from .enemy import Enemy
import os

class UndefinedReference(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            x, y,
            name="Undefined Reference",
            hp=100,
            damage=10,
            color=(139, 69, 19),
            speed=2,
            quiz_question="What does 'undefined reference to main' mean when compiling in C?",
            quiz_options=[
                "A) The main function is missing or has a typo",
                "B) There is a missing semicolon in the code"
            ],
            quiz_answer=0,
            battle_image_path=os.path.join("assets", "monsters", "undefined2.png")
        )

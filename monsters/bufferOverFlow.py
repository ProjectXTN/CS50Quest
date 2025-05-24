from .enemy import Enemy
import os

class bufferOverFlow(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            x, y,
            name="Buffer Overflow",
            hp=110,
            damage=18,
            color=(128, 0, 0),
            speed=2,
            quiz_question="Which situation can cause a buffer overflow in C?",
            quiz_options=[
                "A) Correctly using a for loop inside bounds",
                "B) Writing past the end of an array"
            ],
            quiz_answer=1,
            battle_image_path=os.path.join("assets", "monsters", "bufferover2.png")
        )

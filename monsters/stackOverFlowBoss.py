from .enemy import Enemy
import os
from typing import List

class StackOverflowBoss(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            x, y,
            name="Stack Overflow",
            hp=200,
            damage=25,
            color=(200, 0, 100),
            speed=1,
            quiz_question=[
                "What causes a stack overflow in most programming languages?",
                "What is a common sign of a stack overflow during execution?"
            ],
            quiz_options=[
                [
                    "A) Allocating memory with malloc",
                    "B) Closing a file",
                    "C) Using arrays properly",
                    "D) Infinite recursion"
                ],
                [
                    "A) Program runs slower",
                    "B) 'Segmentation fault' or crash",
                    "C) Missing variable value",
                    "D) Compilation error"
                ]
            ],
            quiz_answer=[3, 1],
            map_image_path=os.path.join("assets", "monsters", "stackoverflow_icon.png"),
            battle_image_path=os.path.join("assets", "monsters", "stackover_boss2.png")
        )

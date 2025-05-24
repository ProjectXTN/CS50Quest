from .enemy import Enemy
import os

class memoryLeak(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            x, y,
            name="Memory Leak",
            hp=120,
            damage=16,
            color=(200, 200, 200),
            speed=2,
            quiz_question="What is a memory leak in C?",
            quiz_options=[
                "A) Forgetting to free memory allocated with malloc/calloc",
                "B) Using printf without including stdio.h"
            ],
            quiz_answer=0,
            battle_image_path=os.path.join("assets", "monsters", "memorryleak2.png")
        )

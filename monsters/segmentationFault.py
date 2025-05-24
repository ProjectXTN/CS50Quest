import os
from .enemy import Enemy

class segmentationFault(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            name="Segmentation Fault",
            hp=80,
            damage=14,
            color=(50, 205, 50),
            speed=2,
            quiz_question="What is the most common cause of a segmentation fault in C?",
            quiz_options=[
                "A) Using a correct pointer",
                "B) Accessing memory you don't own"
            ],
            quiz_answer=1,
            battle_image_path=os.path.join("assets", "monsters", "segfault2.png")
        )

import pygame
import os
from typing import List, Tuple, Optional
from map.map import TILE_SIZE
from .util import astar

class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        name: str = "Enemy",
        hp: int = 10,
        damage: int = 1,
        color: Tuple[int, int, int] = (255, 0, 0),
        speed: int = 1,
        quiz_question: Optional[str] = None,
        quiz_options: Optional[List[str]] = None,
        quiz_answer: int = 0,
        agro_radius: int = 180,
        map_image_path: Optional[str] = os.path.join("assets", "monsters", "bug.png"),
        battle_image_path: Optional[str] = None
    ) -> None:
        super().__init__()
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.agro_radius = agro_radius

        # ---- MAP IMAGE ----
        if map_image_path and os.path.exists(map_image_path):
            map_img = pygame.image.load(map_image_path).convert_alpha()
            self.image = pygame.transform.scale(map_img, (32, 32))
        else:
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

        # ---- BATTLE IMAGE ----
        if battle_image_path and os.path.exists(battle_image_path):
            battle_img = pygame.image.load(battle_image_path).convert_alpha()
            self.battle_image = pygame.transform.scale(battle_img, (128, 128))
        else:
            self.battle_image = self.image

        self.quiz_question = quiz_question or "No quiz set."
        self.quiz_options = quiz_options or ["A) Placeholder", "B) Placeholder"]
        self.quiz_answer = quiz_answer

        self.path: List[Tuple[int, int]] = []
        self.path_update_interval = 12
        self.frames_since_path_update = 0
        self.use_pathfinding = True

    def update(
        self,
        player_pos: Tuple[int, int],
        level_map: List[List[int]],
        tile_size: int
    ) -> None:
        if self.use_pathfinding:
            self.frames_since_path_update += 1

            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist > self.agro_radius:
                self.path = []
                return

            if self.frames_since_path_update >= self.path_update_interval or not self.path:
                start = (self.rect.centerx, self.rect.centery)
                goal = player_pos
                path = astar(level_map, start, goal, tile_size)
                if path and len(path) > 1:
                    self.path = path[1:]
                else:
                    self.path = []
                self.frames_since_path_update = 0

            if self.path:
                next_tile = self.path[0]
                target_pos = (
                    next_tile[0] * tile_size + tile_size // 2,
                    next_tile[1] * tile_size + tile_size // 2
                )
                dx = target_pos[0] - self.rect.centerx
                dy = target_pos[1] - self.rect.centery
                dist = (dx ** 2 + dy ** 2) ** 0.5

                if dist < 2:
                    self.path.pop(0)
                else:
                    dx = dx / dist if dist != 0 else 0
                    dy = dy / dist if dist != 0 else 0
                    next_rect = self.rect.move(round(dx * self.speed), round(dy * self.speed))
                    tile_x = next_rect.centerx // tile_size
                    tile_y = next_rect.centery // tile_size

                    if 0 <= tile_y < len(level_map) and 0 <= tile_x < len(level_map[0]):
                        if level_map[tile_y][tile_x] in [0, 2] or (tile_x, tile_y) == self.path[0]:
                            self.rect = next_rect
        else:
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist < tile_size * 5 and dist != 0:
                dx = dx / dist
                dy = dy / dist
                next_rect = self.rect.move(round(dx * self.speed), round(dy * self.speed))
                tile_x = next_rect.centerx // tile_size
                tile_y = next_rect.centery // tile_size

                if 0 <= tile_y < len(level_map) and 0 <= tile_x < len(level_map[0]):
                    if level_map[tile_y][tile_x] in [0, 2]:
                        self.rect = next_rect

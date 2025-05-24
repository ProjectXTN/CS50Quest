import pygame
import os
from typing import List, Tuple, Optional, Any
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
        agro_radius: int = 120,
        map_image_path: Optional[str] = None,
        battle_image_path: Optional[str] = None
    ) -> None:
        super().__init__()
        self.name: str = name
        self.max_hp: int = hp
        self.hp: int = hp
        self.damage: int = damage
        self.speed: int = speed
        self.agro_radius: int = agro_radius

        # ---- MAP IMAGE ----
        if map_image_path and os.path.exists(map_image_path):
            map_img = pygame.image.load(map_image_path).convert_alpha()
            self.image: pygame.Surface = pygame.transform.scale(map_img, (32, 32))
        else:
            self.image: pygame.Surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.image.fill(color)
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))

        # ---- BATTLE IMAGE ----
        if battle_image_path and os.path.exists(battle_image_path):
            battle_img = pygame.image.load(battle_image_path).convert_alpha()
            self.battle_image: pygame.Surface = pygame.transform.scale(battle_img, (128, 128))
        else:
            self.battle_image: pygame.Surface = self.image  # fallback to map image

        # Quiz attributes
        self.quiz_question: str = quiz_question or "No quiz set."
        self.quiz_options: List[str] = quiz_options or ["A) Placeholder", "B) Placeholder"]
        self.quiz_answer: int = quiz_answer

        # Pathfinding attributes
        self.path: List[Tuple[int, int]] = []
        self.path_update_interval: int = 12
        self.frames_since_path_update: int = 0
        self.use_pathfinding: bool = True

    def update(
        self,
        player_pos: Tuple[int, int],
        level_map: List[List[int]],
        tile_size: int
    ) -> None:
        """
        Update enemy position. If pathfinding is enabled, use A* to follow the player
        around obstacles. Otherwise, move in a straight line and check for walls.
        """
        if self.use_pathfinding:
            self.frames_since_path_update += 1

            # Calculate Euclidean distance to player
            dx: int = player_pos[0] - self.rect.centerx
            dy: int = player_pos[1] - self.rect.centery
            dist: float = (dx ** 2 + dy ** 2) ** 0.5

            if dist > self.agro_radius:
                # Player is too far, enemy goes idle
                self.path = []
                return

            # Only recalculate path every N frames (optimization)
            if self.frames_since_path_update >= self.path_update_interval or not self.path:
                start: Tuple[int, int] = (self.rect.centerx, self.rect.centery)
                goal: Tuple[int, int] = player_pos
                path: Optional[List[Tuple[int, int]]] = astar(level_map, start, goal, tile_size)
                if path and len(path) > 1:
                    # Remove the first element (current position)
                    self.path = path[1:]
                else:
                    self.path = []
                self.frames_since_path_update = 0

            # Move along the path, if available
            if self.path:
                next_tile: Tuple[int, int] = self.path[0]
                target_pos: Tuple[int, int] = (
                    next_tile[0] * tile_size + tile_size // 2,
                    next_tile[1] * tile_size + tile_size // 2
                )
                dx: int = target_pos[0] - self.rect.centerx
                dy: int = target_pos[1] - self.rect.centery
                dist: float = (dx ** 2 + dy ** 2) ** 0.5

                if dist < 2:
                    # Arrived at this tile, pop and move to next
                    self.path.pop(0)
                else:
                    dx = dx / dist if dist != 0 else 0
                    dy = dy / dist if dist != 0 else 0
                    next_rect: pygame.Rect = self.rect.move(int(dx * self.speed), int(dy * self.speed))
                    tile_x: int = next_rect.centerx // tile_size
                    tile_y: int = next_rect.centery // tile_size

                    # Only move if tile is walkable
                    if 0 <= tile_y < len(level_map) and 0 <= tile_x < len(level_map[0]):
                        if level_map[tile_y][tile_x] == 0:
                            self.rect = next_rect
        else:
            # SIMPLE STRAIGHT-LINE CHASE WITH WALL CHECK
            dx: int = player_pos[0] - self.rect.centerx
            dy: int = player_pos[1] - self.rect.centery
            dist: float = (dx ** 2 + dy ** 2) ** 0.5

            if dist < tile_size * 5 and dist != 0:
                dx = dx / dist
                dy = dy / dist
                next_rect: pygame.Rect = self.rect.move(int(dx * self.speed), int(dy * self.speed))
                tile_x: int = next_rect.centerx // tile_size
                tile_y: int = next_rect.centery // tile_size

                if 0 <= tile_y < len(level_map) and 0 <= tile_x < len(level_map[0]):
                    if level_map[tile_y][tile_x] == 0:
                        self.rect = next_rect

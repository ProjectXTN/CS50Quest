import pygame
import os
from typing import Dict, List, Any
from map import level_map, TILE_SIZE

ANIMATION_DELAY: int = 150  # milliseconds
FRAME_WIDTH: int = 32
FRAME_HEIGHT: int = 32

class AnimatedPlayer(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        speed: int = 2,
        max_hp: int = 200,
        damage: int = 25
    ) -> None:
        super().__init__()
        # Loads the player spritesheet with transparency
        self.spritesheet: pygame.Surface = pygame.image.load("assets/player/spritesheet_nerd_128x128.png").convert_alpha()
        self.max_hp: int = max_hp
        self.hp: int = max_hp
        self.damage: int = damage
        self.speed: int = speed

        self.state: str = "idle"
        self.frame_index: int = 0
        self.last_update: int = pygame.time.get_ticks()
        self.attacking: bool = False
        self.direction: str = "down"

        # 4 frames per row. Adjust as needed for your spritesheet:
        self.animations: Dict[str, List[pygame.Surface]] = {
            "idle": self.load_frames(0, [0]),
            "walk_down": self.load_frames(0, [0, 1, 2, 3]),
            "walk_left": self.load_frames(1, [0, 1]),
            "walk_right": self.load_frames(2, [2, 3]),
            "walk_up": self.load_frames(3, [0, 1, 2, 3]),
        }

        self.image: pygame.Surface = self.animations["idle"][0]
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))
        
        # ---- BATTLE: player battle image ----
        battle_path: str = os.path.join("assets", "player", "player-battle.png")
        battle_raw: pygame.Surface = pygame.image.load(battle_path).convert_alpha()
        self.battle_image: pygame.Surface = pygame.transform.scale(battle_raw, (128, 128))

    def load_frames(self, row: int, cols: List[int]) -> List[pygame.Surface]:
        return [self.get_frame(col, row) for col in cols]

    def get_frame(self, col: int, row: int) -> pygame.Surface:
        frame: pygame.Surface = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT), pygame.SRCALPHA)
        frame.blit(
            self.spritesheet,
            (0, 0),
            (col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
        )
        return frame

    def update(self) -> None:
        self.handle_input()
        self.animate()

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        dx: int = 0
        dy: int = 0

        if not self.attacking:
            if keys[pygame.K_UP]:
                dy = -self.speed
                self.direction = "up"
            elif keys[pygame.K_DOWN]:
                dy = self.speed
                self.direction = "down"
            elif keys[pygame.K_LEFT]:
                dx = -self.speed
                self.direction = "left"
            elif keys[pygame.K_RIGHT]:
                dx = self.speed
                self.direction = "right"

            if dx != 0 or dy != 0:
                new_state: str = f"walk_{self.direction}"
            else:
                new_state: str = "idle"

            if new_state != self.state:
                self.state = new_state
                self.frame_index = 0

            new_rect: pygame.Rect = self.rect.move(dx, dy)
            tile_x: int = new_rect.centerx // TILE_SIZE
            tile_y: int = new_rect.centery // TILE_SIZE

            if 0 <= tile_y < len(level_map) and 0 <= tile_x < len(level_map[0]):
                if level_map[tile_y][tile_x] in (0, 2):
                    self.rect = new_rect

    def animate(self) -> None:
        now: int = pygame.time.get_ticks()
        if self.state.startswith("walk"):
            if now - self.last_update > ANIMATION_DELAY:
                self.last_update = now
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.frame_index]
        else:
            self.frame_index = 0
            self.image = self.animations["idle"][0]

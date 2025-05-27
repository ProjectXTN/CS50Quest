import pygame
import os
from typing import List, Dict
from map.map import level_map, TILE_SIZE

ANIMATION_DELAY = 150  # milliseconds
FRAME_SIZE = (32, 32)

class AnimatedPlayer(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int = 2, max_hp: int = 200, damage: int = 25) -> None:
        super().__init__()
        self.spritesheet = pygame.image.load("assets/player/spritesheet_nerd_128x128.png").convert_alpha()
        self.max_hp = self.hp = max_hp
        self.damage = damage
        self.speed = speed
        self.state = "idle"
        self.direction = "down"
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.attacking = False

        self.animations = self._load_animations()
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Battle mode image
        battle_img = pygame.image.load(os.path.join("assets", "player", "player-battle.png")).convert_alpha()
        self.battle_image = pygame.transform.scale(battle_img, (128, 128))

    def _load_animations(self) -> Dict[str, List[pygame.Surface]]:
        def frames(row, cols): return [self._get_frame(c, row) for c in cols]
        return {
            "idle": frames(0, [0]),
            "walk_down": frames(0, [0, 1, 2, 3]),
            "walk_left": frames(1, [0, 1]),
            "walk_right": frames(2, [2, 3]),
            "walk_up": frames(3, [0, 1, 2, 3]),
        }

    def _get_frame(self, col: int, row: int) -> pygame.Surface:
        frame = pygame.Surface(FRAME_SIZE, pygame.SRCALPHA)
        frame.blit(
            self.spritesheet,
            (0, 0),
            (col * FRAME_SIZE[0], row * FRAME_SIZE[1], *FRAME_SIZE)
        )
        return frame

    def update(self) -> None:
        self._handle_input()
        self._animate()

    def _handle_input(self) -> None:
        if self.attacking:
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_UP]:
            dy, self.direction = -self.speed, "up"
        elif keys[pygame.K_DOWN]:
            dy, self.direction = self.speed, "down"
        elif keys[pygame.K_LEFT]:
            dx, self.direction = -self.speed, "left"
        elif keys[pygame.K_RIGHT]:
            dx, self.direction = self.speed, "right"

        self.state = f"walk_{self.direction}" if dx or dy else "idle"
        if self.state != getattr(self, "prev_state", None):
            self.frame_index = 0
        self.prev_state = self.state

        new_rect = self.rect.move(dx, dy)
        tile_x, tile_y = new_rect.centerx // TILE_SIZE, new_rect.centery // TILE_SIZE
        if 0 <= tile_y < len(level_map) and 0 <= tile_x < len(level_map[0]):
            if level_map[tile_y][tile_x] in (0, 2):
                self.rect = new_rect

    def _animate(self) -> None:
        now = pygame.time.get_ticks()
        anim = self.animations[self.state]
        if self.state.startswith("walk"):
            if now - self.last_update > ANIMATION_DELAY:
                self.last_update = now
                self.frame_index = (self.frame_index + 1) % len(anim)
            self.image = anim[self.frame_index]
        else:
            self.frame_index = 0
            self.image = anim[0]

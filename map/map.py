import pygame
from typing import List, Dict

TILE_SIZE: int = 32

# 0 = grass, 1 = wall, 2 = reward
# Fill 18 rows x 25 columns to match 800x600 window size
level_map: List[List[int]] = [
    [1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1],  # Top wall
    [1,0,0,0,0,0,1,0,0,0, 0,0,0,1,0, 0,0,0,1,0, 0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1, 1,1,0,1,0, 1,1,0,1,0, 1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0, 0,1,0,0,0, 0,1,0,0,0, 0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1, 0,1,1,1,1, 0,1,1,1,1, 0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0, 0,0,0,0,1, 0,0,0,0,1, 0,0,0,0,1],
    [1,1,1,1,1,1,0,1,1,1, 1,1,1,0,1, 1,1,1,1,1, 1,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,0, 0,1,0,0,0, 0,0,0,0,1, 0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1, 0,1,1,1,1, 0,1,1,1,1, 1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0, 0,0,0,0,1, 0,0,0,0,1, 0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1, 1,1,1,0,1, 1,1,1,1,1, 1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0, 0,0,0,0,0, 0,0,0,1,0, 0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1, 0,1,1,1,1, 0,1,1,1,1, 1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0, 0,1,0,0,0, 0,0,0,0,1, 0,0,0,0,1],
    [1,1,1,0,1,1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1, 0,1,1,1,1, 0,1,1,1,1, 0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,1, 0,0,0,2,1],
    [1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1],  # Bottom wall
]

# Load tile images for each tile type
TILE_IMAGES: Dict[int, pygame.Surface] = {
    0: pygame.image.load("assets/tiles/grass.png"),
    1: pygame.image.load("assets/tiles/wall.png"),
    2: pygame.image.load("assets/tiles/box_reward_32x32.png"),
}

def draw_map(screen: pygame.Surface) -> None:
    """
    Draws the map on the given Pygame screen surface.
    """
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x: int = col_index * TILE_SIZE
            y: int = row_index * TILE_SIZE
            image = TILE_IMAGES.get(tile)
            if image:
                screen.blit(image, (x, y))

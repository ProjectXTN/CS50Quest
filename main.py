import os
import pygame
import sys
from typing import Tuple
from config import WIDTH, HEIGHT, FPS, TITLE, BG_COLOR
from map import draw_map, level_map, TILE_SIZE
from player.player import AnimatedPlayer
from monsters.util import find_first_free_tile
from battle import battle_loop
from monsters.segmentationFault import segmentationFault
from monsters.undefinedReference import UndefinedReference
from monsters.memoryLeak import memoryLeak
from monsters.bufferOverFlow import bufferOverFlow
from monsters.stackOverFlowBoss import StackOverflowBoss
from rewards.reward import show_reward_screen

def main() -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock: pygame.time.Clock = pygame.time.Clock()
    draw_map(screen)

    # --- Spawn the player at the first walkable tile ---
    start_x: int
    start_y: int
    start_x, start_y = find_first_free_tile(level_map)
    player_pixel_x: int = start_x * TILE_SIZE
    player_pixel_y: int = start_y * TILE_SIZE
    player: AnimatedPlayer = AnimatedPlayer(player_pixel_x, player_pixel_y)
    all_sprites: pygame.sprite.Group = pygame.sprite.Group()
    all_sprites.add(player)

    running: bool = True

    # --- Create multiple enemies ---
    enemies: pygame.sprite.Group = pygame.sprite.Group()
    enemies.add(
        segmentationFault(3 * TILE_SIZE, 5 * TILE_SIZE),
        UndefinedReference(14 * TILE_SIZE, 3 * TILE_SIZE),
        memoryLeak(5 * TILE_SIZE, 13 * TILE_SIZE),
        bufferOverFlow(16 * TILE_SIZE, 15 * TILE_SIZE),
        StackOverflowBoss(23 * TILE_SIZE, 15 * TILE_SIZE)
    )

    # --- Define the cross-platform reward path ---
    reward_path: str = os.path.join("assets", "reward", "reward.png")

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for enemy in enemies:
            enemy.update(player.rect.center, level_map, TILE_SIZE)
        all_sprites.update()

        screen.fill(BG_COLOR)
        draw_map(screen)
        all_sprites.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()

        # --- Check for collision with any enemy ---
        collided_enemy = pygame.sprite.spritecollideany(player, enemies)
        if collided_enemy:
            print(f"Battle triggered with {collided_enemy.name}!")
            battle_result = battle_loop(screen, player, collided_enemy)
            if battle_result:
                enemies.remove(collided_enemy)
            else:
                print("Game Over")
                running = False

        # --- Check if player is on the reward tile ---
        player_tile_x: int = player.rect.centerx // TILE_SIZE
        player_tile_y: int = player.rect.centery // TILE_SIZE
        if level_map[player_tile_y][player_tile_x] == 2:
            show_reward_screen(
                screen,
                reward_path,
                message="YOU WON!"
            )
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

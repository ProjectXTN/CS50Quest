import os
import pygame
import sys
from typing import Tuple
from config import WIDTH, HEIGHT, FPS, TITLE, BG_COLOR
from map.map import draw_map, level_map, TILE_SIZE
from intro.show_intro_screen import show_intro_screen 
from player.player import AnimatedPlayer
from monsters.util import find_first_free_tile
from battle.battle import battle_loop, show_game_over
from monsters.segmentationFault import segmentationFault
from monsters.undefinedReference import UndefinedReference
from monsters.memoryLeak import memoryLeak
from monsters.bufferOverFlow import bufferOverFlow
from monsters.stackOverFlowBoss import StackOverflowBoss
from rewards.reward import show_reward_screen

def run_game(screen, clock) -> str:
    # --- Spawn the player at the first walkable tile ---
    start_x, start_y = find_first_free_tile(level_map)
    player_pixel_x = start_x * TILE_SIZE
    player_pixel_y = start_y * TILE_SIZE
    player = AnimatedPlayer(player_pixel_x, player_pixel_y)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # --- Create multiple enemies ---
    enemies = pygame.sprite.Group()
    enemies.add(
        segmentationFault(5 * TILE_SIZE, 5 * TILE_SIZE),
        UndefinedReference(14 * TILE_SIZE, 3 * TILE_SIZE),
        memoryLeak(5 * TILE_SIZE, 13 * TILE_SIZE),
        bufferOverFlow(16 * TILE_SIZE, 15 * TILE_SIZE),
        StackOverflowBoss(23 * TILE_SIZE, 15 * TILE_SIZE)
    )

    reward_path = os.path.join("assets", "reward", "reward.png")
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

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
                show_game_over(screen)
                return "game_over"

        # --- Check if player is on the reward tile ---
        player_tile_x = player.rect.centerx // TILE_SIZE
        player_tile_y = player.rect.centery // TILE_SIZE
        if level_map[player_tile_y][player_tile_x] == 2:
            show_reward_screen(
                screen,
                reward_path,
                message="YOU WON!"
            )
            return "victory"

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    intro_path = os.path.join("assets", "intro", "player_intro.png")
    show_intro_screen(screen, intro_path)
    clock = pygame.time.Clock()

    while True:
        result = run_game(screen, clock)
        if result == "quit":
            break
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

import pygame
from typing import Any, Optional
from config import WIDTH, HEIGHT

def get_font(size: int = 24, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("arial", size, bold=bold)

def draw_health_bar(screen, x, y, current_hp, max_hp):
    bar_width, bar_height = 200, 20
    fill = int((current_hp / max_hp) * bar_width)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, fill, bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

def render_stats(screen, player, enemy, player_hp, enemy_hp):
    font_stats = get_font(20)
    enemy_stats = f"HP: {enemy_hp}/{enemy.max_hp}   DMG: {enemy.damage}"
    player_stats = f"HP: {player_hp}/{player.max_hp}   DMG: {player.damage}"
    screen.blit(font_stats.render(enemy_stats, True, (255, 180, 180)), (WIDTH - 250, 80))
    screen.blit(font_stats.render(player_stats, True, (180, 220, 255)), (50, 80))

def get_quiz(enemy, index=None):
    # Boss has lists, normal has strings
    if isinstance(enemy.quiz_question, list):
        idx = index if index is not None else 0
        return (
            enemy.quiz_question[idx],
            enemy.quiz_options[idx],
            enemy.quiz_answer[idx],
        )
    return (enemy.quiz_question, enemy.quiz_options, enemy.quiz_answer)

def render_quiz(screen, question, options, selected, result=None):
    quiz_font = get_font(22, bold=True)
    q_surface = quiz_font.render(question, True, (255, 255, 0))
    screen.blit(q_surface, (WIDTH // 2 - q_surface.get_width() // 2, HEIGHT // 2 - 80))

    option_font = get_font(20)
    for i, opt in enumerate(options):
        opt_surface = option_font.render(opt, True, (220, 255, 220))
        opt_rect = opt_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20 + i * 50))
        if selected == i:
            pygame.draw.rect(screen, (255, 255, 0), opt_rect.inflate(20, 12), 3, border_radius=6)
        screen.blit(opt_surface, opt_rect.topleft)

    if result is not None:
        text = "Correct! You recover HP!" if result else "Wrong! The enemy recovers HP!"
        color = (100, 255, 100) if result else (255, 80, 80)
        res_surface = get_font(26, bold=True).render(text, True, color)
        screen.blit(res_surface, (WIDTH // 2 - res_surface.get_width() // 2, HEIGHT // 2 + 100))

def process_quiz_events(events, selected, opt_len):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit(); exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % opt_len
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % opt_len
            elif event.key == pygame.K_RETURN:
                return selected, True
    return selected, False

def battle_loop(screen: pygame.Surface, player: Any, enemy: Any) -> Optional[bool]:
    clock = pygame.time.Clock()
    running = True
    player_hp, enemy_hp = player.hp, enemy.max_hp
    turn = "player"
    quiz_mode = False
    quiz_result = None
    selected_option = 0
    quiz_80, quiz_30 = False, False
    quiz_idx = None

    while running:
        clock.tick(60)
        screen.fill((30, 30, 30))

        # Draw static elements
        font_big = get_font(36, bold=True)
        screen.blit(font_big.render(enemy.name, True, (255, 200, 100)), (WIDTH // 2 - font_big.size(enemy.name)[0] // 2, 10))
        draw_health_bar(screen, 50, 50, player_hp, player.max_hp)
        draw_health_bar(screen, WIDTH - 250, 50, enemy_hp, enemy.max_hp)
        screen.blit(player.battle_image, (100, HEIGHT // 2))
        screen.blit(enemy.battle_image, (WIDTH - 200, HEIGHT // 2))
        render_stats(screen, player, enemy, player_hp, enemy_hp)

        # === Quiz Logic ===
        hp_percent = enemy_hp / enemy.max_hp
        is_boss = isinstance(enemy.quiz_question, list)

        if is_boss:
            if not quiz_80 and hp_percent <= 0.8:
                quiz_mode, quiz_80, quiz_idx = True, True, 0
                quiz_result, selected_option = None, 0
            if not quiz_30 and hp_percent <= 0.3:
                quiz_mode, quiz_30, quiz_idx = True, True, 1
                quiz_result, selected_option = None, 0
        else:
            if not quiz_30 and hp_percent <= 0.3:
                quiz_mode, quiz_30, quiz_idx = True, True, 0
                quiz_result, selected_option = None, 0

        # === QUIZ MODE ===
        if quiz_mode:
            question, options, correct = get_quiz(enemy, quiz_idx)
            render_quiz(screen, question, options, selected_option, quiz_result)
            pygame.display.flip()

            selected_option, answered = process_quiz_events(pygame.event.get(), selected_option, len(options))
            if quiz_result is None and answered:
                quiz_result = selected_option == correct

            if quiz_result is not None:
                pygame.display.flip()
                pygame.time.delay(1200)
                if quiz_result:
                    player_hp = min(player_hp + int(0.5 * player.max_hp), player.max_hp)
                else:
                    enemy_hp = min(enemy_hp + int(0.5 * enemy.max_hp), enemy.max_hp)
                quiz_mode, quiz_idx = False, None
            continue

        # Draw turn info
        turn_info = f"{turn.capitalize()}'s turn - Press SPACE to attack"
        turn_surface = get_font().render(turn_info, True, (255, 255, 255))
        turn_rect = turn_surface.get_rect(centerx=WIDTH // 2)
        turn_rect.bottom = HEIGHT - 40
        screen.blit(turn_surface, turn_rect)
        pygame.display.flip()

        # Battle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and turn == "player" and not quiz_mode:
                if event.key == pygame.K_SPACE:
                    enemy_hp -= player.damage
                    turn = "enemy"

        if turn == "enemy" and not quiz_mode:
            pygame.time.delay(1000)
            player_hp -= enemy.damage
            turn = "player"

        if enemy_hp <= 0:
            player.hp = player_hp
            return True
        if player_hp <= 0:
            player.hp = 0
            return False
        
def show_game_over(screen):
    font = get_font(48, bold=True)
    msg = font.render("GAME OVER", True, (255, 50, 50))
    msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill((30, 30, 30))
    screen.blit(msg, msg_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

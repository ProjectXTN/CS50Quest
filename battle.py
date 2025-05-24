import pygame
from typing import Any, Optional
from config import WIDTH, HEIGHT

def get_font(size: int = 24, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("arial", size, bold=bold)

def draw_health_bar(
    screen: pygame.Surface,
    x: int,
    y: int,
    current_hp: int,
    max_hp: int
) -> None:
    bar_width: int = 200
    bar_height: int = 20
    fill: int = int((current_hp / max_hp) * bar_width)
    border_rect: pygame.Rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect: pygame.Rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(screen, (255, 0, 0), fill_rect)
    pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

def battle_loop(
    screen: pygame.Surface,
    player: Any,
    enemy: Any
) -> Optional[bool]:
    clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True

    player_hp: int = player.hp
    enemy_hp: int = enemy.max_hp
    turn: str = "player"

    quiz_mode: bool = False
    quiz_result: Optional[bool] = None
    selected_option: int = 0

    quiz_80_triggered: bool = False
    quiz_30_triggered: bool = False
    current_quiz_index: Optional[int] = None

    while running:
        clock.tick(60)
        screen.fill((30, 30, 30))

        # Draw enemy name
        font_big: pygame.font.Font = get_font(36, bold=True)
        enemy_name_surface: pygame.Surface = font_big.render(enemy.name, True, (255, 200, 100))
        screen.blit(enemy_name_surface, (WIDTH // 2 - enemy_name_surface.get_width() // 2, 10))

        # Draw health bars
        draw_health_bar(screen, 50, 50, player_hp, player.max_hp)
        draw_health_bar(screen, WIDTH - 250, 50, enemy_hp, enemy.max_hp)

        # Draw sprites
        screen.blit(player.battle_image, (100, HEIGHT // 2))
        screen.blit(enemy.battle_image, (WIDTH - 200, HEIGHT // 2))

        # Draw stats
        font_stats: pygame.font.Font = get_font(20)
        enemy_stats: str = f"HP: {enemy_hp}/{enemy.max_hp}   DMG: {enemy.damage}"
        player_stats: str = f"HP: {player_hp}/{player.max_hp}   DMG: {player.damage}"
        screen.blit(font_stats.render(enemy_stats, True, (255, 180, 180)), (WIDTH - 250, 80))
        screen.blit(font_stats.render(player_stats, True, (180, 220, 255)), (50, 80))

        # === Quiz logic triggered by HP thresholds ===
        hp_percent: float = enemy_hp / enemy.max_hp

        is_boss: bool = isinstance(enemy.quiz_question, list)

        if is_boss:
            # Boss: quiz at 80% (first) and 30% (second)
            if not quiz_80_triggered and hp_percent <= 0.8:
                quiz_mode = True
                quiz_80_triggered = True
                current_quiz_index = 0
                quiz_result = None
                selected_option = 0

            if not quiz_30_triggered and hp_percent <= 0.3:
                quiz_mode = True
                quiz_30_triggered = True
                current_quiz_index = 1
                quiz_result = None
                selected_option = 0
        else:
            # Normal monster: quiz only at 30%
            if not quiz_30_triggered and hp_percent <= 0.3:
                quiz_mode = True
                quiz_30_triggered = True
                current_quiz_index = 0  # Only one question!
                quiz_result = None
                selected_option = 0

        # === QUIZ MODE ===
        if quiz_mode:
            if is_boss:
                question: str = enemy.quiz_question[current_quiz_index]
                options: list[str] = enemy.quiz_options[current_quiz_index]
                correct: int = enemy.quiz_answer[current_quiz_index]
            else:
                question: str = enemy.quiz_question
                options: list[str] = enemy.quiz_options
                correct: int = enemy.quiz_answer

            quiz_font: pygame.font.Font = get_font(22, bold=True)
            question_surface: pygame.Surface = quiz_font.render(question, True, (255, 255, 0))
            screen.blit(question_surface, (WIDTH // 2 - question_surface.get_width() // 2, HEIGHT // 2 - 80))

            option_font: pygame.font.Font = get_font(20)
            for i, option_text in enumerate(options):
                opt_surface: pygame.Surface = option_font.render(option_text, True, (220, 255, 220))
                opt_rect: pygame.Rect = opt_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20 + i * 50))
                if selected_option == i:
                    pygame.draw.rect(screen, (255, 255, 0), opt_rect.inflate(20, 12), 3, border_radius=6)
                screen.blit(opt_surface, opt_rect.topleft)

            if quiz_result is True:
                result_text: pygame.Surface = get_font(26, bold=True).render("Correct! You recover HP!", True, (100, 255, 100))
                screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 + 100))
            elif quiz_result is False:
                result_text: pygame.Surface = get_font(26, bold=True).render("Wrong! The error restores HP!", True, (255, 80, 80))
                screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 + 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if quiz_result is None and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        quiz_result = (selected_option == correct)

            if quiz_result is not None:
                pygame.display.flip()
                pygame.time.delay(1200)
                if quiz_result:
                    # PLAYER recovers 50% of max HP on correct answer!
                    recovered: int = int(0.5 * player.max_hp)
                    player_hp = min(player_hp + recovered, player.max_hp)
                    quiz_mode = False
                    current_quiz_index = None
                else:
                    recovered: int = int(0.5 * enemy.max_hp)
                    enemy_hp = min(enemy_hp + recovered, enemy.max_hp)
                    quiz_mode = False
                    current_quiz_index = None
                continue

        # Show current turn
        turn_info: str = f"{turn.capitalize()}'s turn - Press SPACE to attack"
        screen.blit(get_font().render(turn_info, True, (255, 255, 255)), (WIDTH // 2 - 100, HEIGHT - 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and turn == "player" and not quiz_mode:
                if event.key == pygame.K_SPACE:
                    enemy_hp -= player.damage
                    turn = "enemy"

        if turn == "enemy" and not quiz_mode:
            pygame.time.delay(1000)
            player_hp -= enemy.damage
            turn = "player"

        # Check end of battle
        if enemy_hp <= 0:
            print("You won the battle!")
            player.hp = player_hp
            return True
        if player_hp <= 0:
            print("You were defeated...")
            player.hp = 0
            return False

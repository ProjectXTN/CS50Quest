import pygame
import sys
from typing import Optional
from pygame.surface import Surface
from pygame.rect import Rect
from config import WIDTH, HEIGHT

def show_reward_screen(
    screen: Surface,
    image_path: str,
    message: Optional[str] = None
) -> None:
    """
    Displays the reward screen (diploma, loot, etc).
    """
    # Load and resize the image to fit nicely in the window
    max_width: int = int(WIDTH * 0.7)
    max_height: int = int(HEIGHT * 0.5)

    reward_img_raw: Surface = pygame.image.load(image_path).convert_alpha()
    img_w: int
    img_h: int
    img_w, img_h = reward_img_raw.get_size()

    # Keep image proportions while scaling down to fit the screen
    scale: float = min(max_width / img_w, max_height / img_h, 1)
    new_w: int = int(img_w * scale)
    new_h: int = int(img_h * scale)
    reward_img: Surface = pygame.transform.smoothscale(reward_img_raw, (new_w, new_h))
    reward_rect: Rect = reward_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

    font: pygame.font.Font = pygame.font.SysFont("arial", 48, bold=True)
    text_color: tuple[int, int, int] = (255, 223, 62)
    bg_color: tuple[int, int, int] = (0, 0, 0)
    clock: pygame.time.Clock = pygame.time.Clock()
    waiting: bool = True

    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Exit reward screen when any key or mouse button is pressed
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        screen.fill(bg_color)
        if message:
            text: Surface = font.render(message, True, text_color)
            # Center the message ABOVE the image
            text_rect: Rect = text.get_rect(center=(WIDTH // 2, reward_rect.top - 50))
            screen.blit(text, text_rect)
        screen.blit(reward_img, reward_rect)
        pygame.display.flip()

import pygame
import sys
from pygame.surface import Surface
from config import WIDTH, HEIGHT


def show_intro_screen(screen: Surface, image_path: str, duration: int = 2000) -> None:
    """
    Displays a full-screen intro image for a set duration or until the user presses a key or mouse button.

    Args:
        screen (Surface): The main Pygame screen surface.
        image_path (str): Path to the intro image to display.
        duration (int): Duration in milliseconds before auto-skipping (default is 3000ms).
    """
    # Load and scale the image to fit the screen
    image: Surface = pygame.image.load(image_path).convert()
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    # Display the image on the screen
    screen.blit(image, (0, 0))
    pygame.display.flip()

    clock: pygame.time.Clock = pygame.time.Clock()
    start_time: int = pygame.time.get_ticks()

    # Main loop to wait for user input or timeout
    while True:
        elapsed: int = pygame.time.get_ticks() - start_time

        # Handle events (exit or skip)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                return  # Exit intro screen on any key or mouse press

        # Auto-exit after duration
        if elapsed >= duration:
            return

        clock.tick(60)  # Limit to 60 FPS

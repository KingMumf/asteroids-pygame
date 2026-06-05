import pygame
from logger import log_event

class Score():
    def __init__(self) -> None:
        self.score = 0
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)

    def add_points(self, points: int) -> None:
        self.score += points
        log_event(f"Added {points} points. Total score: {self.score}")

    def reset(self) -> None:
        self.score = 0
        log_event("Score reset to 0.")

    def draw(self, screen: pygame.Surface) -> None:
        score_text = self.font.render(f"Score: {self.score}", True, "white")
        text_surface = self.font.render(f"Score: {self.score}", True, "white")

        position = (10, 10)

        screen.blit(text_surface, position)
import pygame
import math
from shot import Shot

class Weapon:
    def __init__(self, cooldown: float) -> None:
        self.cooldown_time = cooldown
    
    def fire(self, position: pygame.Vector2, rotation: float) -> None:
        pass

class StandardBlaster(Weapon):
    def __init__(self) -> None:
        super().__init__(cooldown=0.3)

    def fire(self, position: pygame.Vector2, rotation: float) -> None:

        bullet_speed = 500
        direction = pygame.Vector2(0, 1).rotate(rotation)

        shot = Shot(position.x, position.y)
        shot.velocity = direction * bullet_speed


class SpreadShot(Weapon):
    def __init__(self) -> None:
        super().__init__(cooldown=0.5)

    def fire(self, position: pygame.Vector2, rotation: float) -> None:
        bullet_speed = 450
        spread_angle = [-15, 0, 15]

        for angle_offset in spread_angle:
            direction = pygame.Vector2(0, 1).rotate(rotation + angle_offset)
            shot = Shot(position.x, position.y)
            shot.velocity = direction * bullet_speed


class RapidFire(Weapon):
    def __init__(self) -> None:
        super().__init__(cooldown=0.1)

    def fire(self, position: pygame.Vector2, rotation: float) -> None:
        bullet_speed = 600
        direction = pygame.Vector2(0, 1).rotate(rotation)

        shot = Shot(position.x, position.y)
        shot.velocity = direction * bullet_speed


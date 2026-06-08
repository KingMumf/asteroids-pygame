import random
import pygame
import math
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        self.points = []
        num_points = random.randint(8, 12)

        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            min_dist = radius * 0.75
            max_dist = radius * 1.15
            distance = random.uniform(min_dist, max_dist)
            point_x = math.cos(angle) * distance
            point_y = math.sin(angle) * distance
            self.points.append(pygame.Vector2(point_x, point_y))

    def draw(self, screen: pygame.Surface) -> None:
        screen_points = []

        for point in self.points:
            absolute_point = self.position + point
            screen_points.append(absolute_point)
            
        pygame.draw.polygon(screen, "white", screen_points, width=LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 

        log_event("asteroid_split")

        random_angle = random.uniform(20, 50)
        new_radius = self.radius / 2
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = self.velocity.rotate(random_angle) * 1.2
        asteroid2.velocity = self.velocity.rotate(-random_angle) * 1.2
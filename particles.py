import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, velocity: pygame.Vector2) -> None:
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.lifetime = random.uniform(0.3, 0.8)  # lifetime of particles
        self.color = random.choice(["white", "lightgray", "gray"])  # random color for particles
        self.radius = random.randint(1, 3) 

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.lifetime -= dt
        
    def draw(self, screen: pygame.Surface) -> None:
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, self.position, self.radius)

    
class ExplosionManager:
    def __init__(self) -> None:
        self.particles = []

    def create_explosion(self, x: float, y: float, count: int = 20) -> None:
        for _ in range(count):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 150)
            velocity = pygame.Vector2(1, 0).rotate(angle) * speed
            
            self.particles.append(Particle(x, y, velocity))

    def update(self, dt: float) -> None:
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, screen: pygame.Surface) -> None:
        for particle in self.particles:
            particle.draw(screen)
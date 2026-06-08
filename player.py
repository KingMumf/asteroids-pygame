import pygame
import math
from constants import (
    PLAYER_RADIUS, 
    LINE_WIDTH, 
    PLAYER_TURN_SPEED, 
    PLAYER_ACCELERATION, 
    PLAYER_MAX_SPEED, 
    PLAYER_FRICTION, 
    PLAYER_SHOOT_SPEED, 
    PLAYER_SHOOT_COOLDOWN_SECONDS, 
    SCREEN_WIDTH, 
    SCREEN_HEIGHT
)
from circleshape import CircleShape
from shot import Shot
from weapons import (
    StandardBlaster,
    SpreadShot,
    RapidFire
)

class Player(CircleShape):
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.lives = 3
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.current_weapon = StandardBlaster()
        self.shoot_cooldown = 0.0


# in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), width=LINE_WIDTH)

        if self.invulnerable and int(pygame.time.get_ticks() / 200) % 2 == 0:
            return

    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    
    def update(self, dt: float) -> None:
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
            if self.shoot_cooldown < 0:
                self.shoot_cooldown = 0

        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity *= (1 - (PLAYER_FRICTION * 8) * dt)
        else:
            self.velocity *= (1 - PLAYER_FRICTION * dt)

        if keys[pygame.K_SPACE]:
            if self.shoot_cooldown <= 0:
                self.shoot_cooldown = self.current_weapon.cooldown_time
                self.shoot()

        if keys[pygame.K_1]:
            self.current_weapon = StandardBlaster()
        if keys[pygame.K_2]:
            self.current_weapon = SpreadShot()
        if keys[pygame.K_3]:
            self.current_weapon = RapidFire()


        if self.velocity.length_squared() > 0 and self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

        self.position += self.velocity * dt

        self.wrap_around(SCREEN_WIDTH, SCREEN_HEIGHT)

    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    
    def shoot(self):
        self.current_weapon.fire(self.position, self.rotation)

    def respawn(self) -> None:
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.invulnerable = True
        self.invulnerable_timer = 2.0
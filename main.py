import sys
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from shot import Shot
from scoring import Score
from particles import ExplosionManager

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    scoreboard = Score()
    explosion_manager = ExplosionManager()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)

    stars = []
    for _ in range(100):
        star_x = random.randint(0, SCREEN_WIDTH)
        star_y = random.randint(0, SCREEN_HEIGHT)
        star_size = random.choice([1, 2])
        brightness = random.randint(120, 255)
        stars.append((star_x, star_y, star_size, brightness))


    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((5, 5, 12))

        for x, y, size, brightness in stars:
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)

        for sprite in drawable:
            sprite.draw(screen)

        explosion_manager.draw(screen)
        scoreboard.draw(screen, player.lives)

        updatable.update(dt)
        explosion_manager.update(dt)

        for shot in shots:
            for asteroid in asteroids:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    explosion_manager.create_explosion(asteroid.position.x, asteroid.position.y)
                    shot.kill()
                    scoreboard.add_points(10)
                    asteroid.split()

        if not player.invulnerable:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    player.lives -= 1
                    scoreboard.draw(screen, player.lives)
                    log_event(f"player_hit Lives remaining: {player.lives}")

                    explosion_manager.create_explosion(player.position.x, player.position.y)

                    if player.lives > 0:
                        player.respawn()
                        break
                    else:
                        log_event("Game Over!")
                        print("Game Over!")
                        print(f"final score: {scoreboard.score}")
                        sys.exit()

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()

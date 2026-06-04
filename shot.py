class Shot(CircleShape):
    def __init__(self, position: Vector2, velocity: Vector2):
        super().__init__(position, SHOT_RADIUS)
        self.velocity = velocity

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", self.position, self.radius)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    
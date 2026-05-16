import random
import pygame


class Ball:
    def __init__(
        self,
        x: int,
        y: int,
        size: int = 16,
        speed_x: int = 6,
        speed_y: int = 6,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color

    def move(self) -> None:
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_y(self) -> None:
        self.speed_y *= -1

    def bounce_x(self) -> None:
        self.speed_x *= -1

    def reset(self, screen_width: int, screen_height: int) -> None:
        self.rect.center = (screen_width // 2, screen_height // 2)

        self.speed_x = random.choice([-6, 6])
        self.speed_y = random.choice([-6, 6])

    def keep_inside_screen(self, screen_height: int) -> None:
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.bounce_y()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.ellipse(screen, self.color, self.rect)
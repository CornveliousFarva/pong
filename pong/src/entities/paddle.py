import pygame


class Paddle:
    def __init__(
        self,
        x: int,
        y: int,
        width: int = 14,
        height: int = 90,
        speed: int = 7,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.color = color

    def move_up(self) -> None:
        self.rect.y -= self.speed

    def move_down(self) -> None:
        self.rect.y += self.speed

    def keep_inside_screen(self, screen_height: int) -> None:
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
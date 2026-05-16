import pygame

from src.entities.ball import Ball
from src.entities.paddle import Paddle
from src.levels import LEVELS


class Game:
    def __init__(self) -> None:
        self.screen_width = 900
        self.screen_height = 600
        self.game_mode = "human_vs_cpu"
        self.fps = 60

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Grand Slam Pong")

        self.clock = pygame.time.Clock()
        self.running = True

        self.current_level_name = "Australian Open"
        self.current_level = LEVELS[self.current_level_name]

        self.bg_color = self.current_level["court_color"]
        self.line_color = self.current_level["line_color"]

        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.SysFont("Arial", 48)

        self.left_paddle = Paddle(
            x=30,
            y=self.screen_height // 2 - 45,
            color=(255, 255, 255),
        )

        self.right_paddle = Paddle(
            x=self.screen_width - 44,
            y=self.screen_height // 2 - 45,
            speed=5,
            color=(255, 255, 255),
        )

        self.ball = Ball(
            x=self.screen_width // 2 - 8,
            y=self.screen_height // 2 - 8,
            color=(255, 230, 0),
        )

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.left_paddle.move_up()

        if keys[pygame.K_s]:
            self.left_paddle.move_down()

        if self.game_mode == "human_vs_human":
            if keys[pygame.K_UP]:
                self.right_paddle.move_up()

            if keys[pygame.K_DOWN]:
                self.right_paddle.move_down()

        elif self.game_mode == "human_vs_cpu":
            self.move_cpu_paddle()

        self.left_paddle.keep_inside_screen(self.screen_height)
        self.right_paddle.keep_inside_screen(self.screen_height)

        self.ball.move()
        self.ball.keep_inside_screen(self.screen_height)

        self.handle_collisions()
        self.handle_scoring()

    def move_cpu_paddle(self) -> None:
        cpu_center = self.right_paddle.rect.centery
        ball_center = self.ball.rect.centery

        if ball_center < cpu_center:
            self.right_paddle.move_up()

        elif ball_center > cpu_center:
            self.right_paddle.move_down()

    def handle_collisions(self) -> None:
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.rect.left = self.left_paddle.rect.right
            self.ball.bounce_x()

        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.rect.right = self.right_paddle.rect.left
            self.ball.bounce_x()

    def handle_scoring(self) -> None:
        if self.ball.rect.right < 0:
            self.right_score += 1
            self.ball.reset(self.screen_width, self.screen_height)

        if self.ball.rect.left > self.screen_width:
            self.left_score += 1
            self.ball.reset(self.screen_width, self.screen_height)

    def draw_center_line(self) -> None:
        for y in range(0, self.screen_height, 30):
            pygame.draw.rect(
                self.screen,
                self.line_color,
                pygame.Rect(self.screen_width // 2 - 2, y, 4, 18),
            )

    def draw_score(self) -> None:
        left_text = self.font.render(str(self.left_score), True, self.line_color)
        right_text = self.font.render(str(self.right_score), True, self.line_color)

        self.screen.blit(left_text, (self.screen_width // 2 - 90, 30))
        self.screen.blit(right_text, (self.screen_width // 2 + 60, 30))

    def draw(self) -> None:
        self.screen.fill(self.bg_color)

        self.draw_center_line()
        self.draw_score()

        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        pygame.display.flip()
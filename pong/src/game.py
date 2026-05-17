import pygame

from src.entities.ball import Ball
from src.entities.paddle import Paddle
from src.levels import LEVELS
from src.settings import PADDLE_COLORS, BALL_COLORS


class Game:
    def __init__(self) -> None:
        self.game_over = False
        self.winner = ""
        self.winning_score = 11
        self.screen_width = 900
        self.screen_height = 600
        self.game_mode = "human_vs_cpu"
        self.fps = 60
        self.paddle_color_index = 0
        self.ball_color_index = 0
        self.winning_score = 11
       

        self.left_paddle = Paddle(
            x=30,
            y=self.screen_height // 2 - 45,
        )

        self.right_paddle = Paddle(
            x=self.screen_width - 44,
            y=self.screen_height // 2 - 45,
        )

        self.ball = Ball(
            x=self.screen_width // 2 - 8,
            y=self.screen_height // 2 - 8,
        )

# NOW these objects exist
        self.left_paddle.color = PADDLE_COLORS[self.paddle_color_index]
        self.right_paddle.color = PADDLE_COLORS[self.paddle_color_index]

        self.ball.color = BALL_COLORS[self.ball_color_index]

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Grand Slam Pong")

        self.clock = pygame.time.Clock()
        self.running = True

        self.current_level_name = "Classic Pong"
        self.current_level = LEVELS[self.current_level_name]


        self.bg_color = self.current_level["court_color"]
        self.line_color = self.current_level["line_color"]

        self.left_score = 0
        self.right_score = 0
        self.font = pygame.font.SysFont("Arial", 48)
        

    def load_level(self, level_name: str) -> None:
        if level_name in LEVELS:
            self.current_level_name = level_name
            self.current_level = LEVELS[level_name]

            self.bg_color = self.current_level["court_color"]
            self.line_color = self.current_level["line_color"]

            self.right_paddle.speed = self.current_level["cpu_speed"]
            self.ball.speed_x = self.current_level["ball_speed"]
            self.ball.speed_y = self.current_level["ball_speed"]

            self.left_score = 0
            self.right_score = 0
            self.ball.reset(self.screen_width, self.screen_height)

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
    
    def next_paddle_color(self) -> None:
        self.paddle_color_index = (self.paddle_color_index + 1) % len(PADDLE_COLORS)
        new_color = PADDLE_COLORS[self.paddle_color_index]
        self.left_paddle.color = new_color
        self.right_paddle.color = new_color

    def previous_paddle_color(self) -> None:
        self.paddle_color_index = (self.paddle_color_index - 1) % len(PADDLE_COLORS)
        new_color = PADDLE_COLORS[self.paddle_color_index]
        self.left_paddle.color = new_color
        self.right_paddle.color = new_color

    def next_ball_color(self) -> None:
        self.ball_color_index = (self.ball_color_index + 1) % len(BALL_COLORS)
        self.ball.color = BALL_COLORS[self.ball_color_index]

    def previous_ball_color(self) -> None:
        self.ball_color_index = (self.ball_color_index - 1) % len(BALL_COLORS)
        self.ball.color = BALL_COLORS[self.ball_color_index]        

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.load_level("Classic Pong")
                elif event.key == pygame.K_2:
                    self.load_level("Australian Open")
                elif event.key == pygame.K_3:
                    self.load_level("French Open")
                elif event.key == pygame.K_4:
                    self.load_level("Wimbledon")
                elif event.key == pygame.K_5:
                    self.load_level("US Open")
                elif event.key == pygame.K_q:
                    self.previous_paddle_color()
                elif event.key == pygame.K_e:
                    self.next_paddle_color()
                elif event.key == pygame.K_z:
                    self.previous_ball_color()
                elif event.key == pygame.K_x:
                    self.next_ball_color()
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()

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
        if self.game_over:
            return

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

        if self.left_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player 1"

        elif self.right_score >= self.winning_score:
            if self.game_mode == "human_vs_human":
                self.winner = "Player 2"
            else:
                self.winner = "CPU"

            self.game_over = True

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

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()
    
    def draw_game_over(self) -> None:
        if self.game_over:
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("Game Over", True, (255, 255, 255))
            winner_text = self.font.render(f"{self.winner} Wins!", True, (255, 255, 255))

            self.screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, self.screen_height // 2 - 60))
            self.screen.blit(winner_text, (self.screen_width // 2 - winner_text.get_width() // 2, self.screen_height // 2 + 10))
            restart_text = pygame.font.SysFont("Arial", 28).render(
                "Press SPACE to restart",
                True,
                (255, 255, 255),
            )

            self.screen.blit(
                restart_text,
                (
                    self.screen_width // 2 - restart_text.get_width() // 2,
                    self.screen_height // 2 + 80,
                ),
            )

    def reset_game(self) -> None:
        self.left_score = 0
        self.right_score = 0

        self.game_over = False
        self.winner = ""

        self.ball.reset(self.screen_width,self.screen_height)

        self.left_paddle.rect.centery = self.screen_height // 2
        self.right_paddle.rect.centery = self.screen_height // 2

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
        self.screen_state = "menu"
        self.title_font = pygame.font.SysFont("Arial", 64)
        self.menu_font = pygame.font.SysFont("Arial", 32)
        
    def draw_menu(self) -> None:
        self.screen.fill((0, 0, 0))

        title_text = self.title_font.render(
            "Grand Slam Pong",
            True,
            (255, 255, 255),
        )

        option_1 = self.menu_font.render(
            "1 - Play vs CPU",
            True,
            (255, 255, 255),
        )

        option_2 = self.menu_font.render(
            "2 - Play vs Player",
            True,
            (255, 255, 255),
        )

        option_3 = self.menu_font.render(
            "ESC - Quit",
            True,
            (255, 255, 255),
        )
        # Added a new title for the main menu, "Grand Slam Pong", which is rendered using a larger font and blitted onto the screen at the top center. This title provides a clear and visually appealing introduction to the game when players first launch it, setting the tone for the tennis-themed Pong experience.
        self.screen.blit(
            title_text,
            (
                self.screen_width // 2 - title_text.get_width() // 2,
                160,
            ),
        )
        # 
        self.screen.blit(
            option_1,
            (
                self.screen_width // 2 - option_1.get_width() // 2,
                280,
            ),
        )
        # Added a new menu option for human vs human mode, allowing players to choose between playing against the CPU or competing against another player on the same machine. This option is rendered as text and blitted onto the screen below the "Play vs CPU" option, providing a clear choice for players who want to play with a friend instead of against the computer.
        self.screen.blit(
            option_2,
            (
                self.screen_width // 2 - option_2.get_width() // 2,
                330,
            ),
        )
        # Added a new menu option for quitting the game, allowing players to easily exit the game from the main menu by pressing the "ESC" key. This option is rendered as text and blitted onto the screen below the other menu options, providing a clear and accessible way for players to quit the game if they choose not to play.
        self.screen.blit(
            option_3,
            (
                self.screen_width // 2 - option_3.get_width() // 2,
                400,
            ),
        )

    # This method is responsible for loading a specific level based on the provided level name. It checks if the level name exists in the LEVELS dictionary, and if it does, it updates the current level settings such as background color, line color, ball speed, and CPU paddle speed according to the selected level. It also resets the scores and positions of the ball and paddles to start fresh with the new level settings.
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
    # This method is responsible for running the main game loop. It continuously checks for events, updates the game state, and redraws the screen at a consistent frame rate defined by self.fps. The loop continues until the self.running flag is set to False, which typically happens when the player chooses to quit the game.
    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
    # This method is responsible for changing the paddle's color to the next color in the PADDLE_COLORS list. It increments the paddle_color_index and uses modulo to wrap around if it exceeds the length of the PADDLE_COLORS list, ensuring that the index stays within the valid range of colors. After updating the index, it sets the paddles' color to the new color from the PADDLE_COLORS list based on the updated index.
    def next_paddle_color(self) -> None:
        self.paddle_color_index = (self.paddle_color_index + 1) % len(PADDLE_COLORS)
        new_color = PADDLE_COLORS[self.paddle_color_index]
        self.left_paddle.color = new_color
        self.right_paddle.color = new_color
    # This method is responsible for changing the paddle's color to the previous color in the PADDLE_COLORS list. It decrements the paddle_color_index and uses modulo to wrap around if it goes below zero, ensuring that the index stays within the valid range of colors. After updating the index, it sets the paddles' color to the new color from the PADDLE_COLORS list based on the updated index.
    def previous_paddle_color(self) -> None:
        self.paddle_color_index = (self.paddle_color_index - 1) % len(PADDLE_COLORS)
        new_color = PADDLE_COLORS[self.paddle_color_index]
        self.left_paddle.color = new_color
        self.right_paddle.color = new_color
    # This method is responsible for changing the ball's color to the next color in the BALL_COLORS list. It increments the ball_color_index and uses modulo to wrap around if it exceeds the length of the BALL_COLORS list, ensuring that the index stays within the valid range of colors. After updating the index, it sets the ball's color to the new color from the BALL_COLORS list based on the updated index.
    def next_ball_color(self) -> None:
        self.ball_color_index = (self.ball_color_index + 1) % len(BALL_COLORS)
        self.ball.color = BALL_COLORS[self.ball_color_index]

    # This method is responsible for changing the ball's color to the previous color in the BALL_COLORS list. It decrements the ball_color_index and uses modulo to wrap around if it goes below zero, ensuring that the index stays within the valid range of colors. After updating the index, it sets the ball's color to the new color from the BALL_COLORS list based on the updated index.
    def previous_ball_color(self) -> None:
        self.ball_color_index = (self.ball_color_index - 1) % len(BALL_COLORS)
        self.ball.color = BALL_COLORS[self.ball_color_index]        

# This method is responsible for handling all the events that occur during the game, such as quitting the game, navigating the menu, selecting game modes, switching levels, and changing colors. It listens for specific key presses to trigger these actions, allowing players to interact with the game and customize their experience. For example, pressing "1" or "2" in the menu starts a new game in either human vs CPU or human vs human mode, while pressing "M" during gameplay returns to the menu. Additionally, players can switch between different levels and customize paddle and ball colors using designated keys.
    def handle_events(self) -> None:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
# 
            elif event.type == pygame.KEYDOWN:
                # Handle menu navigation and game mode selection
                if self.screen_state == "menu":
                    if event.key == pygame.K_1:
                        self.game_mode = "human_vs_cpu"
                        self.screen_state = "playing"
                        self.reset_game()
                    # Added option for human vs human mode in the menu, allowing two players to compete against each other on the same machine. This is triggered by pressing the "2" key, which sets the game mode to "human_vs_human", changes the screen state to "playing", and resets the game to start fresh.
                    elif event.key == pygame.K_2:
                        self.game_mode = "human_vs_human"
                        self.screen_state = "playing"
                        self.reset_game()
                    # 
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                # Allow returning to menu or restarting game on space if game over
                elif self.screen_state == "playing":

                    # Return to menu
                    if event.key == pygame.K_m:
                        self.screen_state = "menu"

                    # Restart after game over
                    elif event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()

                    # Level switching
                    elif event.key == pygame.K_1:
                        self.load_level("Classic Pong")

                    elif event.key == pygame.K_2:
                        self.load_level("Australian Open")

                    elif event.key == pygame.K_3:
                        self.load_level("French Open")

                    elif event.key == pygame.K_4:
                        self.load_level("Wimbledon")

                    elif event.key == pygame.K_5:
                        self.load_level("US Open")

                    # Paddle colors
                    elif event.key == pygame.K_q:
                        self.previous_paddle_color()

                    elif event.key == pygame.K_e:
                        self.next_paddle_color()

                    # Ball colors
                    elif event.key == pygame.K_z:
                        self.previous_ball_color()

                    elif event.key == pygame.K_x:
                        self.next_ball_color()

                    elif event.key == pygame.K_ESCAPE:
                        self.screen_state = "menu"

                    elif event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()

                    elif event.key == pygame.K_p:
                        self.screen_state = "pause"
                    
# This method is responsible for updating the game state each frame. It handles player input, moves the paddles and ball, checks for collisions, and updates the score. It also checks for game over conditions and determines the winner when the game ends.
    def update(self) -> None:
        if self.screen_state == "menu":
            return

        if self.game_over:
            return

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
        
# This method is responsible for moving the CPU-controlled paddle. It compares the vertical center of the ball with the vertical center of the CPU paddle and moves the paddle up or down accordingly to try to keep it aligned with the ball's position. This simple AI allows the CPU to effectively track and respond to the ball's movement during gameplay.
    def move_cpu_paddle(self) -> None:
        cpu_center = self.right_paddle.rect.centery
        ball_center = self.ball.rect.centery

        if ball_center < cpu_center:
            self.right_paddle.move_up()

        elif ball_center > cpu_center:
            self.right_paddle.move_down()

#  This method is responsible for handling collisions between the ball and the paddles. It checks if the ball's rectangle collides with either the left or right paddle's rectangle. If a collision is detected, it adjusts the ball's position to prevent it from getting stuck inside the paddle and calls the bounce_x() method to reverse the ball's horizontal direction, simulating a bounce off the paddle.
    def handle_collisions(self) -> None:
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.rect.left = self.left_paddle.rect.right
            self.ball.bounce_x()

        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.rect.right = self.right_paddle.rect.left
            self.ball.bounce_x()

# 
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

#  This method is responsible for drawing the game elements on the screen each frame. It first checks the current screen state; if it's in the menu, it calls the draw_menu() method to render the menu and then updates the display. If the game is in the playing state, it fills the background with the court color, draws the center line, and renders the current score. It then calls the draw() method on both paddles and the ball to render them on the screen. If the game is over, it calls draw_game_over() to display the game over screen with the winner and restart instructions. Finally, it updates the display to show all the drawn elements.
    def draw_center_line(self) -> None:
        for y in range(0, self.screen_height, 30):
            pygame.draw.rect(
                self.screen,
                self.line_color,
                pygame.Rect(self.screen_width // 2 - 2, y, 4, 18),
            )
# This method is responsible for drawing the current score of both players on the screen. It uses the font object to render the left and right scores as text surfaces, which are then blitted onto the screen at specific positions near the top center. The left player's score is displayed to the left of the center line, while the right player's score is displayed to the right of the center line, allowing players to easily see their current scores during gameplay.
    def draw_score(self) -> None:
        left_text = self.font.render(str(self.left_score), True, self.line_color)
        right_text = self.font.render(str(self.right_score), True, self.line_color)

        self.screen.blit(left_text, (self.screen_width // 2 - 90, 30))
        self.screen.blit(right_text, (self.screen_width // 2 + 60, 30))

# This method is responsible for drawing the game over screen when the game has ended. It creates a semi-transparent black overlay to dim the background and then renders the "Game Over" text along with the winner's name. It also displays instructions for restarting the game by pressing the spacebar. The text is centered on the screen to ensure it is prominently displayed to the player when the game ends.
    def draw(self) -> None:
        if self.screen_state == "menu":
            self.draw_menu()
            pygame.display.flip()
            return

        self.screen.fill(self.bg_color)
        self.draw_center_line()
        self.draw_score()

        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    # This method is responsible for drawing the game over screen when the game has ended. It creates a semi-transparent black overlay to dim the background and then renders the "Game Over" text along with the winner's name. It also displays instructions for restarting the game by pressing the spacebar. The text is centered on the screen to ensure it is prominently displayed to the player when the game ends.
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
# This method is responsible for resetting the game state when the game is over. It initializes the scores to zero, sets the game over flag to False, and resets the ball and paddles to their starting positions.
    def reset_game(self) -> None:
        self.left_score = 0
        self.right_score = 0

        self.game_over = False
        self.winner = ""

        self.ball.reset(self.screen_width,self.screen_height)

        self.left_paddle.rect.centery = self.screen_height // 2
        self.right_paddle.rect.centery = self.screen_height // 2

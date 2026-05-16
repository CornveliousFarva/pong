import pygame
from game import Game
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()
        screen.fill((0, 0, 0))
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
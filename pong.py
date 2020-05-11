import pygame, sys

# General Setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window

screen_width = 1280
screen_height = 960

screen = pygame.display.set_mode((screen_width, screen_width))
pygame.display.set_caption('Pong')

while True:
    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Updating the Windows
    pygame.display.flip()
    clock.tick(60)

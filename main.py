# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

positions = [
    (125, 300),
    (300, 125),
    (475, 300),
    (300, 475)
]

pos = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pos += 1
                if pos > len(positions) - 1:
                    pos = 0
                    
    # every 1 seconds
    if pygame.time.get_ticks() % (60 * 1) == 0:
        pos += 1
        if pos > len(positions) - 1:
            pos = 0

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#FFD166")

    pos_circle = positions[pos]

    pygame.draw.circle(screen, "#FB6286", (300, 300), 200)
    pygame.draw.circle(screen, "#FFD166", (300, 300), 150)
    pygame.draw.circle(screen, "#073B4C", pos_circle, 25)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

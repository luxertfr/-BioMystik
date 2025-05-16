# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

frames = []
# for i in range(2):
#     img = pygame.image.load(f"./assets/sprites/walk_{i}.png")
#     scaled_img = pygame.transform.scale(img, (128, 128))
#     frames.append(scaled_img)
frames = [pygame.image.load(f"./assets/sprites/walk_{i}.png").convert_alpha() for i in range(2)]


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill("purple")
        # Dans la boucle du jeu :
    current_frame = (pygame.time.get_ticks() // 300) % len(frames)
    screen.blit(frames[current_frame], (player_pos.x, player_pos.y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_q]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
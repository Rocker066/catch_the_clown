import random
import pygame

# Initialize pygame
pygame.init()

# Set display surface
WIDTH = 945
HEIGHT = 600
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Catch2')

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 4
CLOWN_ACCELERATION = 1

score = 0
player_lives = PLAYER_STARTING_LIVES

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# Set colors
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)
BLACK = (255, 255, 255)

# Set font
font = pygame.font.Font('assets/Franxurter.ttf', 32)

# Set text
title_text = font.render('Catch the Clown', True, BLUE)
title_text_rect = title_text.get_rect()
title_text_rect.topleft = (50, 10)

score_text = font.render('Score: ' + str(score), True, YELLOW)
score_text_rect = score_text.get_rect()
score_text_rect.topright = (WIDTH - 50, 10)

lives_text = font.render('Lives: ' + str(player_lives), True, YELLOW)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (WIDTH - 50, 50)

game_over_text = font.render('GAMEOVER', True, BLUE, YELLOW)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WIDTH // 2, HEIGHT // 2)

continue_text = font.render('Click anywhere to play again', True, YELLOW, BLUE)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (WIDTH // 2, HEIGHT // 2 + 64)

paused_text = font.render('PAUSED', True, YELLOW, BLUE)
paused_text_rect = paused_text.get_rect()
paused_text_rect.center = (WIDTH // 2, HEIGHT // 2)

# Set sound and music
click_sound = pygame.mixer.Sound('assets/click_sound.wav')
click_sound.set_volume(.01)
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
miss_sound.set_volume(.01)
pygame.mixer.music.load('assets/ctc_background_music.wav')
pygame.mixer.music.set_volume(.1)

# Set images
background_image = pygame.image.load('assets/background.png')
background_image_rect = background_image.get_rect()
background_image_rect.topleft = (0, 0)

clown_image = pygame.image.load('assets/clown.png')
clown_image_rect = clown_image.get_rect()
clown_image_rect.center = (WIDTH // 2, HEIGHT // 2)

# Main game loop
pygame.mixer.music.play()
running = True
is_paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Toggle pause with Escape key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused = not is_paused

        # A mouse click is made while not paused
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_paused:
            pos_x, pos_y = event.pos

            # The clown was clicked
            if clown_image_rect.collidepoint(pos_x, pos_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                # Move the clown in a new direction
                previous_dx, previous_dy = clown_dx, clown_dy

                while previous_dx == clown_dx and previous_dy == clown_dy:
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

            else:
                miss_sound.play()
                player_lives -= 1

    if not is_paused:
        # Move the clown
        clown_image_rect.x += clown_velocity * clown_dx
        clown_image_rect.y += clown_velocity * clown_dy

        # Bounce the clown off the edges of the screen
        if clown_image_rect.right >= WIDTH or clown_image_rect.left <= 0:
            clown_dx *= -1
        if clown_image_rect.top <= 0 or clown_image_rect.bottom >= HEIGHT:
            clown_dy *= -1

        # Update the HUD
        score_text = font.render('Score: ' + str(score), True, YELLOW)
        lives_text = font.render('Lives: ' + str(player_lives), True, YELLOW)

        # Check for game over
        if player_lives <= 0:
            display_surface.blit(game_over_text, game_over_text_rect)
            display_surface.blit(continue_text, continue_text_rect)
            pygame.display.update()

            # Pause the game until the player clicks then reset
            pygame.mixer.music.stop()
            is_paused = True

            while is_paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_paused = False
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                        score = 0
                        player_lives = PLAYER_STARTING_LIVES
                        clown_velocity = CLOWN_STARTING_VELOCITY
                        clown_image_rect.center = (WIDTH // 2, HEIGHT // 2)

                        clown_dx = random.choice([-1, 1])
                        clown_dy = random.choice([-1, 1])
                        pygame.mixer.music.play()

                        is_paused = False

    # Blit the background image and HUD elements regardless of pause state
    display_surface.blit(background_image, background_image_rect)
    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(lives_text, lives_text_rect)

    # Blit the clown only when not paused or after game over screen has been shown.
    if not is_paused and player_lives > 0:
        display_surface.blit(clown_image, clown_image_rect)

    # If paused show paused text overlay.
    if is_paused:
        display_surface.blit(paused_text, paused_text_rect)

    # Update the screen
    pygame.display.flip()

    # Tick the clock at FPS rate.
    clock.tick(FPS)

# End game cleanly.
pygame.quit()
import random
import pygame


# Initialize pygame
pygame.init()

# Set display surface
WIDTH = 945
HEIGHT = 600
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Catch the Clown')

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

# Set fonts
font = pygame.font.Font('assets/Franxurter.ttf', 32)
font2 = pygame.font.Font('assets/Franxurter.ttf', 22)

# Set text
title_text = font.render('Catch the Clown', True, BLUE)
title_text_rect = title_text.get_rect()
title_text_rect.topleft = (50, 10)

score_text = font.render('Score: ' + str(score), True, YELLOW)
score_text_rect = score_text.get_rect()
score_text_rect.topright = (WIDTH -50, 10)

lives_text =font.render('Lives: ' + str(player_lives), True, YELLOW)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (WIDTH - 50, 50)

game_over_text = font.render('GAMEOVER', True, BLUE, YELLOW)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WIDTH // 2, HEIGHT // 2)

continue_text = font.render('Click anywhere to play again', True, YELLOW, BLUE)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (WIDTH // 2, HEIGHT // 2 + 64)

created_by_text = font2.render('Created by: MAHYAR', True, YELLOW)
created_by_text_rect = created_by_text.get_rect()
created_by_text_rect.bottomright = (WIDTH - 10, HEIGHT)

# Set sound and music
click_sound = pygame.mixer.Sound('assets/click_sound.wav')
click_sound.set_volume(.02)
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
miss_sound.set_volume(.02)
pygame.mixer.music.load('assets/ctc_background_music.wav')
pygame.mixer.music.set_volume(.05)

# set images
background_image = pygame.image.load('assets/background.png')
background_image_rect = background_image.get_rect()
background_image_rect.topleft = (0, 0)

clown_image = pygame.image.load('assets/clown.png')
clown_image_rect = clown_image.get_rect()
clown_image_rect.center = (WIDTH // 2, HEIGHT // 2)

# The main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # A mouse click is made
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos_x = event.pos[0]
            pos_y = event.pos[1]

            # The clown was clicked
            if clown_image_rect.collidepoint(pos_x, pos_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                # Move the clown in a new direction
                previous_dx = clown_dx
                previous_dy = clown_dy
                while previous_dx == clown_dx and previous_dy == clown_dy:
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
                    # print('Clicked!')
                    # print(clown_dx, clown_dy)
                    # print(clown_image_rect.x, clown_image_rect.y)
            else:
                miss_sound.play()
                player_lives -= 1
                # print('Clicked!')
                # print(clown_dx, clown_dy)
                # print(clown_image_rect.x, clown_image_rect.y)

    # Move the clown
    clown_image_rect.x += clown_dx * clown_velocity
    clown_image_rect.y += clown_dy * clown_velocity

    # Bounce the clown off the edges of the screen
    if clown_image_rect.left <= 0 or clown_image_rect.right >= WIDTH:
        clown_dx *= -1
    if clown_image_rect.top <= 0 or clown_image_rect.bottom >= HEIGHT:
        clown_dy *= -1

    # update hud
    score_text = font.render('Score: ' + str(score), True, YELLOW)
    lives_text = font.render('Lives: ' + str(player_lives), True, YELLOW)

    # Check for game over
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(continue_text, continue_text_rect)
        pygame.display.update()

        # Pause the game until the player clicks then reset
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # The player wants to continue
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES

                    clown_image_rect.center = (WIDTH // 2, HEIGHT // 2)
                    clown_velocity = CLOWN_STARTING_VELOCITY

                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False

                # The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Blit the background
    display_surface.blit(background_image, background_image_rect)

    # Blit HUD
    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(lives_text, lives_text_rect)
    display_surface.blit(created_by_text, created_by_text_rect)

    # Blit assets
    display_surface.blit(clown_image, clown_image_rect)

    # Update the display and tick clock
    pygame.display.flip()
    clock.tick(FPS)

# End game
pygame.quit()
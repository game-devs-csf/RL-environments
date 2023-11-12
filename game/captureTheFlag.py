import pygame
import sys

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # Choose the font for the score, None means default font

# Set the frames per second (FPS)
FPS = 60

# Set up some constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
FLAG_SIZE = 20
PLAYER_SPEED = 5
HALF_WIDTH = WIDTH // 2

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)  # Color for the dividing line

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the players and flags
player1 = pygame.Rect(0, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
player2 = pygame.Rect(WIDTH - PLAYER_SIZE, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
flag1 = pygame.Rect(0, 0, FLAG_SIZE, FLAG_SIZE)
flag2 = pygame.Rect(WIDTH - FLAG_SIZE, HEIGHT - FLAG_SIZE, FLAG_SIZE, FLAG_SIZE)

# Scoring
score1 = 0
score2 = 0

# Game loop
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.y - PLAYER_SPEED > 0:
        player1.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player1.y + PLAYER_SPEED < HEIGHT - PLAYER_SIZE:
        player1.y += PLAYER_SPEED
    if keys[pygame.K_a] and player1.x - PLAYER_SPEED > 0:
        player1.x -= PLAYER_SPEED
    if keys[pygame.K_d] and player1.x + PLAYER_SPEED < WIDTH - PLAYER_SIZE:
        player1.x += PLAYER_SPEED

    if keys[pygame.K_UP] and player2.y - PLAYER_SPEED > 0:
        player2.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player2.y + PLAYER_SPEED < HEIGHT - PLAYER_SIZE:
        player2.y += PLAYER_SPEED
    if keys[pygame.K_LEFT] and player2.x - PLAYER_SPEED > 0:
        player2.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player2.x + PLAYER_SPEED < WIDTH - PLAYER_SIZE:
        player2.x += PLAYER_SPEED

   # Scoring
    if player1.colliderect(flag2):
        score1 += 1
        player1.x = 0
        player1.y = HEIGHT // 2
        player2.x = WIDTH - PLAYER_SIZE
        player2.y = HEIGHT // 2
    if player2.colliderect(flag1):
        score2 += 1
        player1.x = 0
        player1.y = HEIGHT // 2
        player2.x = WIDTH - PLAYER_SIZE
        player2.y = HEIGHT // 2

    # Player reset
    if player1.colliderect(player2) and player1.x + PLAYER_SIZE / 2 > HALF_WIDTH:
        player1.x = 0
        player1.y = HEIGHT // 2
    if player2.colliderect(player1) and player2.x + PLAYER_SIZE / 2 < HALF_WIDTH:
        player2.x = WIDTH - PLAYER_SIZE
        player2.y = HEIGHT // 2

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)
    pygame.draw.rect(screen, RED, flag1)
    pygame.draw.rect(screen, BLUE, flag2)

    # Draw the scores
    score_text = font.render(f"Player 1: {score1} Player 2: {score2}", True, WHITE)
    screen.blit(score_text, (20, 20))  # Adjust the position as needed

    # Draw the dividing line
    pygame.draw.line(screen, WHITE, (HALF_WIDTH, 0), (HALF_WIDTH, HEIGHT), 2)

    # Update the display
    pygame.display.flip()

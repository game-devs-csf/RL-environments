import pygame
import sys
from pygame import Vector2

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
PLAYER_SPEED = 5
PLAYER_SIZE = 40
BALL_SPEED = 3
FPS = 60  # Frames per second

# Initialize scores
score1 = 0
score2 = 0

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the players and the ball
player1 = pygame.Rect(WIDTH // 2, HEIGHT - 20, PLAYER_SIZE, PLAYER_SIZE)  # Increased size from 10, 10 to 20, 20
player2 = pygame.Rect(WIDTH // 2, 20, PLAYER_SIZE, PLAYER_SIZE)  # Increased size from 10, 10 to 20, 20
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 10)

# Set up the direction and speed of the ball
ball_velocity = pygame.Vector2(0, 0)

# Set up the players' velocities
player1_velocity = pygame.Vector2(0, 0)
player2_velocity = pygame.Vector2(0, 0)

# Create a clock object
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)  # This will delay the loop to run at 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Reset velocities
    player1_velocity = pygame.Vector2(0, 0)
    player2_velocity = pygame.Vector2(0, 0)

   # Move the players and update their velocities
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player1.move_ip(-PLAYER_SPEED, 0)
        player1_velocity.x = -PLAYER_SPEED
    if keys[pygame.K_d]:
        player1.move_ip(PLAYER_SPEED, 0)
        player1_velocity.x = PLAYER_SPEED
    if keys[pygame.K_w]:
        player1.move_ip(0, -PLAYER_SPEED)
        player1_velocity.y = -PLAYER_SPEED
    if keys[pygame.K_s]:
        player1.move_ip(0, PLAYER_SPEED)
        player1_velocity.y = PLAYER_SPEED

    if keys[pygame.K_LEFT]:
        player2.move_ip(-PLAYER_SPEED, 0)
        player2_velocity.x = -PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player2.move_ip(PLAYER_SPEED, 0)
        player2_velocity.x = PLAYER_SPEED
    if keys[pygame.K_UP]:
        player2.move_ip(0, -PLAYER_SPEED)
        player2_velocity.y = -PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player2.move_ip(0, PLAYER_SPEED)
        player2_velocity.y = PLAYER_SPEED

    # Collide with walls
    if player1.left < 0: 
        player1.left = 0
        player1_velocity.x *= -1
    if player1.right > WIDTH: 
        player1.right = WIDTH
        player1_velocity.x *= -1
    if player1.top < 0: 
        player1.top = 0
        player1_velocity.y *= -1
    if player1.bottom > HEIGHT: 
        player1.bottom = HEIGHT
        player1_velocity.y *= -1

    # Collide with walls
    if player2.left < 0: 
        player2.left = 0
        player2_velocity.x *= -1
    if player2.right > WIDTH: 
        player2.right = WIDTH
        player2_velocity.x *= -1
    if player2.top < 0: 
        player2.top = 0
        player2_velocity.y *= -1
    if player2.bottom > HEIGHT: 
        player2.bottom = HEIGHT
    player2_velocity.y *= -1

    # Move the ball
    ball.move_ip(ball_velocity)

    # Collide with walls
    if ball.left < 0 or ball.right > WIDTH:
        ball_velocity.x *= -1
    if ball.top < 0 or ball.bottom > HEIGHT:
        ball_velocity.y *= -1

    # Collide with players
    if ball.colliderect(player1):
        if player1_velocity.length() == 0:
            if ball.centerx < player1.centerx:  # Ball hit left side of player
                ball_velocity.x = -abs(ball_velocity.x)
            else:  # Ball hit right side of player
                ball_velocity.x = abs(ball_velocity.x)
            ball_velocity.y *= -1
        else:
            ball_velocity += pygame.Vector2(player1_velocity.x, player1_velocity.y)
    if ball.colliderect(player2):
        if player2_velocity.length() == 0:
            if ball.centerx < player2.centerx:  # Ball hit left side of player
                ball_velocity.x = -abs(ball_velocity.x)
            else:  # Ball hit right side of player
                ball_velocity.x = abs(ball_velocity.x)
            ball_velocity.y *= -1
        else:
            ball_velocity += pygame.Vector2(player2_velocity.x, -player2_velocity.y)

    # Apply friction
    ball_velocity *= 0.99

    # Check for scoring
    if ball.top < 0:
        score1 += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_velocity = pygame.Vector2(0, 0)  # Reset ball speed
        player1.center = (WIDTH // 2, HEIGHT - 20)  # Reset player1 position
        player2.center = (WIDTH // 2, 20)  # Reset player2 position
    if ball.bottom > HEIGHT:
        score2 += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_velocity = pygame.Vector2(0, -0)  # Reset ball speed
        player1.center = (WIDTH // 2, HEIGHT - 20)  # Reset player1 position
        player2.center = (WIDTH // 2, 20)  # Reset player2 position

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), player1)
    pygame.draw.rect(screen, (255, 255, 255), player2)
    pygame.draw.rect(screen, (255, 255, 255), ball)

    # Draw scores
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player 1: {score1} Player 2: {score2}", True, (255, 255, 255))
    screen.blit(text, (20, 20))

    # Print velocities
    print(f"\rPlayer 1 velocity: {player1_velocity} Player 2 velocity: {player2_velocity}", end="")
    

    # Flip the display
    pygame.display.flip()
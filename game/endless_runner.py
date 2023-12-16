import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Endless Runner Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define the floor
floor_y = window_height - 50  # 50 is the height of the floor
floor_height = 50
floor_color = (171, 55, 12)  # RGB color for brownish orange

# Define player properties
player_width = 50
player_height = 50
base_player_height = player_height  # Store the original player height
ducking_height = 30  # Height of the player when ducking
player_x = 100
player_y = floor_y - player_height  # Player spawns above the floor
player_speed = 5
player_velocity = 0  # New velocity variable

# Define jump force
jump_force = 20

# Define the obstacle properties
obstacle_width = 50
obstacle_height = 50
obstacle_x = window_width  # Start from the right edge of the window
obstacle_y = floor_y - obstacle_height  # Obstacle spawns at the floor level
obstacle_speed = 7.5

# Define gravity
gravity = 1.5

# Define the score
score = 0
frame_counter = 0
font = pygame.font.Font(
    None, 36
)  # Choose the font for the score, None means the default font
# Calculate the offset
offset = window_width * 0.05

# Define the dodges counter
dodges = 0

# Define the obstacle colors
floor_level_color = (121, 217, 85)  # RGB color for green
above_floor_color = (135, 206, 235)  # RGB color for sky blue

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if (
        keys[pygame.K_SPACE] and player_y == floor_y - player_height
    ):  # Only allow jumping when on the floor
        player_velocity = -jump_force  # Use the jump force variable here
    if keys[pygame.K_DOWN]:  # If the down key is pressed
        player_height = ducking_height  # Duck
    else:
        player_height = 50  # Stand up

    # Apply gravity and velocity
    player_velocity += gravity  # Gravity pulls down
    player_y += player_velocity  # Velocity moves the player

    # Move the obstacle
    obstacle_x -= obstacle_speed

    # Prevent the player from falling through the floor
    if player_y > floor_y - player_height:
        player_y = floor_y - player_height
        player_velocity = 0

    # Check for collision
    if player_x + player_width > obstacle_x and player_x < obstacle_x + obstacle_width:
        if (
            player_y + player_height > obstacle_y
            and player_y < obstacle_y + obstacle_height
        ):
            print("Game Over")
            running = False

    # Apply gravity
    if player_y < floor_y - player_height:  # Only apply gravity if above the floor
        player_y += gravity

    # Increase the score
    frame_counter += 1

    # Increase the score every n frames
    if frame_counter % 2 == 0:
        score += 1

    # Create the score text
    score_text = font.render(
        "Score: " + str(score), True, (0, 0, 0)
    )  # The color is black
    # Create the dodges text
    dodges_text = font.render(
        "Dodges: " + str(dodges), True, (0, 0, 0)
    )  # The color is black

    # Set the obstacle color based on its y-coordinate
    if obstacle_y == floor_y - obstacle_height:
        obstacle_color = floor_level_color
    else:
        obstacle_color = above_floor_color

    # Draw the game objects
    window.fill(white)
    pygame.draw.rect(window, black, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(
        window,
        obstacle_color,
        (obstacle_x, obstacle_y, obstacle_width, obstacle_height),
    )
    pygame.draw.rect(
        window, floor_color, (0, floor_y, window_width, floor_height)
    )  # Draw the floor
    # Draw the score text
    window.blit(
        score_text, (window_width - score_text.get_width() - offset, 0)
    )  # Subtract the offset from the x-coordinate
    # Draw the dodges text below the score text
    window.blit(
        dodges_text,
        (window_width - dodges_text.get_width() - offset, score_text.get_height()),
    )
    pygame.display.update()

    # Reset obstacle position
    # Check if the obstacle has moved past the player
    if obstacle_x + obstacle_width < player_x:
        # Increment the dodges counter
        dodges += 1
        # Reset the obstacle
        obstacle_x = window_width
        obstacle_y = random.choice(
            [
                floor_y - obstacle_height,
                floor_y - obstacle_height - base_player_height / 1.5,
            ]
        )

    clock.tick(60)

# Quit the game
pygame.quit()

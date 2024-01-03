import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
FPS = 60  # Frames per second


class Colors:
    """
    Description:
        Color palette to be used in the game as RGB (int, int, int) tuples.
    """

    BLACK = (28, 28, 28)
    RED = (227, 34, 33)
    GREEN = (3, 192, 60)
    BLUE = (33, 227, 227)
    MAGENTA = (215, 108, 224)
    GREY = (171, 178, 191)
    WHITE = (239, 233, 244)


class Player:
    """
    Description:
        Player in the field capable of moving in 8 directions while inside the
        pitch, interact with the ball and score.
    Parameters:
    Class:
        _SIZE(int): side length
        _SPEED(float): movement speed on the pitch
    Instance:
        _score(int): accumulated score
        _color(int, int, int): displayed color
        _velocity(pygame.Vector2): velocity vector for player movement
        _initial_pos(int, int): initial position at kick-off
        _rect(pygame.Rect): rectangular coordinates
    """

    _SIZE = 25
    _SPEED = 5

    def __init__(self, color, initial_pos):
        self._score = 0
        self._color = color
        self._velocity = pygame.Vector2()
        self._initial_pos = initial_pos
        self._rect = pygame.Rect(self._initial_pos, (Player._SIZE, Player._SIZE))

    def reset(self):
        """Reset position and velocity"""
        self._rect.topleft = self._initial_pos
        self._velocity.update()

    def move(self, pitch, left, right, up, down):
        """Move player inside the screen according to its velocity"""
        self._velocity.update()  # Reset velocity to Vector2(0, 0)
        if left:
            self._velocity.x -= Player._SPEED
        if right:
            self._velocity.x += Player._SPEED
        if up:
            self._velocity.y -= Player._SPEED
        if down:
            self._velocity.y += Player._SPEED

        self._rect.move_ip(self._velocity)  # Move to new position
        self._rect.clamp_ip(pitch)  # Ensure it's inside the pitch

    def scored(self):
        """Add 1 to the score"""
        self._score += 1

    def get_score(self):
        """Return player score"""
        return self._score

    def get_color(self):
        """Return player color"""
        return self._color

    def get_rect(self):
        """Return player coordinates"""
        return self._rect

    def get_velocity(self):
        """Return player velocity"""
        return self._velocity


if __name__ == "__main__":
    # Ball constants
    BALL_SPEED = 1.5
    BALL_SIZE = 10

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set up the players and the ball
    player1 = Player(Colors.BLUE, (Player._SIZE // 2, HEIGHT // 2))
    player2 = Player(Colors.RED, (WIDTH - Player._SIZE // 2, HEIGHT // 2))
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

    # Set up the direction and speed of the ball
    ball_velocity = pygame.Vector2(0, 0)

    # Create a clock object
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)  # This will delay the loop to run at 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("\nGame Finished")
                sys.exit()

        # Move the players and update their velocities
        # checking for wall collisions
        keys = pygame.key.get_pressed()

        player1.move(
            screen.get_rect(),
            keys[pygame.K_a],
            keys[pygame.K_d],
            keys[pygame.K_w],
            keys[pygame.K_s],
        )

        player2.move(
            screen.get_rect(),
            keys[pygame.K_LEFT],
            keys[pygame.K_RIGHT],
            keys[pygame.K_UP],
            keys[pygame.K_DOWN],
        )

        # Move the ball
        ball.move_ip(ball_velocity)

        # Collide with walls
        if ball.left < 0 or ball.right > WIDTH:
            ball_velocity.x *= -1
        if ball.top < 0 or ball.bottom > HEIGHT:
            ball_velocity.y *= -1

        # Collide with players
        if ball.colliderect(player1.get_rect()):
            if player1.get_velocity().length() == 0:
                if (
                    ball.centerx < player1.get_rect().centerx
                ):  # Ball hit left side of player
                    ball_velocity.x = -abs(ball_velocity.x)
                else:  # Ball hit right side of player
                    ball_velocity.x = abs(ball_velocity.x)
                ball_velocity.y *= -1
            else:
                ball_velocity += pygame.Vector2(
                    player1.get_velocity().x, player1.get_velocity().y
                )
        if ball.colliderect(player2.get_rect()):
            if player2.get_velocity().length() == 0:
                if (
                    ball.centerx < player2.get_rect().centerx
                ):  # Ball hit left side of player
                    ball_velocity.x = -abs(ball_velocity.x)
                else:  # Ball hit right side of player
                    ball_velocity.x = abs(ball_velocity.x)
                ball_velocity.y *= -1
            else:
                ball_velocity += pygame.Vector2(
                    player2.get_velocity().x, player2.get_velocity().y
                )

        # Apply friction
        ball_velocity *= 0.75

        # Check for scoring
        if ball.left < 0:
            player2.scored()
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_velocity = pygame.Vector2(0, 0)  # Reset ball speed
            player1.reset()
            player2.reset()
        if ball.right > WIDTH:
            player1.scored()
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_velocity = pygame.Vector2(0, -0)  # Reset ball speed
            player1.reset()
            player2.reset()

        # Draw everything
        screen.fill(Colors.BLACK)
        pygame.draw.rect(screen, player1.get_color(), player1.get_rect())
        pygame.draw.rect(screen, player2.get_color(), player2.get_rect())
        pygame.draw.rect(screen, Colors.GREY, ball)

        # Draw scores
        font = pygame.font.Font(None, 36)
        text = font.render(
            f"Player 1: {player1.get_score()} Player 2: {player2.get_score()}",
            True,
            (255, 255, 255),
        )
        screen.blit(text, (20, 20))

        # Print velocities
        print(
            f"\rPlayer 1 velocity: {player1.get_velocity()} "
            f"Player 2 velocity: {player2.get_velocity()}",
            end="     ",
        )

        # Flip the display
        pygame.display.flip()

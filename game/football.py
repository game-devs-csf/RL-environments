import pygame
import sys


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


class GameObject:
    """
    Description:
        Displayed game object with rectangular coordinates and color.
    Parameters:
        _rect(pygame.Rect): Rectangular coordinates
        _color(int, int, int): Displayed color
    """

    def __init__(self):
        self._rect = None
        self._color = None

    def get_rect(self):
        """Return rectangular coordinates."""
        return self._rect

    def get_color(self):
        """Return displayed color."""
        return self._color

    def draw(self, screen):
        """Draw GameObject on the screen"""
        pygame.draw.rect(screen, self._color, self._rect)


class Player(GameObject):
    """
    Description:
        Player in the field capable of moving in 8 directions while inside the
        pitch, interact with the ball and score.
    Parameters:
    Class:
        _SIZE(int): side length
        _SPEED(float): movement speed on the pitch
    Instance:
        _rect(pygame.Rect): rectangular coordinates
        _color(int, int, int): displayed color
        _score(int): accumulated score
        _velocity(pygame.Vector2): velocity vector for player movement
        _initial_pos(int, int): initial position at kick-off
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

    def get_velocity(self):
        """Return player velocity"""
        return self._velocity


class Ball(GameObject):
    """
    Description:
        Ball to be moved by the players and used to score goals.
        Collides with pitch walls and players.
    Parameters:
        _SIZE(int): side length
        _COLOR(int, int, int): displayed color
        _SPEED(float): movement speed on the pitch
        _FRICTION(float): movement dampening factor
        _INITIAL_POS(int, int)
        _rect(pygame.Rect): rectangular coordinates
        _velocity(pygame.Vector2): velocity vector for movement
        _color(int, int, int): Displayed color
    """

    _SIZE = 10
    _COLOR = Colors.WHITE
    _SPEED = 1.5
    _FRICTION = 0.75
    _INITIAL_POS = (0, 0)

    def __init__(self, pitch):
        Ball._INITIAL_POS = pitch.get_rect().center
        self._rect = pygame.Rect(Ball._INITIAL_POS, (Ball._SIZE, Ball._SIZE))
        self._velocity = pygame.Vector2()
        self._color = Ball._COLOR

    def reset(self):
        """Reset velocity and position"""
        self._rect.center = Ball._INITIAL_POS
        self._velocity.update()

    def bounce(self, x, y):
        """Revert velocity in given axes"""
        if x:
            self._velocity.x *= -1
        if y:
            self._velocity.y *= -1

    def get_velocity(self):
        """Return ball velocity"""
        return self._velocity


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set up some constants
    WIDTH, HEIGHT = 640, 480
    FPS = 60  # Frames per second

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set up the players and the ball
    player1 = Player(Colors.BLUE, (Player._SIZE // 2, HEIGHT // 2))
    player2 = Player(Colors.RED, (WIDTH - Player._SIZE // 2, HEIGHT // 2))
    ball = Ball(screen)
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

        ball_rect = ball.get_rect()

        # Move the ball
        ball_rect.move_ip(ball.get_velocity())

        # Collide with walls
        ball_x_collision = (
            ball_rect.left < screen.get_rect().left
            or ball_rect.right > screen.get_rect().right
        )
        ball_y_collision = (
            ball_rect.top < screen.get_rect().top
            or ball_rect.bottom > screen.get_rect().bottom
        )
        ball.bounce(ball_x_collision, ball_y_collision)

        # Collide with players
        for player in (player1, player2):
            if ball_rect.colliderect(player.get_rect()):
                if player.get_velocity().length() == 0:
                    if (
                        ball_rect.centerx < player.get_rect().centerx
                    ):  # Ball hit left side of player
                        ball.bounce(1, 0)
                        ball_rect.right = player.get_rect().left
                    else:  # Ball hit right side of player
                        ball.bounce(1, 0)
                        ball_rect.left = player.get_rect().right
                    ball.bounce(0, 1)
                else:
                    ball.get_velocity().xy += player.get_velocity()

        # Apply friction
        # TODO: Lower this for more control over ball trayectory
        # Use high values for "automatic testing" of collisions and ball
        # movement
        ball.get_velocity().xy *= 0.95

        # Check for scoring
        if ball.get_rect().left < 0:
            player2.scored()
            ball.reset()
            player1.reset()
            player2.reset()
        if ball.get_rect().right > WIDTH:
            player1.scored()
            ball.reset()
            player1.reset()
            player2.reset()

        ball_rect = ball.get_rect()
        if not screen.get_rect().contains(ball_rect):
            ball_rect.clamp_ip(screen.get_rect())

            for player_rect in [i.get_rect() for i in (player1, player2)]:
                if ball_rect.colliderect(player_rect):
                    if ball_rect.left == screen.get_rect().left:
                        player_rect.left = ball_rect.right
                    elif ball_rect.right == screen.get_rect().right:
                        player_rect.right = ball_rect.left

                    if ball_rect.top == screen.get_rect().top:
                        player_rect.top = ball_rect.bottom
                    elif ball_rect.bottom == screen.get_rect().bottom:
                        player_rect.bottom = ball_rect.top

        # Draw everything
        screen.fill(Colors.BLACK)
        for player in (player1, player2):
            player.draw(screen)
        ball.draw(screen)

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

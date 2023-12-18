import random

import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces


class EndlessRunnerEnv(gym.Env):
    metadata = {"render.modes": ["human"], "render_fps": 60}

    def __init__(self, render_mode="human"):
        self.window_width = 800
        self.window_height = 400
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Endless Runner Game")

        # Define colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Define the floor
        self.floor_y = self.window_height - 50  # 50 is the height of the floor
        self.floor_height = 50
        self.floor_color = (171, 55, 12)  # RGB color for brownish orange

        # Define player properties
        self.player_width = 50
        self.player_height = 50
        self.base_player_height = self.player_height  # Store the original player height
        self.ducking_height = 30  # Height of the player when ducking
        self.player_x = 100
        self.player_y = (
            self.floor_y - self.player_height
        )  # Player spawns above the floor
        self.player_speed = 5
        self.player_velocity = 0  # New velocity variable

        # Define jump force
        self.jump_force = 20

        # Define the obstacle properties
        self.obstacle_width = 50
        self.obstacle_height = 50
        self.obstacle_x = self.window_width  # Start from the right edge of the window
        self.obstacle_y = random.choice(
            [
                self.floor_y - self.obstacle_height,
                self.floor_y - self.obstacle_height - self.base_player_height / 1.5,
            ]
        )
        self.obstacle_speed = 7.5

        # Define gravity
        self.gravity = 1.5

        # Define the score
        self.score = 0
        self.frame_counter = 0
        self.font = pygame.font.Font(
            None, 36
        )  # Choose the font for the score, None means the default font
        # Calculate the offset
        self.offset = self.window_width * 0.05

        # Define the dodges counter
        self.dodges = 0

        # Define the obstacle colors
        self.floor_level_color = (121, 217, 85)  # RGB color for green
        self.above_floor_color = (135, 206, 235)  # RGB color for sky blue

        # Game loop
        self.clock = pygame.time.Clock()
        self.framerate = 60

        # Observation space
        # The obstacle_x goes from window_width (800 for now) to 50 (player_x - obstacle_width)
        # Try different bin sizes for the obstacle_x
        self.observation_space = spaces.Dict(
            {
                "player_y": spaces.Box(
                    low=self.floor_y - self.player_height,
                    high=300,
                    shape=(1,),
                    dtype=np.float32,
                ),
                "obstacle_x": spaces.Box(
                    low=self.player_x - self.obstacle_width,
                    high=self.window_width,
                    shape=(1,),
                    dtype=np.float32,
                ),
                "obstacle_y": spaces.Box(
                    low=self.floor_y - self.obstacle_height,
                    high=self.floor_y
                    - self.obstacle_height
                    - self.base_player_height / 1.5,
                    shape=(1,),
                    dtype=np.float32,
                ),
            }
        )

        # Action space
        self.action_space = spaces.Discrete(3)  # 0: do nothing, 1: jump, 2: duck

        # Action to keycode mapping
        self.action_to_keycode = {
            0: None,
            1: pygame.K_SPACE,
            2: pygame.K_DOWN,
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    def _get_obs(self):
        return {
            "player_y": self.player_y,
            "obstacle_x": self.obstacle_x,
            "obstacle_y": self.obstacle_y,
        }

    def _get_info(self):
        return {"score": self.score, "dodges": self.dodges}

    def reset(self, seed=None, options=None):
        # Reset the environment to its initial state
        super().reset(seed=seed)

        # Reset the player
        self.player_y = self.floor_y - self.player_height
        self.player_velocity = 0
        self.player_height = self.base_player_height

        # Reset the obstacle
        self.obstacle_x = self.window_width
        self.obstacle_y = random.choice(
            [
                self.floor_y - self.obstacle_height,
                self.floor_y - self.obstacle_height - self.base_player_height / 1.5,
            ]
        )

        # Reset the score
        self.score = 0
        self.frame_counter = 0
        self.dodges = 0

        observation = self._get_obs()

        info = self._get_info()

        return observation, info

    def step(self, action):
        # Perform one step in the environment based on the given action

        # Move the player
        keys = pygame.key.get_pressed()
        if (
            keys[pygame.K_SPACE] and self.player_y == self.floor_y - self.player_height
        ):  # Only allow jumping when on the floor
            self.player_velocity = -self.jump_force  # Use the jump force variable here
        if keys[pygame.K_DOWN]:  # If the down key is pressed
            self.player_height = self.ducking_height  # Duck
        else:
            self.player_height = 50  # Stand up

        # Apply gravity and velocity
        self.player_velocity += self.gravity  # Gravity pulls down
        self.player_y += self.player_velocity  # Velocity moves the player

        # Move the obstacle
        self.obstacle_x -= self.obstacle_speed

        # Prevent the player from falling through the floor
        if self.player_y > self.floor_y - self.player_height:
            self.player_y = self.floor_y - self.player_height
            self.player_velocity = 0

        # Check for collision
        if (
            self.player_x + self.player_width > self.obstacle_x
            and self.player_x < self.obstacle_x + self.obstacle_width
        ):
            if (
                self.player_y + self.player_height > self.obstacle_y
                and self.player_y < self.obstacle_y + self.obstacle_height
            ):
                print("Game Over")
                reward = -1
                terminated = True

        # Apply gravity
        if (
            self.player_y < self.floor_y - self.player_height
        ):  # Only apply gravity if above the floor
            self.player_y += self.gravity

        # Increase the score
        self.frame_counter += 1

        # Increase the score every n frames
        if self.frame_counter % 2 == 0:
            self.score += 1

        # Reset obstacle position
        # Check if the obstacle has moved past the player
        if self.obstacle_x + self.obstacle_width < self.player_x:
            # Increment the dodges counter
            self.dodges += 1
            reward = 1
            # Reset the obstacle
            self.obstacle_x = self.window_width
            self.obstacle_y = random.choice(
                [
                    self.floor_y - self.obstacle_height,
                    self.floor_y - self.obstacle_height - self.base_player_height / 1.5,
                ]
            )

        observation = self._get_obs()

        info = self._get_info()

        if self.render_mode == "human":
            self.render()
        # Return (observation, reward, terminated, truncated, info)
        return observation, reward, terminated, False, info

    def render(self):
        # Render the current state of the environment
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="human")'
            )
            return
        else:
            return self._render(self.render_mode)

    def _render_frame(self, mode: str):
        # Render the current frame of the environment
        if self.window is None and self.render_mode == "human":
            pygame.init()
            # pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        # Create the score text
        score_text = self.font.render(
            "Score: " + str(self.score), True, (0, 0, 0)
        )  # The color is black
        # Create the dodges text
        dodges_text = self.font.render(
            "Dodges: " + str(self.dodges), True, (0, 0, 0)
        )  # The color is black
        distance_text = self.font.render(
            "Obstacle x: " + str(self.obstacle_x), True, (0, 0, 0)
        )  # The color is black

        # Set the obstacle color based on its y-coordinate
        if self.obstacle_y == self.floor_y - self.obstacle_height:
            obstacle_color = self.floor_level_color
        else:
            obstacle_color = self.above_floor_color

        # Draw the game objects
        self.window.fill(self.white)
        pygame.draw.rect(
            self.window,
            self.black,
            (self.player_x, self.player_y, self.player_width, self.player_height),
        )
        pygame.draw.rect(
            self.window,
            obstacle_color,
            (
                self.obstacle_x,
                self.obstacle_y,
                self.obstacle_width,
                self.obstacle_height,
            ),
        )
        pygame.draw.rect(
            self.window,
            self.floor_color,
            (0, self.floor_y, self.window_width, self.floor_height),
        )  # Draw the floor
        # Draw the score text
        self.window.blit(
            score_text, (self.window_width - score_text.get_width() - self.offset, 0)
        )  # Subtract the offset from the x-coordinate
        # Draw the dodges text below the score text
        self.window.blit(
            dodges_text,
            (
                self.window_width - dodges_text.get_width() - self.offset,
                score_text.get_height(),
            ),
        )
        # Draw the distance text below the dodges text
        self.window.blit(
            distance_text,
            (
                self.window_width - distance_text.get_width() - self.offset,
                score_text.get_height() + dodges_text.get_height(),
            ),
        )
        pygame.display.update()

        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.window is not None:
            # Quit the game
            pygame.quit()

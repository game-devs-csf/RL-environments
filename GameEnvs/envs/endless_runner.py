import random

import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces


class EndlessRunnerEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60, "obstacle_x_bins": 75}

    def __init__(self, render_mode="human"):
        self.window_width = 800
        self.window_height = 400

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
        self.player_state = 0  # 0: standing, 1: ducking, 2: jumping
        self.obstacle_height_to_binary = 0  # 0: floor, 1: above floor
        # The obstacle_x goes from window_width (800 for now) to 50 (player_x - obstacle_width)
        # Try different bin sizes for the obstacle_x
        self.observation_space = spaces.Dict(
            {
                "player_state": spaces.Discrete(
                    3
                ),  # 0: standing, 1: ducking, 2: jumping
                "obstacle_x": spaces.Box(
                    low=self.player_x - self.obstacle_width,  # Behind the player
                    high=self.window_width,  # Starting point
                    shape=(1,),
                    dtype=np.float32,
                ),
                "obstacle_height": spaces.Discrete(2),  # 0: floor, 1: above floor
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

    def _get_obs(
        self,
    ):
        # Bin the obstacle_x into n bins
        obstacle_x_bins = np.linspace(
            self.player_x - self.obstacle_width,
            self.window_width,
            self.metadata["obstacle_x_bins"],
        )
        obstacle_x_binned = np.digitize(self.obstacle_x, obstacle_x_bins)
        return {
            "player_state": self.player_state,  # 0: standing, 1: ducking, 2: jumping
            "obstacle_x": obstacle_x_binned,
            "obstacle_height": self.obstacle_height_to_binary,  # 0: floor, 1: above floor
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
        reward = 0
        terminated = False
        # Move the player
        # keys = pygame.key.get_pressed()
        if (
            action == 1 and self.player_y == self.floor_y - self.player_height
        ):  # Only allow jumping when on the floor
            self.player_velocity = -self.jump_force  # Use the jump force variable here
        if action == 2:  # If the down key is pressed
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

            # Convert the obstacle_y to binary
            if (
                self.obstacle_y == self.floor_y - self.obstacle_height
            ):  # If the obstacle is on the floor
                self.obstacle_height_to_binary = 0
            else:  # If the obstacle is above the floor
                self.obstacle_height_to_binary = 1

            # Determine the state of the player (jumping, ducking, standing)
            if (
                self.player_y == self.floor_y - self.player_height
            ):  # If the player is standing
                self.player_state = 0  # Standing
            elif (
                self.player_y
                < self.floor_y - self.player_height - self.base_player_height / 1.5
            ):  # If the player is ducking
                self.player_state = 1  # Ducking
            else:  # If the player is jumping
                self.player_state = 2  # Jumping

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
            return self._render_frame(self.render_mode)

    def _render_frame(self, mode: str):
        # Render the current frame of the environment
        if self.window is None and self.render_mode == "human":
            pygame.init()
            # pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height)
            )
            pygame.display.set_caption("Endless Runner Game")
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

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

        pygame.display.update()

        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.window is not None:
            # Quit the game
            pygame.quit()

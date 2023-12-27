import numpy as np
import pygame
import random
import math
import time
import os
import sys

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Add the project's root directory to sys.path
sys.path.append(project_root)

from baseEnv.env import Env  # noqa: E402
from baseMdl.mdl import Mdl  # noqa: E402


class CartpoleEnv(Env):
    """
    Description:
        A pole is attached by an un-actuated joint to a cart, which moves along a frictionless track.
        The pendulum starts upright, and the goal is to prevent it from falling over by increasing and reducing the cart's velocity.
        Based on:
            - https://gymnasium.farama.org/environments/classic_control/cart_pole/
            - https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py

    Parameters:
        envName (str): The name of the environment
    """

    def __init__(self, envName):
        """
        Description:
            Initializes the environment

        Parameters:
            envName (str): The name of the environment
        """
        super().__init__(envName)

        # Indicates the direction of the fixed force the cart is pushed with
        self.action_space = [0, 1]
        self.force_mag = 10.0
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = self.masspole + self.masscart
        self.length = 0.5
        self.polemass_length = self.masspole * self.length
        self.tau = 0.02

        # Angle at which to fail the episode
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        self.reset()

    def reset(self, show_display=pygame.SHOWN):
        """
        Description:
            Resets the environment to its initial state

        Returns:
            state (tuple): The new state of the environment
        """
        super().reset(show_display)

        self.reward = 0

        self.episode_length = 0

        """
        The state of the environment is the position of the cart, the velocity of the cart, the angle of the pole, and the angular velocity of the pole tip

        cartPosition: -4.8 to 4.8
        cartVelocity: -Inf to Inf
        poleAngle: -0.418 rad to 0.418 rad
        poleVelocity: -Inf to Inf
        """
        self.state = tuple((random.uniform(-0.05, 0.05) for _ in range(4)))

        return self.state

    def step(self, action):
        """
        Description:
            Moves the environment one step forward in time

        Parameters:
            action (int): The action to take in the environment

        Returns:
            state (tuple): The new state of the environment
            reward (float): The reward for the action taken
            done (bool): Whether the episode is over
        """

        # Unpack the state
        x, x_dot, theta, theta_dot = self.state

        # Calculate the force applied to the cart, based on https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
        force = self.force_mag if action == 1 else -self.force_mag

        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        temp = (
            force + self.polemass_length * theta_dot**2 * sintheta
        ) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.length * (4.0 / 3.0 - self.masspole * costheta**2 / self.total_mass)
        )
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc

        self.state = (x, x_dot, theta, theta_dot)

        # Check if the episode is over
        if self.episode_length >= 500:
            reward = 0
            return self.state, reward, True

        # Check if the cart has moved too far to the left or right
        if self.state[0] < -4.8 or self.state[0] > 4.8:
            reward = 0
            return self.state, reward, True

        # Check if the pole has fallen over
        if self.state[2] < -0.42 or self.state[2] > 0.42:
            reward = 0
            return self.state, reward, True

        reward = 1
        self.episode_length += 1

        return self.state, reward, False

    def render(self):
        """
        Description:
            Renders the environment
        """
        self.env.fill((255, 255, 255))

        w, h = self.window_size

        # Draw the ground
        pygame.draw.line(self.env, (50, 50, 50), (0, h // 2 + 15), (w, h // 2 + 15), 1)

        # Calculate the position of the center of the cart
        x_1 = ((self.state[0] / 4.8) + 1) * w / 2
        y_1 = h // 2 + 10

        # Calculate the position of the end of the pole
        origin = pygame.math.Vector2(x_1, y_1)
        end = pygame.math.Vector2(150, 0)

        # Rotate the pole by the angle theta, and by 90 degrees to make it point up
        rot_end = origin + end.rotate_rad(-self.state[2] - math.pi / 2)

        # Draw the cart
        pygame.draw.rect(self.env, (0, 0, 0), pygame.Rect(x_1 - 30, h // 2, 60, 30))

        # Draw the pole
        pygame.draw.line(self.env, (235, 177, 52), origin, rot_end, 10)

        super().render()

        # Wait for tau seconds
        time.sleep(self.tau)


class CartpoleMdl(Mdl):
    """
    Description:
        A model makes desitions on whether to accelerate the cart left or
        right in order to balance the pole attached to it.
        It interacts with the CartpoleEnv to maximize its total reward.
    Parameters:
        mdl_name (str): name of the model
        environment (CartpoleEnv): environment with which it interacts
    """

    def __init__(self, mdl_name, environment):
        """
        Description:
            Initializes the model
        Parameters:
            mdl_name (str): name of the model
            environment (CartpoleEnv): environment with which it interacts
        """
        # Sets name and env
        super().__init__(mdl_name, environment)
        # For discretizing
        self.upper_bounds = [4.8, 3.4, 0.42, 3.4]
        self.lower_bounds = [-4.8, -3.4, -0.42, -3.4]
        self.buckets = (
            1,
            1,
            6,
            5,
        )
        # For training
        self.pisodes = 501
        self.alpha = 0.1
        self.gamma = 0.9
        # For exploration
        self.epsilon = 1.0
        self.min_epsilon = 0.1
        self.max_epsilon = 1.0
        self.decay = 0.01

    def train_from_scratch(self):
        """Train new model with brand new q_table"""
        self.q_table = np.zeros(self.buckets + (len(self.env.action_space),))

        print(f"Training model from scratch for {self.episodes - 1}" f"episodes...")
        for episode in range(self.episodes):
            current_state = self.discretize(
                self.environment.reset(pygame.HIDDEN),
                self.lower_bounds,
                self.upper_bounds,
                self.buckets,
            )

            total_reward = 0

            epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(
                -self.decay * episode
            )

            while self.env.running:
                exp_tradeoff = random.uniform(0, 1)

                if exp_tradeoff > epsilon:
                    action = np.argmax(self.q_table[current_state])
                else:
                    action = random.choice(self.env.action_space)

                observation, reward, done = self.env.step(action)

                new_state = self.discretize(
                    observation, self.lower_bounds, self.upper_bounds, self.buckets
                )

                total_reward += reward

                self.q_table[current_state][action] += self.alpha * (
                    reward
                    + self.gamma * np.max(self.q_table[new_state])
                    - self.q_table[current_state][action]
                )

                current_state = new_state

                if done:
                    self.env.running = False

            if not episode % 100:
                print(
                    f"Episode: {episode} | Reward: {total_reward} "
                    f"| Epsilon: {epsilon}"
                )

    def watch_trained_model(self):
        """Watch model in its environment."""
        current_state = self.discretize(
            self.env.reset(), self.lower_bounds, self.upper_bounds, self.buckets
        )
        total_reward = 0

        print("Watching trained model...")
        while self.env.running:
            self.env.render()

            action = np.argmax(self.q_table[current_state])

            observation, reward, done = self.env.step(action)

            new_state = self.discretize(
                observation, self.lower_bounds, self.upper_bounds, self.buckets
            )

            total_reward += reward

            current_state = new_state

            if done:
                self.env.running = False
                print(f"Total Reward: {total_reward}")
        print("Finished watching trained model...")

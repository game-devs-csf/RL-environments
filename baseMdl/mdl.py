import random
import numpy as np
import pygame


class Mdl:
    """
    Description:
        Base class for models

    Parameters:
        modelName (str): The name of the model
        environment (Env): The environment of the model
    """

    def __init__(self, mdl_name, environment):
        # Name and Env
        self.mdlName = mdl_name
        self.env = environment
        # The model itself
        self.q_table = None
        # For discretizing
        self.upper_bounds = None
        self.lower_bounds = None
        self.buckets = None
        # For training
        self.episodes = None
        self.alpha = None
        self.gamma = None
        # For training exploration
        self.min_epsilon = None
        self.max_epsilon = None
        self.decay = None

    def discretize(obs, lower_bounds, upper_bounds, buckets):
        """Discretize the observation space into buckets."""
        ratios = [
            (ob + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i])
            for i, ob in enumerate(obs)
        ]
        new_obs = [int(round((buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
        new_obs = [min(buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        return tuple(new_obs)

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

    def import_model(self):
        while True:
            mdl_file = input("Enter model file name (.npy): ")
            try:
                self.q_table = np.load(mdl_file, allow_pickle=False)
            except OSError:
                print(
                    f"The input file {mdl_file}.npy doesn't exist "
                    f"or cannot be read."
                )
            except ValueError:
                print(
                    f"The file {mdl_file} contains an object array, but can't "
                    f"be read due to allow_pickle=False"
                )
            except EOFError:
                print(
                    f"All data has already been read from file {mdl_file}.\n"
                    f"Can't read an empty file."
                )

    def watch_trained_model(self):
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

    def ask_to_save_model(self):
        while True:
            save = input("Save model? [y/N]: ")
            if save in ("", "N", "n"):
                return
            elif save in ("Y", "y"):
                mdl_file = input("Enter model file name: ")
                np.save(mdl_file, self.q_table)
                return

            print("Please enter 'y' or 'n'.\n" "Or press ENTER for default 'n'.")

import os, sys
import time
import random
import numpy as np
import pygame

#import pygame
#import sys
#
#class Env:
#    """
#        Description:
#            Base class for environments
#
#        Parameters:
#            envName (str): The name of the environment
#            width (int): The width of the environment window
#            height (int): The height of the environment window
#    """
#    def __init__(self, envName, width = 500, height = 500):
#        self.envName = envName
#        self.action_space = None
#        self.observation_space = None
#        self.env = None
#        self.running = False
#        self.window_size = (width, height)
#        self.reward = None
#
#    def step(self, action):
#        pass
#
#    def reset(self, show_display = pygame.SHOWN):
#        """
#            Description:
#                Resets the environment to its initial state
#        """
#        pygame.init()
#        pygame.display.set_caption(self.envName)
#        self.env = pygame.display.set_mode(self.window_size, pygame.HWSURFACE | pygame.DOUBLEBUF | show_display)
#        self.running = True
#
#    def render(self):
#        """
#            Description:
#                Renders the environment
#        """
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                self.running = False
#            elif event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_ESCAPE:
#                    self.running = False
#
#        pygame.display.flip()
#
#    def close(self):
#        pygame.quit()
#        sys.exit()


class Model():
    """
        Description:
            Base class for models

        Parameters:
            modelName (str): The name of the model
            environment (Env): The environment of the model
    """
    def __init__(self, mdl_name, environment):
        self.mdlName = mdlName
        self.environment = environment
        self.upper_bounds = None
        self.lower_bounds = None
        self.buckets = None
        self.q_table = None

    def discretize(obs, lower_bounds, upper_bounds, buckets):
        """Discretize the observation space into buckets."""
        ratios = [(ob + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i, ob in enumerate(obs)]
        new_obs = [int(round((buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
        new_obs = [min(buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        return tuple(new_obs)

    def train_from_scratch():
        """Train new model with brand new q_table"""
        q_table = np.zeros(buckets + (len(env.action_space),))

        episodes = 501

        alpha = 0.1
        gamma = 0.9

        # exploration
        epsilon = 1.0
        min_epsilon = 0.1
        max_epsilon = 1.0
        decay = 0.01

        print(f"Training model from scratch for {episodes - 1} episodes...")
        for episode in range(episodes):
            
            current_state = discretize(env.reset(pygame.HIDDEN), lower_bounds, upper_bounds, buckets)

            total_reward = 0

            epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

            while env.running:

                exp_tradeoff = random.uniform(0, 1)

                if exp_tradeoff > epsilon:
                    action = np.argmax(q_table[current_state])
                else:
                    action = random.choice(env.action_space)
                
                observation, reward, done = env.step(action)

                new_state = discretize(observation, lower_bounds, upper_bounds, buckets)

                total_reward += reward
                
                q_table [current_state][action] += alpha * (reward + gamma * np.max(q_table[new_state]) - q_table[current_state][action])

                current_state = new_state

                # env.render()

                if done:
                    env.running = False

            if not episode % 100:
                print(f"Episode: {episode} | Reward: {total_reward} | Epsilon: {epsilon}")

        return q_table

    def import_model():
        while True:
            mdl_file = input("Enter model file name (.npy): ")
            try:
                return np.load(mdl_file, allow_pickle=False)
            except OSError:
                print(f"The input file {mdl_file} doesn't exist "
                      f"or cannot be read.")
            except ValueError:
                print(f"The file {mdl_file} contains an object array, but can't "
                      f"be read due to allow_pickle=False")
            except EOFError:
                print(f"All data has already been read from file {mdl_file}.\n"
                      f"Can't read an empty file.")

    def watch_trained_model(mdl_q_table):
        current_state = discretize(env.reset(), lower_bounds, upper_bounds, buckets)
        total_reward = 0

        print("Watching trained model...")
        while True:
            env.render()

            action = np.argmax(mdl_q_table[current_state])

            observation, reward, done = env.step(action)

            new_state = discretize(observation, lower_bounds, upper_bounds, buckets)

            total_reward += reward

            current_state = new_state

            if done:
                break
        print("Finished watching trained model...")

    def ask_to_save_model(mdl_q_table):
        while True:
            save = input("Save model? [y/N]: ")
            if save in ("", "N", "n"):
                return
            elif save in ("Y", "y"):
                mdl_file = input("Enter model file name: ")
                np.save(mdl_file, mdl_q_table)
                return
            
            print("Please enter 'y' or 'n'.\n"
                  "Or press ENTER for default 'n'.")

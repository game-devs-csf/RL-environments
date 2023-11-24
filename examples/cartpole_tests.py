from cartPole.cartpole import CartpoleEnv
import os
import sys
import random
import numpy as np
import pygame

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Add the project's root directory to sys.path
sys.path.append(project_root)


# This function discretizes the observation space into buckets
def discretize(obs, lower_bounds, upper_bounds, buckets):
    ratios = [
        (ob + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i])
        for i, ob in enumerate(obs)
    ]
    new_obs = [int(round((buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
    new_obs = [min(buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
    return tuple(new_obs)


# Create an instance of the Cartpole environment
env = CartpoleEnv("Cartpole")

upper_bounds = [4.8, 3.4, 0.42, 3.4]
lower_bounds = [-4.8, -3.4, -0.42, -3.4]

buckets = (
    1,
    1,
    6,
    5,
)

q_table = np.zeros(buckets + (len(env.action_space),))

episodes = 501

alpha = 0.1
gamma = 0.9

# exploration
epsilon = 1.0
min_epsilon = 0.1
max_epsilon = 1.0
decay = 0.01

for episode in range(episodes):
    current_state = discretize(
        env.reset(pygame.HIDDEN), lower_bounds, upper_bounds, buckets
    )

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

        q_table[current_state][action] += alpha * (
            reward + gamma * np.max(q_table[new_state]) - q_table[current_state][action]
        )

        current_state = new_state

        # env.render()

        if done:
            env.running = False

    if not episode % 100:
        print(f"Episode: {episode} | Reward: {total_reward} | Epsilon: {epsilon}")

current_state = discretize(env.reset(), lower_bounds, upper_bounds, buckets)
total_reward = 0

while True:
    env.render()

    action = np.argmax(q_table[current_state])

    observation, reward, done = env.step(action)

    new_state = discretize(observation, lower_bounds, upper_bounds, buckets)

    total_reward += reward

    current_state = new_state

    if done:
        break

# Close the environment
env.close()

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

from cartPole.cartpole import CartpoleEnv  # noqa: E402


def discretize(obs, bins):
    return tuple(np.digitize(ob, bin) - 1 for ob, bin in zip(obs, bins))


# Create an instance of the Cartpole environment
env = CartpoleEnv("Cartpole")

upper_bounds = [4.8, 3.4, 0.42, 3.4]
lower_bounds = [-4.8, -3.4, -0.42, -3.4]

buckets = (
    np.linspace(-4.8, 4.8, 5),
    np.linspace(-3.4, 3.4, 5),
    np.linspace(-0.42, 0.42, 18),
    np.linspace(-3.4, 3.4, 18),
)

q_table = np.random.uniform(
    low=-1,
    high=1,
    size=tuple(len(bucket) for bucket in buckets) + (len(env.action_space),),
)

episodes = 4001

alpha = 0.1
gamma = 0.99

# exploration
epsilon = 1.0
min_epsilon = 0.1
max_epsilon = 1.0
decay = 0.001

for episode in range(episodes):
    current_state = discretize(env.reset(pygame.HIDDEN), buckets)

    total_reward = 0

    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

    while env.running:
        exp_tradeoff = random.uniform(0, 1)

        if exp_tradeoff > epsilon:
            action = np.argmax(q_table[current_state])
        else:
            action = random.choice(env.action_space)

        observation, reward, done = env.step(action)

        new_state = discretize(observation, buckets)

        total_reward += reward

        # print(current_state, new_state)
        q_table[current_state][action] += alpha * (
            reward + gamma * np.max(q_table[new_state]) - q_table[current_state][action]
        )

        current_state = new_state

        # env.render()

        if done:
            env.running = False

    if not episode % 100:
        print(f"Episode: {episode} | Reward: {total_reward} | Epsilon: {epsilon}")

current_state = discretize(env.reset(), buckets)
total_reward = 0

done = False
while not done:
    env.render()

    action = np.argmax(q_table[current_state])

    observation, reward, done = env.step(action)

    new_state = discretize(observation, buckets)

    total_reward += reward

    current_state = new_state

print(f"Total reward: {total_reward}")
# Close the environment
env.close()

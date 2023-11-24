import os, sys
import random
import numpy as np
import pygame

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Add the project's root directory to sys.path
sys.path.append(project_root)

from cartPole.cartpole import CartpoleEnv


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


def train_from_scratch():
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
                reward
                + gamma * np.max(q_table[new_state])
                - q_table[current_state][action]
            )

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
            print(f"The input file {mdl_file} doesn't exist " f"or cannot be read.")
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

        print("Please enter 'y' or 'n'.\n" "Or press ENTER for default 'n'.")


def main():
    run_app = True
    while run_app:
        valid_input = False
        new_model = False
        while not valid_input:
            train = input(
                "==================================\n"
                "        CARTPOLE TESTS\n"
                "==================================\n"
                "\n"
                "Train Model from scratch? [Y/n]: "
            )
            if train in ["", "y", "Y"]:
                mdl_q_table = train_from_scratch()
                new_model = True
                valid_input = True
            elif train in ["n", "N"]:
                mdl_q_table = import_model()
                valid_input = True
            else:
                print("Please enter 'y' or 'n'.\n" "Or press ENTER for default 'y'.")

        watch_trained_model(mdl_q_table)

        if new_model:
            ask_to_save_model(mdl_q_table)

        valid_input = False
        while not valid_input:
            rerun = input("Watch a new model? [Y/n]: ")
            if rerun in ["", "Y", "y"]:
                valid_input = True
            elif rerun in ["N", "n"]:
                run_app = False
                valid_input = True
            else:
                print("Please enter 'y' or 'n'.\n" "Or press ENTER for default 'y'")

    # Close the environment
    env.close()


if __name__ == "__main__":
    main()

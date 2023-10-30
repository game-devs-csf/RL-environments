import os, sys
import time
import random

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Add the project's root directory to sys.path
sys.path.append(project_root)

from cartPole.cartpole import CartpoleEnv

# Create an instance of the Cartpole environment
env = CartpoleEnv("Cartpole")

# Initialize the environment
env.reset()

# Run the environment 10 times
for _ in range(10):
    time.sleep(1)
    env.reset()

    while env.running:
        
        observation, reward, done = env.step(random.randint(0, 1))
        
        env.render()

        if done:
            env.running = False

# Close the environment
env.close()
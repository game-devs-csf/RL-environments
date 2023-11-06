# Cartpole Environment

## Description

This environment implements the cart-pole problem. A pole is attached by a joint to a cart, which moves along a frictionless track. The pendulum is placed upright on the cart and the goal is to balance the pole by applying forces in the left and right direction on the cart.

## Action space

The cart can be accelerated left or right.

## Environment

The agent knows the following attributes from the game state:

- Pole angle
- Pole angular velocity

Optional:

- Cart position
- Cart velocity

## Training

The simulation is run for 1,000 episodes of 500 game-state steps. An episode is interrupted if the pole's angle is greater than 30 degrees away from being upright.

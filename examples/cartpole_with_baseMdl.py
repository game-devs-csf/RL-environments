import os
import sys

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Add the project's root directory to sys.path
sys.path.append(project_root)

from cartPole.cartpole_with_baseMdl import CartpoleEnv, CartpoleMdl  # noqa: E402


# Create an instance of the Cartpole environment
env = CartpoleEnv("Cartpole")
# Create an instance of teh Cartpole model
mdl = CartpoleMdl("CartpoleMdl", env)


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
                mdl.train_from_scratch()
                new_model = True
                valid_input = True
            elif train in ["n", "N"]:
                mdl.import_model()
                valid_input = True
            else:
                print("Please enter 'y' or 'n'.\n" "Or press ENTER for default 'y'.")

        mdl.watch_trained_model()

        if new_model:
            mdl.ask_to_save_model()

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

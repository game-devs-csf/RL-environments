import numpy as np


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
        pass

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
        pass

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

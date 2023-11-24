import pygame
import sys


class Env:
    """
    Description:
        Base class for environments

    Parameters:
        envName (str): The name of the environment
        width (int): The width of the environment window
        height (int): The height of the environment window
    """

    def __init__(self, envName, width=500, height=500):
        self.envName = envName
        self.action_space = None
        self.observation_space = None
        self.env = None
        self.running = False
        self.window_size = (width, height)
        self.reward = None

    def step(self, action):
        pass

    def reset(self, show_display=pygame.SHOWN):
        """
        Description:
            Resets the environment to its initial state
        """
        pygame.init()
        pygame.display.set_caption(self.envName)
        self.env = pygame.display.set_mode(
            self.window_size, pygame.HWSURFACE | pygame.DOUBLEBUF | show_display
        )
        self.running = True

    def render(self):
        """
        Description:
            Renders the environment
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        pygame.display.flip()

    def close(self):
        pygame.quit()
        sys.exit()

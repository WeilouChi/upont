import pygame
from settings import *

class Ending:
    def __init__(self) -> None:
        
        # setup
        self.display_surface = pygame.display.get_surface()

        # backround
        self.background = pygame.image.load('../graphics/background/ending.png')
        self.background = pygame.transform.scale(self.background, (750, 500))


    def run(self):
        self.display_surface.blit(self.background, (310,100))



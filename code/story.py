import pygame
from settings import *
from support import import_folder


class Story:
    def __init__(self, surface, story_index) -> None:
        
        # setup
        self.display_surface = surface
        self.story_index = story_index
        self.frames = import_folder('../graphics/story')

        # background
        if story_index >= 5:
            story_index = 5
        self.story_bg = self.frames[story_index]
        self.story_bg = pygame.transform.scale(self.story_bg, (1280, 550))
        self.story_enter = pygame.image.load('../graphics/background/story_enter.png')
        self.story_enter = pygame.transform.scale(self.story_enter, (160, 50))

        

    def run(self):
        #pygame.display.flip()
        self.display_surface.blit(self.story_bg, (0,100))
        self.display_surface.blit(self.story_enter, (1100, 650))


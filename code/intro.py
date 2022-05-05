import pygame
from settings import *
from support import import_folder

class Us(pygame.sprite.Sprite):
    def __init__(self, direction, path) -> None:
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.y = 620
        if direction == 'R':
            self.x = 1180
            self.rect = self.image.get_rect(center = (self.x, self.y))
            self.pos = False
            self.stop = 680
        else:
            self.x = 100
            self.rect = self.image.get_rect(center = (self.x, self.y))
            self.pos = True
            self.stop = 530

    def animate(self):
        self.frame_index += 0.15
        self.speed = 1
        
        if self.rect.x != self.stop:
            if self.pos:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

        else:
            self.image = self.frames[0]
            


    def update(self) -> None:
        self.animate()



class Intro:
    def __init__(self) -> None:
        
        # setup
        self.display_surface = pygame.display.get_surface()

        # backround
        self.background = pygame.image.load('../graphics/background/bg.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        self.headline = pygame.image.load('../graphics/background/headline.png')

        self.setup_upont()
        self.setup_me()

    def setup_upont(self):
        self.upont = pygame.sprite.Group()
        upont_sprite = Us('R', '../graphics/player/left')
        self.upont.add(upont_sprite)

    def setup_me(self):
        self.me = pygame.sprite.Group()
        me_sprite = Us('L', '../graphics/me/right')
        self.me.add(me_sprite)

    def run(self):
        pygame.display.flip()
        self.display_surface.blit(self.background, (0,0))
        self.display_surface.blit(self.headline, (250, 60))

        self.upont.update()
        self.me.update()

        self.upont.draw(self.display_surface)
        self.me.draw(self.display_surface)

        
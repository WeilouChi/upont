import pygame, sys
from settings import *
from level import Level

class GameStates():
    def __init__(self) -> None:
        self.state = 'intro'

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Upon T')
        self.clock = pygame.time.Clock()

        self.level = Level()
        if self.state == 'main_game':
            # sound
            main_sound = pygame.mixer.Sound('../audio/main.ogg')
            main_sound.set_volume(0.4)
            main_sound.play(loops= -1)

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.K_RETURN:
                self.state = 'main_game'

        self.screen.fill(WATER_COLOR)
        pygame.display.update()
        self.clock.tick(FPS)

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.level.toggle_menu()

        self.screen.fill(WATER_COLOR)
        self.level.run()
        pygame.display.update()
        self.clock.tick(FPS)

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Upon T')
        self.clock = pygame.time.Clock()

        self.level = Level()

        # sound
        main_sound = pygame.mixer.Sound('../audio/main.ogg')
        main_sound.set_volume(0.4)
        main_sound.play(loops= -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    while True:
        game = GameStates()
        game.state_manager()
import pygame
from settings import *

class UltPlayer:
    def __init__(self, animation_player) -> None:
        self.animation_player = animation_player
        self.sprite_type = 'ult'
        self.sounds = {
        'sing': pygame.mixer.Sound('../audio/sing.mp3'),
        'earthquake':pygame.mixer.Sound('../audio/jump.mp3')
        }
        

    def sing(self, player, cost, groups):
        if player.energy >= cost:
            self.sounds['sing'].play()
            player.energy -= cost

            self.animation_player.create_particles('sing', player.rect.center, 0.1, self.sprite_type, groups)

    def earthquake(self, player, cost, groups):
        if player.energy >= cost:
            self.sounds['earthquake'].play(loops=2)
            player.energy -= cost
            
            self.animation_player.create_particles('earthquake', player.rect.center, 0.1, self.sprite_type, groups)


    def ult_range_effect(self, player,duration_time, groups):
        self.animation_player.create_range(player.rect.center, duration_time, groups)

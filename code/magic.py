from random import randint
import pygame
from settings import *

class MagicPlayer:
    def __init__(self, animation_player) -> None:
        self.animation_player = animation_player
        self.sprite_type = 'magic'
        self.sounds = {
        'heal': pygame.mixer.Sound('../audio/heal.wav'),
        'flame':pygame.mixer.Sound('../audio/Fire.wav')
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, 0.15, self.sprite_type, groups)
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), 0.15 ,self.sprite_type ,groups)
    def flame(self, player, cost, groups):
        if player.energy > cost:
            player.energy -= cost
            self.sounds['flame'].play()
            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0, -1)
            elif player.status.split('_')[0] == 'down': direction = pygame.math.Vector2(0, 1)
            else: direction = pygame.math.Vector2(0, 1)

            for i in range(1, 4):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), 0.15, self.sprite_type, groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3) + offset_y
                    self.animation_player.create_particles('flame', (x, y), 0.15,  self.sprite_type, groups)
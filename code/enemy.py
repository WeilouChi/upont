import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player, trigger_death_particles, add_exp, add_energy, add_total_exp):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        self.add_total_exp = add_total_exp
        self.add_energy = add_energy

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # sleep timer
        self.sleep_type = False
        self.sleep_time = None
        self.sleep_duration = 14000
        self.sleeping_can_attack = True
        self.sleeping_duration = 1800
        self.sleeping_time = None

        # sounds
        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.2)

    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'attack':[], 'sleep': []}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self, player):
        if self.sleep_type:
            distance = 500
        else:
            distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            if self.sleep_type:
                self.status = 'sleep'
            else:
                self.status = 'idle'

    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable and self.sleeping_can_attack:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        if self.sleep_type:
            if current_time - self.sleep_time >= self.sleep_duration:
                self.sleep_type = False

        if not self.sleeping_can_attack:
            if current_time - self.sleeping_time >= self.sleeping_duration:
                self.sleeping_can_attack = True

    def get_damage(self,player,attack_type):
        if self.vulnerable:
            
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.hit_sound.play()
                self.health -= player.get_full_weapon_damage()
            elif attack_type == 'magic':
                self.hit_sound.play()
                self.health -= player.get_full_magic_damage()
            else:
                skill = player.get_full_ult_damage()
                if skill == 0 and self.sleep_type == False: # sing
                    self.sleep_time = pygame.time.get_ticks()
                    self.sleep_type = True
                    self.sleeping_time = pygame.time.get_ticks()
                    self.sleeping_can_attack = False
                elif skill > 0: # earthquake
                    self.health -= skill
                    self.hit_sound.play()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

        
    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.add_total_exp(self.exp)
            self.add_energy()
            self.death_sound.play()

    def hit_reaction(self):
        if not self.vulnerable and not self.sleep_type:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
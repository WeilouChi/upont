from matplotlib.pyplot import cool
import pygame 
from settings import *
from support import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites, create_attack, destroy_attack, create_magic, create_ult, create_ult_effect_sprite
    , stats, exp, total_exp, level_num):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/upont.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking =False
        self.ult_attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon 
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 1
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_duration_cooldown = 200
        self.flame_learned = False

        # ult
        self.create_ult = create_ult
        self.create_ult_effect_sprite = create_ult_effect_sprite
        self.ult_index = 0
        self.ult = list(ult_data.keys())[self.ult_index]
        self.can_switch_ult = True
        self.ult_switch_time = None
        self.ult_style = 0
        self.ult_start_time = 0
        self.ult_cooldown = 0
        self.sing_learned = False
        self.earthquake_learned = False
        

        # stats
        self.stats = stats
        self.max_stats = {'health': 300, 'energy': 160, 'attack': 20, 'magic' : 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
        self.health = self.stats['health'] 
        self.energy = self.stats['energy'] 
        self.exp = exp
        self.total_exp = total_exp
        self.speed = self.stats['speed']
        self.level = level_num

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.2)
        self.level_up_sound = pygame.mixer.Sound('../audio/level_up.wav')
        self.level_up_sound.set_volume(0.3)
        self.learned_sound = pygame.mixer.Sound('../audio/learn_new_skill.mp3')
        self.learned_sound.set_volume(0.6)


    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up' : [], 'down' : [], 'left' : [], 'right' : [],
            'right_idle' : [], 'left_idle' : [], 'up_idle' : [], 'down_idle' : [],
            'right_attack' : [], 'left_attack' : [], 'up_attack' : [], 'down_attack' : []  }
        
        for animation in self.animations:
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)


    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack input
            if keys[pygame.K_j]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            # magic input
            if keys[pygame.K_k]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            # ult input
            if keys[pygame.K_l] and self.sing_learned:
                self.attacking = True
                self.ult_attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.ult_style = list(ult_data.keys())[self.ult_index]
                strength = list(ult_data.values())[self.ult_index]['strength']
                cost = list(ult_data.values())[self.ult_index]['cost']
                self.ult_cooldown = list(ult_data.values())[self.ult_index]['cooldown']
                self.ult_start_time = pygame.time.get_ticks()
                self.create_ult(self.ult_style, cost)
                if self.ult_style == 'sing':
                    self.create_ult_effect_sprite(self.ult_cooldown)
            


            if keys[pygame.K_e] and self.can_switch_magic and self.flame_learned:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

            if keys[pygame.K_q] and self.can_switch_ult and self.earthquake_learned:
                self.can_switch_ult = False
                self.ult_switch_time = pygame.time.get_ticks()
                
                if self.ult_index < len(list(ult_data.keys())) - 1:
                    self.ult_index += 1
                else:
                    self.ult_index = 0

                self.ult = list(ult_data.keys())[self.ult_index]
        elif self.ult_style == 'earthquake' and self.ult_attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.ult_start_time >= self.ult_cooldown:
                self.create_ult_effect_sprite(200)
                self.ult_attacking = False




    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
        

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and self.ult_attacking:
            if current_time - self.attack_time >= self.attack_cooldown + ult_data[self.ult]['cooldown']:
                self.attacking = False
                self.ult_attacking = False
                self.destroy_attack()
        elif self.attacking and not self.ult_attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
            

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.can_switch_ult:
            if current_time - self.ult_switch_time >= self.switch_duration_cooldown:
                self.can_switch_ult = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
        

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker 
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_full_ult_damage(self):
        base_damage = self.stats['magic']
        spell_damage = ult_data[self.ult]['strength']
        if spell_damage == 0:
            return 0
        else: 
            return base_damage + spell_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 5
        else:
            self.energy = self.stats['energy']

    def resume(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.0005 * self.stats['energy']
        else:
            self.energy = self.stats['energy']

        if self.health < self.stats['health']:
            self.health += 0.0001 * self.stats['health']
        else:
            self.health = self.stats['health']
    
    def level_up(self):
        need_exp = self.level * 50 + 100
        if need_exp >= 400:
            need_exp = 400
        if self.total_exp >= need_exp:
            self.total_exp -= need_exp
            self.level += 1
            self.level_up_sound.play()
            if self.level % 5 == 0 and self.level <= 15 :
                self.learned_sound.play()

    def learn_skill(self):
        if self.level >= 5:
            self.flame_learned = True
        if self.level >= 10:
            self.sing_learned = True
        if self.level >= 15:
            self.earthquake_learned = True

        

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.resume()
        self.level_up()
        self.learn_skill()


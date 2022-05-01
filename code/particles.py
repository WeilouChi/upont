import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('../graphics/particles/flame/frames'),
            'aura': import_folder('../graphics/particles/aura'),
            'heal': import_folder('../graphics/particles/heal/frames'),

            # ult
            'sing' : import_folder('../graphics/particles/sing/frames'),
            'crack' : import_folder('../graphics/particles/crack'),
            'earthquake' : import_folder('../graphics/particles/earthquake/frames'),

            # attacks 
            'claw': import_folder('../graphics/particles/claw'),
            'slash': import_folder('../graphics/particles/slash'),
            'sparkle': import_folder('../graphics/particles/sparkle'),
            'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
            'thunder': import_folder('../graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('../graphics/particles/smoke_orange'),
            'raccoon': import_folder('../graphics/particles/raccoon'),
            'spirit': import_folder('../graphics/particles/nova'),
            'bamboo': import_folder('../graphics/particles/bamboo'),
            
            # leafs 
            'leaf': (
                import_folder('../graphics/particles/leaf1'),
                import_folder('../graphics/particles/leaf2'),
                import_folder('../graphics/particles/leaf3'),
                import_folder('../graphics/particles/leaf4'),
                import_folder('../graphics/particles/leaf5'),
                import_folder('../graphics/particles/leaf6'),
                self.reflect_images(import_folder('../graphics/particles/leaf1')),
                self.reflect_images(import_folder('../graphics/particles/leaf2')),
                self.reflect_images(import_folder('../graphics/particles/leaf3')),
                self.reflect_images(import_folder('../graphics/particles/leaf4')),
                self.reflect_images(import_folder('../graphics/particles/leaf5')),
                self.reflect_images(import_folder('../graphics/particles/leaf6'))
                )
            }

    def reflect_images(self,frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self,pos,groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos,animation_frames, 0.15 , 'magic', groups)

    def create_particles(self,animation_type,pos, animation_speed,sprite_type ,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames, animation_speed,sprite_type,groups)

    def create_range(self, pos, duration, groups):
        RangeEffect(pos, duration, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames, animation_speed,sprite_type, groups):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.frames = animation_frames 
        self.image = self.frames[self.frame_index]
        if self.sprite_type == 'ult':
             self.rect = self.image.get_rect(center = (pos[0] - 10, pos[1]))
        else:
            self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


class RangeEffect(pygame.sprite.Sprite):
    def __init__(self,pos,duration_time, groups) -> None:
        super().__init__(groups)
        surf = pygame.Surface([400, 400])
        surf.set_colorkey((0,0,0))
        self.image = surf
        self.sprite_type = 'ult'
        self.image.fill('black')
        self.duration_time = duration_time
        self.rect = self.image.get_rect(center = pos)
        self.start_time = pygame.time.get_ticks()

    def duration(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration_time:
            self.kill()

    def update(self):
        self.duration()



import pygame
from  settings import *

class UI:
    def __init__(self) -> None:
        
        # general 
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(130, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(130, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)


        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

        # convert ult dictionary
        self.ult_graphics = []
        for ult in ult_data.values():
            ult = pygame.image.load(ult['graphic']).convert_alpha()
            ult = pygame.transform.scale(ult, (64, 64))
            self.ult_graphics.append(ult)

        # convert avatar dictionary
        avatar = pygame.image.load('../graphics/player/avatar.png')
        avatar = pygame.transform.scale(avatar, (64, 64))
        self.avatar_graphics = [avatar]
        


    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def show_level(self, level):
        text_surf = self.font.render(str(int(level)), False, TEXT_COLOR)

        text_rect = text_surf.get_rect(bottomright = (115, 42))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched=False):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self, weapon_index):
        bg_rect = self.selection_box(10, 630)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_swiched):
        bg_rect = self.selection_box(120, 630, has_swiched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)
    
    def ultimation_opverlay(self, ult_index, has_swiched):
        bg_rect = self.selection_box(230, 630, has_swiched)
        ult_surf = self.ult_graphics[ult_index]
        ult_rect = ult_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(ult_surf, ult_rect)

    def avatar_overlay(self, avatar_index):
        bg_rect = self.selection_box(10, 10)
        avatar_surf = self.avatar_graphics[avatar_index]
        avatar_rect = avatar_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(avatar_surf, avatar_rect)



    def display(self, player, ult_display):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)
        

        self.weapon_overlay(player.weapon_index)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        if ult_display:
            self.ultimation_opverlay(player.ult_index ,not player.can_switch_ult)
        self.avatar_overlay(0)
        self.show_level(player.level)

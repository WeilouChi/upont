import pygame, sys
from settings import *
from level import Level
from intro import Intro
from story import Story

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Upon T')
		self.clock = pygame.time.Clock()

		# state
		self.level_index = 0
		self.intro = Intro()
		self.story_index = 0

		# intro sound
		self.intro_sound = pygame.mixer.Sound('../audio/intro.mp3')
		self.intro_sound.set_volume(0.1)
		self.intro_sound.play()

		# story sound
		self.story_sound = pygame.mixer.Sound('../audio/Lyphard Melody.mp3')
		self.story_sound.set_volume(0.3)

		# weilou sound
		self.weilou_0 = pygame.mixer.Sound('../audio/weilou_level_0.mp3')
		self.weilou_0.set_volume(0.6)
		self.weilou_1 = pygame.mixer.Sound('../audio/weilou_level_1.mp3')
		self.weilou_1.set_volume(0.6)
		self.weilou_2 = pygame.mixer.Sound('../audio/weilou_level_2.mp3')
		self.weilou_2.set_volume(0.6)
		
		# overworld
		self.status = 'intro'

	def create_story(self):
		self.story = Story(self.screen, self.story_index)

	def create_level(self):
		if self.level_index == 0:
			self.level = Level(self.level_index)
		else:
			self.level = Level(self.level_index, self.stats, self.exp, self.total_exp, self.level_num)

	def state_manager(self):
		if self.status == 'intro':
			self.intro.run()
		elif self.status == 'main_game':
			self.level.run()
		elif self.status == 'story':
			self.story.run()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if self.status == 'main_game':
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							self.level.toggle_menu()
						if (self.level.clear and event.key == pygame.K_RETURN) or event.key == pygame.K_ESCAPE:
							self.status = 'story'
							self.story_index += 1
							self.create_story()
							self.level.main_sound.stop()
							self.story_sound.set_volume(0.3)
							self.stats = self.level.stats
							self.exp = self.level.exp
							self.total_exp = self.level.total_exp
							self.level_num = self.level.level_num

							
				elif self.status == 'intro':
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							self.status = 'story'
							self.create_story()
							self.intro_sound.stop()
							self.story_sound.play(loops = -1)

				elif self.status == 'story':
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							if self.level_index <= 2:
								if self.level_index == 0:
									self.weilou_0.play()
								elif self.level_index == 1:
									self.weilou_1.play()
								else:
									self.weilou_2.play()
								self.status = 'main_game'
								self.create_level()
								self.level_index += 1
								self.story_sound.set_volume(0)
							elif self.story_index <= 5 and self.level_index > 2:
								self.story_index += 1
								self.create_story()
							else:
								self.intro_sound.play()
								self.status = 'intro'
								self.level_index = 0
								self.story_index = 0
								self.story_sound.set_volume(0)

			if self.status == 'main_game':
				self.screen.fill(WATER_COLOR)
			elif self.status == 'story':
				self.screen.fill('black')
			self.state_manager()
			pygame.display.update()
			self.clock.tick(FPS)




if __name__ == '__main__':
	game = Game()
	game.run()
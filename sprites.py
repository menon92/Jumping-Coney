# sprite class for platform game
import pygame as pg 
from settings import *
from random import choice, randrange

# define 2D vector 
vec = pg.math.Vector2 

class Spritesheet:
	"""utility class for loading and parsing spritesheets
	   	
       args : image file name
	"""
	
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert()

	def get_scaled_image(self, x, y, width, height, scale_pct = 1.0):
		# take an seuface 
		image = pg.Surface((width, height))
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		image = pg.transform.scale(image, (int(width * scale_pct), int(height * 0.50)))
		return image

	def get_image(self, x, y, widht, height):
		# grab an image out of a larger spritesheet
		image = pg.Surface((widht, height))
		image.blit(self.spritesheet, (0, 0), (x, y, widht, height))
		# resize image
		image = pg.transform.scale(image, (widht // 2, height // 2)) # // for keep int value
		return image

	def get_image_scaled3x(self, x, y, widht, height):
		# grab an image out of a larger spritesheet
		image = pg.Surface((widht, height))
		image.blit(self.spritesheet, (0, 0), (x, y, widht, height))
		# resize image
		image = pg.transform.scale(image, (widht // 3, height // 3)) # // for keep int value
		return image

	def get_image_scaled4x(self, x, y, widht, height):
		# grab an image out of a larger spritesheet
		image = pg.Surface((widht, height))
		image.blit(self.spritesheet, (0, 0), (x, y, widht, height))
		# resize image
		image = pg.transform.scale(image, (widht // 4, height // 4)) # // for keep int value
		return image


class Player(pg.sprite.Sprite):
	"""docstring for Powerup"""
	def __init__(self, game):
		# add all groups when init object
		self._layer = PLAYER_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		# initilize var for animation
		self.walking = False
		self.jumping = False
		self.is_hit_grasses = False
		self.is_hit_cactuses = False
		self.current_frame = 0
		self.last_update = 0
		self.load_image() # load all required image for doing annimation
		# end initilization var for animation

		# self.image = pg.Surface((30, 40))
		# self.image.fill(YELLOW)
		# self.image = self.game.spritesheet.get_image(614, 1063, 120, 191)
		self.image = self.standing_frames[0] # [0] = initial image
		# self.image.set_colorkey(BLACK) # remove black color from image
		self.rect = self.image.get_rect()
		# self.vx = 0 # velocity to x
		# self.vy = 0 # velocity to y
		# self.rect.center = (WIDTH / 2, HEIGHT / 2)
		self.rect.center = (40, HEIGHT - 100)
		self.pos = vec(40, HEIGHT - 100)            # initial position
		self.vel = vec(0, 0)                        # velocity
		self.acc = vec(0, 0)                        # acceleration

	def load_image(self):
		# load standing frames
		self.standing_frames = [self.game.spritesheet.get_image(581, 1265, 121, 191), # bunny2_ready.png
								self.game.spritesheet.get_image(584, 0, 121, 201)]    # bunny2_stant.png
		# remove black color from the frame
		for frame in self.standing_frames:
			frame.set_colorkey(BLACK)

		# load walk_frames for walking in right side 
		self.walk_frames_r = [self.game.spritesheet.get_image(584, 203, 121, 201), # bunny2_walk1.png 
							  self.game.spritesheet.get_image(678, 651, 121, 207)] # bunny2_walk2.png
		# remove black color from the frame / image
		for frame in self.walk_frames_r:
			frame.set_colorkey(BLACK)

		# load walk_frames for walking in left side 
		# to walk left side we need to flip the walk_frames_right
		self.walk_frames_l = []
		for frame in self.walk_frames_r:
			frame.set_colorkey(BLACK)
			self.walk_frames_l.append(pg.transform.flip(frame, True, False)) # True = horizenttally False = not virtically
		
		# load jump frames 
		self.jump_frames = self.game.spritesheet.get_image(416, 1660, 150, 181)
		self.jump_frames.set_colorkey(BLACK)	 

	# I don't know why jump_cut not working
	def jump_cut(self):
		if self.jumping:
			if self.vel.y < -3:
				self.vel.y = 3

	def jump(self):
		# jump only if standing on a platform
		self.rect.x += 2 # chekc collidetion by adding 2 px bello form the current rect.x
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.x += -2
		if hits and not self.jumping:
			self.game.jump_sound.play()
			self.jumping = True
			self.vel.y = -PLAYER_JUMP

	def update(self):
		self.animate()
		# self.vx = 0
		self.acc = vec(0, PLAYER_GRAV)

		# if player hits a grass
		self.rect.x += 1
		grass_hits = pg.sprite.spritecollide(self, self.game.grasses, False)
		# print "grass hits: ", grass_hits
		self.rect.x -= 1
		if grass_hits:
			self.game.hit_grass.play()
			# todo - add grass hit sound		
			# if we hit a grass then we don't want move small reverse side 
			# print "grass hited"
			self.is_hit_grasses = True
			
			if self.rect.centerx < grass_hits[0].rect.centerx:
				self.acc.x = -0.35
			elif self.rect.centerx > grass_hits[0].rect.centerx:
				self.acc.x = 0.35

			if self.game.score >= LOST_POINTS_BY_HIT_GRASS:
				self.game.score -= LOST_POINTS_BY_HIT_GRASS
		else:
			self.is_hit_grasses = False

		# if player hits a cactus
		cactus_hits = pg.sprite.spritecollide(self, self.game.cactuses, False)
		if cactus_hits:
			# print "hit cactus"
			self.game.hit_grass.play()
			self.is_hit_cactuses = True
			if self.rect.centerx < cactus_hits[0].rect.centerx:
				self.acc.x = -0.35
			elif self.rect.centerx > cactus_hits[0].rect.centerx:
				self.acc.x = 0.35 
			
			if self.game.score >= LOST_POINTS_BY_HIT_CACTUS:
				self.game.score -= LOST_POINTS_BY_HIT_CACTUS
		else:
			self.is_hit_cactuses = False

		# track key pressed
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] and not self.is_hit_grasses and not self.is_hit_cactuses:  # if left key is pressed then go left side
			# print "left key pressed"
			# self.vx = -5
			self.acc.x = -PLAYER_ACC
		if keys[pg.K_RIGHT] and not self.is_hit_grasses and not self.is_hit_cactuses: # if right key is pressed then go right siee
			# print "right key pressed"
			# self.vx = 5
			self.acc.x = PLAYER_ACC

		# set up and down action
		# if keys[pg.K_UP]:
		# 	self.acc.y = -0.2
		# if keys[pg.K_DOWN]:
		# 	self.acc.y = 0.2

		# self.rect.x += self.vx
		# self.rect.y += self.vy

		# apply friction on both x, y
		# self.acc += self.vel * PLAYER_FRICTION
		# apply friction on to the x direction not in y direction
		# a = (v - u) / t # u = 0
		self.acc.x += self.vel.x * PLAYER_FRICTION 
		# equation of motion
		self.vel += self.acc # v = u + at
		# if our x velocity is less then 0.1 then we force the velocity 
		# set to zero
		if abs(self.vel.x) < 0.1:
			self.vel.x = 0

		# S = s + ut + 0.5 * a * t * t
		self.pos += self.vel + 0.5 * self.acc
		# wrap around the sides of the screen
		if self.pos.x > WIDTH + self.rect.width / 2:
			self.pos.x = 0 - self.rect.width / 2
		if self.pos.x < 0 - self.rect.width / 2:
			self.pos.x = WIDTH + self.rect.width / 2

		# new positon
		# self.rect.center = self.pos 
		self.rect.midbottom = self.pos  

	def animate(self):
		# get the current time tick
		now = pg.time.get_ticks()

		# chekc we are walking or not. If our velocity is not 0 then we are walking
		if self.vel.x != 0:
			self.walking = True
		else:
			self.walking = False

		# show walk animation
		if self.walking:
			if now - self.last_update > 200:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
				bottom = self.rect.bottom
				if self.vel.x > 0: # we are walking in right 
					self.image = self.walk_frames_r[self.current_frame]
				else: # we are walking in left
					self.image = self.walk_frames_l[self.current_frame]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

		# show ideal animation
		if not self.jumping and not self.walking:
			if now - self.last_update > 350:
				# update the last update tick
				self.last_update = now
				bottom = self.rect.bottom
				# take frame one after another
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				# set that frame to the image 
				self.image = self.standing_frames[self.current_frame]
				# change the bottom of the image
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom
		# maks is for making a pixel perfect collision
		self.mask = pg.mask.from_surface(self.image)


class Platform(pg.sprite.Sprite):
	"""docstring for Powerup"""
	# x = x pos of platform 
	# y = y pos of platform    
	# w = widht of the platform
	# h = height of the platform
	def __init__(self, game, x, y):
		self._layer = PLATFORM_LAYER
		self.groups = game.all_sprites, game.platforms
		pg.sprite.Sprite.__init__(self, self.groups)
		# self.image = pg.Surface((w, h))
		# self.image.fill(GREEN)
		self.game = game
		images = [self.game.spritesheet.get_scaled_image(0, 0, 380, 94, scale_pct = 0.75),
				  self.game.spritesheet.get_scaled_image(262, 1152, 200, 100, scale_pct = 0.75), 
				  self.game.spritesheet.get_scaled_image(0, 672, 380, 94, scale_pct = 0.75), 
				  self.game.spritesheet.get_scaled_image(208, 1879, 201, 100, scale_pct = 0.75), 
				  self.game.spritesheet.get_scaled_image(0, 96, 380, 94, scale_pct = 0.75), 
				  self.game.spritesheet.get_scaled_image(382, 408, 200, 100, scale_pct = 0.75), 
				  self.game.spritesheet.get_scaled_image(0, 288, 380, 94, scale_pct = 0.75), 
				  self.game.spritesheet.get_scaled_image(213, 1662, 201, 100, scale_pct = 0.75)]
		self.image = choice(images)
		self.image.set_colorkey(BLACK)	  
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.set_object_on_platform()

	def set_object_on_platform(self):
		# randomly set powerup onto the  platform
		if randrange(90) < POW_SPAWN_PCT:
			Powerup(self.game, self)

		select = choice(['grass', 'cactus', 'spikeman'])
		# select = 'spikeman'
		if select == 'grass':
			# randomly set grass onto the  platform
			if randrange(100) < GRASS_SPAWN_PCT:
				# print "crate a grass"
				Grass(self.game, self)
		elif select == 'cactus':
			# randomly set cactus onto the  platform
			if randrange(100) < CACTUS_SPAWN_PCT:
				# print "on Cactus spawn"
				Cactus(self.game, self)
		elif select == 'spikeman':
			# randomly set sipke mane onto the platrom
			if randrange(130) < SPIKE_SPAWN_PCT:
				# print "crate an spikeMan"
				SpikeMan(self.game, self)


class Powerup(pg.sprite.Sprite):
	"""docstring for Powerup"""
	def __init__(self, game, plat):
		self._layer = POW_LAYER
		self.groups = game.all_sprites, game.powerups
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.plat = plat
		self.load_images()
		self.type = choice(['boost', 'gold', 'silver', 'bronze'])
		# self.type = choice(['boost'])
		if self.type == 'boost':
			self.image = self.powerup_boost_image
		elif self.type == 'gold':
			self.image = self.gold_images[0] # initial gold image
		elif self.type == 'bronze':
			self.image = self.bronze_images[0] # initial bronze image
		elif self.type == 'silver':
			self.image = self.silver_images[0] # initial silver image

		# initilize variable for animating gold
		self.current_frame_for_gold = 0
		self.last_update_gold = 0
		self.current_frame_for_silver = 0
		self.last_update_silver = 0
		self.current_frame_for_bronze = 0
		self.last_update_bronze = 0

		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = self.plat.rect.centerx
		self.rect.bottom = self.plat.rect.top - 5

	def load_images(self):
		# load boost image
		self.powerup_boost_image = self.game.spritesheet.get_image(820, 1805, 71, 70)
		self.powerup_boost_image.set_colorkey(BLACK)

		# load all gold images
		self.gold_images = [self.game.spritesheet.get_image(698, 1931, 84, 84),  # gold_1 
							self.game.spritesheet.get_image(829, 0, 66, 84),     # gold_2
							self.game.spritesheet.get_image(897, 1574, 50, 84),  # gold_3
							self.game.spritesheet.get_image(645, 651, 15, 84),   # gold_4
							pg.transform.flip(self.game.spritesheet.get_image(829, 0, 66, 84), True, False)] # flip version of gold_2
							
		# remvoe black color form frame
		for frame in self.gold_images:
			frame.set_colorkey(BLACK)

		# load all silver images
		self.silver_images = [self.game.spritesheet.get_image(584, 406, 84, 84),  # silver_1 
							  self.game.spritesheet.get_image(852, 1003, 66, 84), # silver_2
							  self.game.spritesheet.get_image(899, 1219, 50, 84), # silver_3
							  self.game.spritesheet.get_image(662, 651, 14, 84),  # silver_4
							  pg.transform.flip(self.game.spritesheet.get_image(852, 1003, 66, 84), True, False)] # flip version of silver_2
							
		# remvoe black color form frame
		for frame in self.silver_images:
			frame.set_colorkey(BLACK)

		# load all bronze images
		self.bronze_images = [self.game.spritesheet.get_image(707, 296, 84, 84), # bronze_1 
							  self.game.spritesheet.get_image(826, 206, 66, 84), # bronze_2
							  self.game.spritesheet.get_image(899, 116, 50, 84), # bronze_3
							  self.game.spritesheet.get_image(670, 406, 14, 84), # bronze_4
							  pg.transform.flip(self.game.spritesheet.get_image(826, 206, 66, 84), True, False)] # flip version of bronze_2

		# remove black color form frame
		for frame in self.bronze_images:
			frame.set_colorkey(BLACK)

	def update(self):
		self.rect.bottom = self.plat.rect.top - 5

		if self.type == 'gold':
			self.animate_gold()
		elif self.type == 'silver':
			self.animate_silver()
		elif self.type == 'bronze':
			self.animate_bronze()

		if not self.game.platforms.has(self.plat):
			self.kill()

	def animate_gold(self):
		# print "On animate_gold"
		now = pg.time.get_ticks()

		if now - self.last_update_gold > 300:
			self.last_update_gold = now
			# get the curren frame for gold
			self.current_frame_for_gold = (self.current_frame_for_gold + 1) % len(self.gold_images)
			# set this frame for showing
			self.image = self.gold_images[self.current_frame_for_gold]

	def animate_silver(self):
		# print "On animate_silver"
		now = pg.time.get_ticks()
		if now - self.last_update_silver > 300:
			self.last_update_silver = now
			# get current frame for silver
			self.current_frame_for_silver = (self.current_frame_for_silver + 1) % len(self.silver_images)
			# set this frame for showing
			self.image = self.silver_images[self.current_frame_for_silver]

	def animate_bronze(self):
		# print "On animate_bronze"
		now = pg.time.get_ticks()
		if now - self.last_update_bronze > 300:
			self.last_update_bronze = now
			self.current_frame_for_bronze = (self.current_frame_for_bronze + 1) % len(self.bronze_images)
			self.image = self.bronze_images[self.current_frame_for_bronze]


class Cloud(pg.sprite.Sprite):
	"""docstring for Powerup"""
 	def __init__(self, game):
 		self._layer = CLOUD_LAYER
 		self.groups = game.all_sprites, game.clouds
 		pg.sprite.Sprite.__init__(self, self.groups)
 		self.game = game
 		self.image = choice(self.game.cloud_images)
 		self.image.set_colorkey(BLACK)
 		self.rect = self.image.get_rect()
 		scale = randrange(50, 101) / 100.0
 		# print "scale", scale

 		self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), 
 		 											 int(self.rect.height * scale)))
 		self.rect.x = randrange(0, WIDTH - self.rect.width)
 		self.rect.y = randrange(-500, -50)

 		# print "self.rect.x", self.rect.x
 		# print "self.rect.y", self.rect.y

 	def update(self):
 		if self.rect.top > HEIGHT * 2:
 			self.kill()


class Mob(pg.sprite.Sprite):
	"""docstring for Powerup"""
	def __init__(self, game):
		self._layer = MOB_LAYER
		self.groups = game.all_sprites, game.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
		self.image_up.set_colorkey(BLACK)
		self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)
		self.image_down.set_colorkey(BLACK)
		self.image = self.image_up
		self.rect = self.image.get_rect()
		self.rect.centerx = choice([-100, WIDTH - 100])
		self.vx = randrange(1, 4)
		if self.rect.centerx > WIDTH:
			self.vx *= -1
		self.vy = 0
		self.dy = 0.5

	def update(self):
		self.rect.x += self.vx
		self.vy += self.dy
		if self.vy > 3 or self.vy < -3:
			self.dy *= -1
		center = self.rect.center
		if self.dy < 0:
			self.image = self.image_up
		else:
			self.image = self.image_down
		self.rect = self.image.get_rect()
		self.maks = pg.mask.from_surface(self.image)
		self.rect.center = center
		self.rect.y += self.vy
		if self.rect.left > WIDTH + 100 or self.rect.right < -100:
			self.kill()


class WingMan(pg.sprite.Sprite):
	"""docstring for Powerup"""
	def __init__(self, game):
		self._layer = ENIMES_LAYER
		self.groups = game.all_sprites, game.wingmans
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.load_enime_images()
		# self.type = choice(['wing_man', 'spike_man'])
		self.type = choice(['wing_man'])

		# init variable for animation
		self.last_update_wing_man = 0
		self.current_frame_for_wing_man = 0
		self.last_update_spike_man = 0
		self.current_frame_for_spike_man = 0
		
		# select image for choice 
		if self.type == 'wing_man':
			self.image = self.wing_man_images[0] # initial wingMan image
		# elif self.type == 'spike_man':
		# 	self.image = self.spike_man_walk_right_images[1] # initial spikeMan image

		self.rect = self.image.get_rect()
		# self.rect.centerx = choice([-100, WIDTH - 200])
		self.rect.centerx = -100 # aways start before left 
		self.rect.centery = randrange(-50, HEIGHT - 400)
		self.vx = randrange(1, 3) # initial velocity

	def load_enime_images(self):
		self.wing_man_images = [self.game.spritesheet.get_image(382, 635, 174, 126),  # wingMan1.png
		                        self.game.spritesheet.get_image(0, 1879, 206, 107),   # wingMan2.png
		                        self.game.spritesheet.get_image(0, 1559, 216, 101),   # wingMan3.png
		                        self.game.spritesheet.get_image(0, 1456, 216, 101),   # wingMan4.png
		                        self.game.spritesheet.get_image(382, 510, 182, 123),  # wingMan5.png
		                        self.game.spritesheet.get_image(0, 1456, 216, 101),   # wingMan4.png
		                        self.game.spritesheet.get_image(0, 1559, 216, 101),   # wingMan3.png
		                        self.game.spritesheet.get_image(0, 1879, 206, 107)]   # wingMan2.png
		for frame in self.wing_man_images:
			frame.set_colorkey(BLACK)

		self.spike_man_walk_right_images = [self.game.spritesheet.get_image(704, 1256, 120, 159), # spikeMan_walk1
		                                    self.game.spritesheet.get_image(812, 296, 90, 155)]   # spikeMan_walk2
		for frame in self.spike_man_walk_right_images:
			frame.set_colorkey(BLACK)

		self.spike_man_walk_left_images = []
		for frame in self.spike_man_walk_right_images:
			frame.set_colorkey(BLACK)
			self.spike_man_walk_left_images.append(pg.transform.flip(frame, True, False))

	def update(self):
		if self.type == 'wing_man':
			self.animate_wing_man()
		elif self.type == 'spike_man':
			pass

		self.rect.x += self.vx

		if self.rect.left > WIDTH:
			self.kill()

	def animate_wing_man(self):
		now = pg.time.get_ticks()
		if now - self.last_update_wing_man > 200:
			self.last_update_wing_man = now
			self.current_frame_for_wing_man = (self.current_frame_for_wing_man + 1) % len(self.wing_man_images)
			self.image = self.wing_man_images[self.current_frame_for_wing_man]
	
	def animate_spike_main(self):
		pass


class SpikeMan(pg.sprite.Sprite):
	"""docstring for Powerup"""
	def __init__(self, game, plat):
		self._layer = ENIMES_LAYER
		self.groups = game.all_sprites, game.spikemans
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.plat = plat
		self.load_spike_man_images()
		# self.type = choice(['wing_man', 'spike_man'])
		self.type = choice(['spike_man'])

		# init variable for animation
		self.last_update_spike_man = 0
		self.current_frame_for_spike_man = 0

		self.walking_right = True
		self.walking_left = False
		self.hit_staus = False
		
		# select image for choice 
		if self.type == 'spike_man':
			self.image = self.spike_man_walk_right_images[0] # initial wingMan image

		self.rect = self.image.get_rect()
		# print "spikeman self.rect:", self.rect
		self.rect.centerx = self.plat.rect.centerx
		self.rect.bottom = self.plat.rect.top 
		self.vx = 1 # randrange(1, 3) # initial velocity

	def load_spike_man_images(self):
		self.spike_man_walk_right_images = [self.game.spritesheet.get_image_scaled3x(812, 296, 90, 155),   # spikeMan_walk2
											self.game.spritesheet.get_image_scaled3x(704, 1256, 120, 159)] # spikeMan_walk1
		
		# self.spike_man_walk_right_images_small = []                                
		for frame in self.spike_man_walk_right_images:
			# print "type of frame: ", type(frame)
			# rect = frame.get_rect()
			# print "rect widht:", rect.width
			# print "rect height: ", rect.height

			# self.spike_man_walk_right_images_small.append(pg.transform.scale(frame, (int(rect.width // 2),
			# 																		 int(rect.height // 2))))
			frame.set_colorkey(BLACK)

			# for img in self.spike_man_walk_right_images_small:
			# 	print "small img rect: ", img.get_rect()

			# rect = frame.get_rect()
			# print "after scale image new w, h"
			# print "rect widht:", rect.width
			# print "rect height: ", rect.height

		self.spike_man_walk_left_images = []
		for frame in self.spike_man_walk_right_images:
			frame.set_colorkey(BLACK)
			self.spike_man_walk_left_images.append(pg.transform.flip(frame, True, False))

	def update(self):
		self.animate_spike_man()

		# if hit status is false then we move normally 
		# if hit status is true then we ran away 

		# print "hit staus: ", self.hit_staus
		# self.rect.x += self.vx
		if not self.hit_staus:
			if self.walking_right and self.rect.left < self.plat.rect.right - 15:
				self.rect.x += self.vx
			else:
				self.walking_right = False
				self.walking_left = True

			if self.walking_left and self.rect.right > self.plat.rect.left + 15:
				self.rect.x -= self.vx
			else:
				self.walking_left = False
				self.walking_right = True			
		else:
			if self.walking_right:
				self.rect.x += 7
			else:
				self.rect.x -= 7

		if self.rect.centerx > WIDTH or self.rect.centerx < 0:
			self.kill()

	def animate_spike_man(self):
		now = pg.time.get_ticks()
		if now - self.last_update_spike_man > 100:
			self.last_update_spike_man = now
			self.current_frame_for_spike_man = (self.current_frame_for_spike_man + 1) % len(self.spike_man_walk_right_images)

			# print "animate_spike_man walking right: ", self.walking_right
			# print "animate_spike_man walking left: ", self.walking_left

			# self.image = self.spike_man_walk_right_images[self.current_frame_for_spike_man]

			if self.walking_right: # then show walking right image
				self.image = self.spike_man_walk_right_images[self.current_frame_for_spike_man]
			else: # walking left
				self.image = self.spike_man_walk_left_images[self.current_frame_for_spike_man]


class Grass(pg.sprite.Sprite):
	"""docstring for Powerup"""
	def __init__(self, game, plat):
		self._layer = GRASS_LAYER
		self.groups = game.all_sprites, game.grasses
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.plat = plat

		self.load_grass_images()

		self.image = choice(self.grass_images)
		self.rect = self.image.get_rect()
		self.rect.centerx = self.plat.rect.centerx
		self.rect.bottom = self.plat.rect.top


	def load_grass_images(self):
		self.grass_images = [self.game.spritesheet.get_image(868, 1877, 58, 57), # grass1.png 
		                     self.game.spritesheet.get_image(784, 1931, 82, 70), # grass2.png
		                     self.game.spritesheet.get_image(534, 1063, 58, 57), # grass_brown1.png
						     self.game.spritesheet.get_image(801, 752, 82, 70)]  # grass_brown2.png

		# remove black color from image
		for image in self.grass_images:
			image.set_colorkey(BLACK)

	def update(self):
 		if self.rect.top > HEIGHT:
 			self.kill()


class  Cactus(pg.sprite.Sprite):
	"""docstring for Powerup"""
	def __init__(self, game, plat):
		self._layer = GRASS_LAYER
		self.groups = game.all_sprites, game.cactuses
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.plat = plat

		self.load_cactus_images()

		self.image = choice(self.cactus_images)
		self.rect = self.image.get_rect()
		self.rect.centerx = randrange(self.plat.rect.left + 10, self.plat.rect.right - 10)
		self.rect.bottom = self.plat.rect.top - 1

	def load_cactus_images(self):
		self.cactus_images = [self.game.spritesheet.get_image(707, 134, 117, 160), 
							  self.game.spritesheet.get_image_scaled3x(707, 134, 117, 160), 
							  self.game.spritesheet.get_image_scaled4x(707, 134, 117, 160)]

		# remvoe black color form image
		for img in self.cactus_images:
			img.set_colorkey(BLACK)

	def update(self):
 		if self.rect.top > HEIGHT:
 			self.kill()

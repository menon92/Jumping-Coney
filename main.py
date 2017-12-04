# Jumpy! - platform game
# date : 16-07-2017
import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
	def __init__(self):
		# initilize game window, etc
		pg.init()
		pg.mixer.init()
		# icon must be set before display.set_mod() in Linux
		# load icon image
		self.icon_img = pg.image.load(ICON)
		pg.display.set_icon(self.icon_img)
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.running = True 
		self.font_name = pg.font.match_font(FONT_NAME)
		self.load_data()

	def load_data(self):
		# load heigh score
		self.dir = path.dirname(__file__)
		self.img_dir = path.join(self.dir, 'img')
		with open(path.join(self.dir, HS_FILE), 'w') as f:
			try:
				self.heighscore = int(f.read)
			except:
				self.heighscore = 0

		# load background image
		self.background_image = pg.image.load(path.join(self.img_dir, BG_IMAGE))
		# resize bg image according to our window width height
		self.background_image = pg.transform.scale(self.background_image, (WIDTH, HEIGHT))
		# print self.background_image.get_rect()

		# # load icon image
		# self.icon_img = pg.image.load(path.join(self.img_dir, ICON))

		# load spritesheet image
		self.spritesheet = Spritesheet(path.join(self.img_dir, SPRITESHEET))		

		# load sounds
		self.snd_dir = path.join(self.dir, 'snd')
		self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump.wav'))
		self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'boost16.wav'))
		self.coin_pickup_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Pickup_Coin.wav'))
		self.hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Hit_Hurt.wav'))
		self.hit_grass = pg.mixer.Sound(path.join(self.snd_dir, 'Hit_Hurt42.wav'))
		self.leser_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Laser_Shoot.wav'))
		# load cloud images
		self.cloud_images = []
		for i in range(1, 4):
			self.cloud_images.append(pg.image.load(path.join(self.img_dir, 'cloud{}.png'.format(i))).convert())


	def new(self):
		# start a new game
		self.score = 0
		# initilize sprite group
		# self.all_sprites = pg.sprite.Group()
		self.all_sprites = pg.sprite.LayeredUpdates()
		self.platforms = pg.sprite.Group()
		self.powerups = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.clouds = pg.sprite.Group()
		self.wingmans = pg.sprite.Group()
		self.spikemans = pg.sprite.Group()
		self.grasses = pg.sprite.Group()
		self.cactuses = pg.sprite.Group()

		# initilize a player
		# self parametter is for sending game object copy to player object
		# so that player can access the each everythong in game object
		self.player = Player(self) 
		# initilize platform
		# self.p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
		# self.p2 = Platform(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20)

		# add player to sprite group
		# self.all_sprites.add(self.player)
		# self.all_sprites.add(self.p1)
		# self.platforms.add(self.p1)

		# self.all_sprites.add(self.p2)
		# self.platforms.add(self.p2)

		for plat in PLATFORM_LIST:
			# p = Platform(*plat)
			# p = Platform(self, *plat)
			Platform(self, *plat)
			# self.all_sprites.add(p)
			# self.platforms.add(p)

		self.mob_timer = 0
		self.enime_timer = 0
		self.is_spikeman_hit_player = False

		pg.mixer.music.load(path.join(self.snd_dir, "HappyTune.ogg"))
		
		# make cloud for starting window
		for i in range(8):
			c = Cloud(self)
			c.rect.y += 500


		self.run()

	def run(self):
		# game loop
		pg.mixer.music.play(loops = -1)
		self.playing = True
		while self.playing:
			 # keep loop running at the same speed all time
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
		pg.mixer.music.fadeout(500) # stop music

	def update(self):
		# game loop - update
		self.all_sprites.update()

		# spawn an enime Wing Man? 
		now = pg.time.get_ticks()
		if now - self.enime_timer > 5000:
			self.enime_timer = now
			WingMan(self)

		# hit enime Wing Man ? 
		enime_hits = pg.sprite.spritecollide(self.player, self.wingmans, True)
		for enime in enime_hits:
			if enime.type == 'wing_man':
				self.hit_sound.play() 
			if enime_hits:
				# decrease score
				if self.score >= LOST_POINTS_BY_HIT_WINGMAN:
					self.score -= LOST_POINTS_BY_HIT_WINGMAN

		# spawn a mob ? 
		now = pg.time.get_ticks()
		if now - self.mob_timer > 8000 + random.choice([-1000, 500, 0, 500, 1000]):
			self.mob_timer = now
			Mob(self)

		# hit mobs ? 
		mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
		if mob_hits:
			self.playing = False 

		# hits spike man ?
		spikeman_hits = pg.sprite.spritecollide(self.player, self.spikemans, False)
		if spikeman_hits:
			# print "hit spikeman"
			self.leser_snd.play(loops = 5)
			# print spikeman_hits
			# self.is_spikeman_hit_player = True
			spikeman_hits[0].hit_staus = True
			if self.score >= LOST_POINTS_BY_HIT_SPIKEMAN:
				self.score -= LOST_POINTS_BY_HIT_SPIKEMAN
		else:
			# self.is_spikeman_hit_player = False
			pass

		# print "self.player.vel.y %d" % (self.player.vel.y)

		if self.player.vel.y > 0: # chekc if player hits a platform - only if falling then place it onto platform
			# print "if - self.player.vel.y %d" % (self.player.vel.y)
			# chekc collision is happend or not
			hits = pg.sprite.spritecollide(self.player, self.platforms, False) # False = don't delete platform object
			# print "hits len = ", len(hits)
			
			if hits:
				# find the lowest platform
				lowest = hits[0]
				for hit in hits:
					if hit.rect.bottom > lowest.rect.bottom:
						lowest = hit
				# chekc if we reach to edge of platform or not
				# pos set to midbottom in player class
				if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
					# chekc player is hight enouth to go to next platform
					if self.player.pos.y < lowest.rect.centery:
						# print "self.player.pos.y", self.player.pos.y
						# print "hits[0].rect.bottom", hits[0].rect.bottom
						self.player.pos.y = lowest.rect.top
						self.player.vel.y = 0
						self.player.jumping = False

		# if player reaches top 1/4 of screen then scroll window to up
		if self.player.rect.top <= HEIGHT / 4:
			# self.player.pos.y += abs(self.player.vel.y) # move player
			self.player.pos.y += max(abs(self.player.vel.y), 2) # move player

			# make cloud randomly
			if random.randrange(100) < 15:
				# print "making new cloud"
				Cloud(self)

			for cloud in self.clouds:
				cloud.rect.y += max(abs(self. player.vel.y / 2), 2)

			for mob in self.mobs:
				mob.rect.y += max(abs(self.player.vel.y), 2)

			for enime in self.wingmans:
				enime.rect.y += max(abs(self.player.vel.y), 2)

			for spikeman in self.spikemans:
				spikeman.rect.y += max(abs(self.player.vel.y), 2)

			for grass in self.grasses:
				grass.rect.y += max(abs(self.player.vel.y), 2)

			for cactus in self.cactuses:
				cactus.rect.y += max(abs(self.player.vel.y), 2)

			for plat in self.platforms:
				# plat.rect.y += abs(self.player.vel.y)
				plat.rect.y += max(abs(self.player.vel.y), 2)
				# if platform is out out screen then delete this platform
				if plat.rect.top >= HEIGHT:
					plat.kill()
					self.score += 10

		# if player hits a powerup
		power_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
		for power in power_hits:
			if power.type == 'boost':
				self.boost_sound.play()
				self.player.vel.y = -BOOST_POWER
				self.player.jumping = False
			elif power.type == 'gold':
				self.coin_pickup_sound.play()
				self.score += GOLD_POINTS
				self.player.jumping = False
			elif power.type == 'silver':
				self.coin_pickup_sound.play()
				self.score += SILVER_POINTS
				self.player.jumping = False
			elif power.type == 'bronze':
				self.coin_pickup_sound.play()
				self.score += BRONZE_POINTS
				self.player.jumping = False

		# die!
		if self.player.rect.bottom > HEIGHT:
			for sprite in self.all_sprites:
				sprite.rect.y -= max(self.player.vel.y, 10)
				if sprite.rect.bottom < 0:
					sprite.kill()
		if len(self.platforms) == 0:
			self.playing = False


		# spawn new platforms to keep same avarage number
		while len(self.platforms) < 10:
			width = random.randrange(50, 100)
			# p = Platform(random.randrange(0, WIDTH - width), 
			# 			 random.randrange(-75, -30), 
			# 			 width, 20)
			p = Platform(self, random.randrange(0, WIDTH - width), 
						 random.randrange(-75, -30))
			# self.platforms.add(p)
			# self.all_sprites.add(p)

	def events(self):
		# game loop - events
		# process input (events)
		for event in pg.event.get():
			# check for closing window
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN: 
				if event.key == pg.K_SPACE:
					self.player.jump()
			if event.type == pg.KEYUP:
				if event.key == pg.K_SPACE:
					self.player.jump_cut

	def draw(self):
		# game loop - draw
		# self.screen.fill(BGCOLOR)
		self.screen.blit(self.background_image, (0, 0))
		self.all_sprites.draw (self.screen)
		# dwaw player into the screen at position player.rect
		# 	self.screen.blit(self.player.image, self.player.rect)
		self.draw_text("score: " +  str(self.score), 22, RED, WIDTH / 2, 15)
		pg.display.flip()

	def show_start_screen(self):
		# game splash/start screen
		pg.mixer.music.load(path.join(self.snd_dir, "Yippee.ogg"))
		pg.mixer.music.play()

		self.screen.fill(BGCOLOR)
		self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
		self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2 - 30)
		self.draw_text("> If you hit GRASS or CACTUS you loss 1 point", 15, WHITE, WIDTH - 440, (HEIGHT / 2) + 35)
		self.draw_text("> If you hit SPIKEMAN you loss 2 points", 15, WHITE, WIDTH - 465 , (HEIGHT / 2) + 65)
		self.draw_text("> If you hit FLYMAN you loss 20 points", 15, WHITE, WIDTH - 470, (HEIGHT / 2) + 95)
		self.draw_text("> If you hit MOB you die!", 15, RED, WIDTH - 500, (HEIGHT / 2) + 125)

		self.draw_text("> GOLD, SILVER, BRONZE give you 100, 50, 25 points", 15, WHITE, WIDTH - 414, (HEIGHT / 2) + 155)

		self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 30)
		self.draw_text("Heigh Score: " + str(self.heighscore), 22, WHITE, WIDTH / 2, 15)
		pg.display.flip()
		self.wait_for_key()

		pg.mixer.fadeout(500)

	def show_go_screen(self):
		# game over/continue
		pg.mixer.music.load(path.join(self.snd_dir, "game-over.wav"))
		pg.mixer.music.play()

		if not self.running:
			return
		self.screen.fill(BGCOLOR)
		self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
		self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
		self.draw_text("Press any key to play agin :)", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)

		# update high score
		if self.score > self.heighscore: 
			self.heighscore = self.score
			self.draw_text("NEW HEIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
			with open(path.join(self.dir, HS_FILE), 'w') as f:
				f.write(str(self.heighscore))
		else:
			self.draw_text("High Score: " + str(self.heighscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

		pg.display.flip()
		self.wait_for_key()

		pg.mixer.fadeout(500)

	def wait_for_key(self):
		waitting = True
		while waitting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waitting = False
					self.running = False
				if event.type == pg.KEYUP: # KEYUP = any key in keyboard
					waitting = False

	def draw_text(self, text, size, color, x, y):
		font = pg.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)


def main():
	game = Game()
	game.show_start_screen()
	while game.running:
		game.new()
		game.show_go_screen()

	pg.quit()


if __name__ == '__main__':
	main()


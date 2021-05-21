import pygame
import random
import sys, os
# import pdbg
from assets import colors
from pygame.locals import *
# from rect import * 

pygame.init()
pygame.font.init()

# setting up window
width = 500
height = 500
gameScreen = pygame.display.set_mode((width, height))
gameIcon = pygame.image.load(os.path.join('assets', 'snake.png'))
pygame.display.set_caption("Snake Game")
pygame.display.set_icon(gameIcon)

# run = True


# snake object
# Rect object: Rect(x, y, width, height)
class Snake():
	def __init__(self, x, y, width, height):
		self.list = []
		self.rect = Rect(x, y, width, height)

	def draw(self, gameScreen, block_size):
		for XnY in self.list:
			self.rect = Rect(XnY[0], XnY[1], block_size, block_size)
			pygame.draw.rect(gameScreen, colors.BLACK, self.rect)

# food object
class Food():
	def __init__(self, x, y, width, height):
		self.rect = Rect(x, y, width, height)
		# self.collide = False

	def draw(self, gameScreen):
		pygame.draw.rect(gameScreen, colors.YELLOW, self.rect)

	def check_collision(self, snake):
		return self.rect.colliderect(snake)
		 

def play_again():
	playAgainFont = pygame.font.SysFont('comicsans', 20, bold=True)
	playAgain = True

	while playAgain:
		gameScreen.fill((240, 200, 200))
		playAgainLabel = playAgainFont.render('Press Space to play again...', 1, colors.BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playAgain = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					main()

		gameScreen.blit(playAgainLabel, ((width / 2 - playAgainLabel.get_width() / 2), (height / 2 - playAgainLabel.get_height() / 2)))
		pygame.display.update()
	pygame.quit()

def welcome():
	exitGame = False
	welcomeFont = pygame.font.SysFont('comicsans', 20, bold=True)
	enterFont = pygame.font.SysFont('comicsans', 20, bold=True)

	while not exitGame:
		gameScreen.fill((240, 200, 200))
		welcomeLabel = welcomeFont.render("Welcome to Snake Game!", 1, colors.BLACK)
		enterLabel = enterFont.render("Press Space to play...", 1, colors.BLACK)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exitGame = True
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					main()

		gameScreen.blit(welcomeLabel, ((width / 2 - welcomeLabel.get_width() / 2), (height / 2 - welcomeLabel.get_height() / 2)))
		gameScreen.blit(enterLabel, ((width / 2 - enterLabel.get_width() / 2), 300))
		pygame.display.update()


# main function
def main():
	clock = pygame.time.Clock()
	FPS = 15
	run = True
	block_size = 10
	snake = Snake(random.randint(0, 400), random.randint(0, 400), block_size, block_size)
	food = Food(random.randint(0, 400), random.randint(0, 400), block_size, block_size)
	lengthOfSnake = 1
	snakeVelocity_X = 0
	snakeVelocity_Y = 0
	lost = False
	score = 0
	lostCount = 0

	#font
	scoreFont = pygame.font.SysFont('Courier', 20, bold=True)
	lostFont = pygame.font.SysFont('Courier', 50, bold=True)

	# utility function to keep code clean
	def redraw():
		gameScreen.fill(colors.GRAY)

		# label(s)
		scoreLabel = scoreFont.render(f"Score: {score}" , 1, colors.WHITE)
		lostLabel = lostFont.render("You Lost!", 1, colors.RED)

		# redraw surface(s)
		snake.draw(gameScreen, block_size)
		food.draw(gameScreen)
		gameScreen.blit(scoreLabel, (10, 10))

		if lost: 
			gameScreen.blit(lostLabel, ((width / 2 - lostLabel.get_width() / 2), (height / 2 - lostLabel.get_height() / 2)))

		pygame.display.update()


	# game loop 
	while run:
		# running the loop at 15FPS
		clock.tick(FPS)

		if lost:
			lostCount += 1
			if lostCount > FPS * 3:
				run = False
				play_again()
			else:
				continue

		for event in pygame.event.get():
			# moving the snake
			if event.type == pygame.KEYDOWN:
				if event.key == K_LEFT:
					snakeVelocity_X = -5
					snakeVelocity_Y = 0
					# print("left arrow pressed.")
				elif event.key == K_RIGHT:
					snakeVelocity_X = 5
					snakeVelocity_Y = 0
				elif event.key == K_UP:
					snakeVelocity_Y = -5
					snakeVelocity_X = 0
				elif event.key == K_DOWN:
					snakeVelocity_Y = 5
					snakeVelocity_X = 0

			# checking if 'x' button is pressed
			if event.type == pygame.QUIT:
				run = False

		# boundary conditions and coordinate update
		if (snake.rect.x <= 0 or snake.rect.x + snake.rect.width > width ) or (snake.rect.y <= 0 or snake.rect.y + snake.rect.height > height):
			lost = True
		else:
			snake.rect.x += snakeVelocity_X
			snake.rect.y += snakeVelocity_Y

		snakeHead = []
		snakeHead.append(snake.rect.x)
		snakeHead.append(snake.rect.y)
		snake.list.append(snakeHead)
		if len(snake.list) > lengthOfSnake:
			del snake.list[0]

		for block in snake.list[:-1]:
			if block == snakeHead:
				lost = True
				

		# print("head: " + str(snakeHead))
		# print("list: " + str(snake.list))

		# snake.add_snake_block()
		if food.check_collision(snake):
			del food
			food = Food(random.randint(0, 400), random.randint(0, 400), block_size, block_size)
			score += 1
			lengthOfSnake += 1

		redraw()
	pygame.quit()

if __name__ == '__main__':
	welcome()

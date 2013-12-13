#!/usr/bin/env python

# adxl345 accelerometer example program v0.2
# Russell Barnes - 12 Dec 2013 for Linux User magazine issue 135
# www.linuxuser.co.uk

import pygame
from adxl345 import ADXL345

adxl345 = ADXL345() # Initialise the accelerometer
pygame.init() # Initialise Pygame

# Create a screen of 800x600 resolution
screen = pygame.display.set_mode([800, 600])

# Name the game window, set the mouse visibility and start an FPS clock
pygame.display.set_caption('ADXL345 Space Test - Press ESC to quit')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# Load the images we're using from http://opengameart.org/users/rawdanitsu   
background_image = pygame.image.load("Space-Background-4_0.jpg").convert()
player_image = pygame.image.load("ship0.png").convert()

# We can use colour key method to remove the background from the ship
player_image.set_colorkey([0, 0, 0])

player_position = [450, 350] # Initial starting point of the ship
game_over = False # Global variable to decide if the game should end

def update_pos():
	""" Poll the adxl345 and update player pos based on readings"""
	move_data = adxl345.getAxes(True) # Returns a dict of axes results
	if move_data['x'] < -0.1 or move_data['x'] > 0.1:
		player_position[0] += move_data['x'] * 20
	if move_data['y'] < -0.1 or move_data['y'] > 0.1:
		player_position[1] += move_data['y'] * 20

def check_pos():
	""" Check player pos to make it 
	wrap-around the game window"""
	if player_position[0] > 850:
		player_position[0] = -75
	elif player_position[0] < -75:
		player_position[0] = 850
	
	if player_position[1] > 650:
		player_position[1] = -75
	elif player_position[1] < -75:
		player_position[1] = 650

###### MAIN LOOP ######
while not game_over: # Handle control events while the game is in play
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			game_over = True # Quit if close button is pressed
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: 
				game_over = True # Quit if escape key is pressed

	update_pos() # Update the players' position
	check_pos() # Check the players' position

    # Update the background then the players' position on the screen
	screen.blit(background_image, [0, 0])
	screen.blit(player_image, [player_position[0],player_position[1]])
	
	pygame.display.flip() # Refresh the screen
 	clock.tick(20) # Force frame-rate to desired number
     
pygame.quit () # Game quits gracefully when 'game_over' turns True

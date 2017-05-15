# -*- coding: utf-8 -*-
"""
Created on Sat May 13 16:41:44 2017

@author: Justin Kleiber
"""
import pygame
import random
from Cobra import Cobra
from Block import Block
from Wall import Wall
from time import sleep

#initialize pygame
pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 145, 34)
WHITE = (255, 255, 255)

#Are we running this from the Console or from Spyder?
CONSOLE = False

screen_size = (0, 0)

if CONSOLE:
    screen_size = (1200, 720)
    Block.block_size = 20
else:
    screen_size = (3000, 1800)

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake")

#set game running state
playing = True
begin = False

#setup the clock
clock = pygame.time.Clock()

#Create the wall
wall = Wall(screen_size[0], screen_size[1])

#Create the snake
cobra = Cobra(200, 300)

#create the food block and mae it regenerate itself in a real position
food_block = Block(-Block.block_size, -Block.block_size)
food_ready = False

#Set the direction of the snake
#0: up, 1: right, 2: down, 3: left
SNAKE_DIRECTION = 1

#initialize random number generator
random.seed()

#place a block randomly on the board, but not on the snake
def cook_food():
    food_cooked = False
    block_on_snake = False
    x = 0
    y = 0
    
    while not food_cooked:
        #get row and column for where the food block should go. Avoid wall
        col = random.randint(1, (screen_size[0] / Block.block_size) - 2)
        row = random.randint(1, (screen_size[1] / Block.block_size) - 2)
        
        #convert to pixel units
        x = col * Block.block_size
        y = row * Block.block_size
        
        #reinitialize so we dont get stuck
        block_on_snake = False
        
        for block in cobra.blocks:
            if block.x == x and block.y == y:
                block_on_snake = True
                break
        
        food_cooked = not block_on_snake
    
    #change block loaction
    food_block.set_x(x)
    food_block.set_y(y)

#Game Logic Function
def game_logic():
    global begin
    global SNAKE_DIRECTION
    global food_ready
    
    if begin:
        cobra.move_snake(SNAKE_DIRECTION)
        
        #generate a new block for the snake to eat if no such block exists yet
        if not food_ready:
            cook_food()
            food_ready = True
        
        #check to see if the snake left the screen (game over condition)
        #if off the left of the screen
        if cobra.x < Block.block_size:
            begin = False
        #if off the right of the screen
        if cobra.x > screen_size[0] - (2 * Block.block_size):
            begin = False
        #if off the top of the screen
        if cobra.y < Block.block_size:
            begin = False
        #if off the bottom of the screen
        if cobra.y > screen_size[1] - (2 * Block.block_size):
            begin = False
            
        #check to see if the snake ate itself (game over condition)
        
        #check to see if the snake ate a food block (add block to snake)
        if cobra.x == food_block.x and cobra.y == food_block.y:
            cobra.add_block()
            food_ready = False  
        
    else:
        #reset the snake's position and number of blocks
        cobra.reset()
        
        #set default direction to go right
        SNAKE_DIRECTION = 1
        
#Drawing function
def drawing():
    cobra.draw(screen, RED)
    food_block.draw(screen, BLUE)
    wall.draw(screen, DARK_GREEN)

# GAME LOOP
while playing:
    
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not SNAKE_DIRECTION == 2:
                    SNAKE_DIRECTION = 0
            elif event.key == pygame.K_RIGHT:
                if not SNAKE_DIRECTION == 3:
                    SNAKE_DIRECTION = 1
            elif event.key == pygame.K_DOWN:
                if not SNAKE_DIRECTION == 0:
                    SNAKE_DIRECTION = 2
            elif event.key == pygame.K_LEFT:
                if not SNAKE_DIRECTION == 1:
                    SNAKE_DIRECTION = 3
            elif event.key == pygame.K_RETURN:
                begin = True
            elif event.key == pygame.K_q:
                playing = False
    
    #Game Logic
    game_logic()
    
    #Clear display
    screen.fill(WHITE)
    
    #Drawings
    drawing()
    
    #Update display
    pygame.display.flip()
    
    #limit to 15 frames per second
    clock.tick(10)
    
#end the game
pygame.display.quit()
pygame.quit()
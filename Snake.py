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
from enum import Enum

#initialize pygame
pygame.init()

#Normal
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 145, 34)
WHITE = (255, 255, 255)

#Retro
RETRO_GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#Color Themes
class Themes(Enum):
    NORMAL = 0
    RETRO = 1

#Theme tracker 
theme = Themes.NORMAL

#Are we running this from the Console or from Spyder?
CONSOLE = False

screen_size = (0, 0)

if CONSOLE:
    screen_size = (1200, 720)
    Block.block_size = 20
else:
    screen_size = (3000, 1800)

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake | Press Enter To Begin... | Press Q to quit")

#set game running state
playing = True

#Game State Enum
class GameState(Enum):
    START = 0
    PLAYING = 1
    GAME_OVER = 2

#keep track of state
game_state = GameState.START

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
    global game_state
    global SNAKE_DIRECTION
    global food_ready
    
    if game_state == GameState.PLAYING:
        cobra.move_snake(SNAKE_DIRECTION)
        
        #generate a new block for the snake to eat if no such block exists yet
        if not food_ready:
            cook_food()
            food_ready = True
        
        #check to see if the snake left the screen (game over condition)
        #if off the left of the screen
        if cobra.x < Block.block_size:
            game_state = GameState.GAME_OVER
        #if off the right of the screen
        if cobra.x > screen_size[0] - (2 * Block.block_size):
            game_state = GameState.GAME_OVER
        #if off the top of the screen
        if cobra.y < Block.block_size:
            game_state = GameState.GAME_OVER
        #if off the bottom of the screen
        if cobra.y > screen_size[1] - (2 * Block.block_size):
            game_state = GameState.GAME_OVER
            
        #check to see if the snake ate itself (game over condition)
        if cobra.check_snakicide():
            game_state = GameState.GAME_OVER
        
        #check to see if the snake ate a food block (add block to snake)
        if cobra.x == food_block.x and cobra.y == food_block.y:
            cobra.add_block()
            food_ready = False
            
        #Show Current Score
        pygame.display.set_caption("Snake | Score: " + str(cobra.get_score()))
        
    elif game_state == GameState.GAME_OVER:
        pygame.display.set_caption("Snake | Final Score: " 
                                   + str(cobra.get_score()) 
                                   + " | Press S to set up new game, Q to Quit")
        
    else:
        #reset the snake's position and number of blocks
        cobra.reset()
        
        #set default direction to go right
        SNAKE_DIRECTION = 1
        
        #Tell user to press enter to begin
        pygame.display.set_caption("Snake | Press Enter To Begin... | Press Q to quit")
        
#Drawing function
def drawing():
    if theme == Themes.NORMAL:
        cobra.draw(screen, RED)
        food_block.draw(screen, BLUE)
        wall.draw(screen, DARK_GREEN)
    elif theme == Themes.RETRO:
        cobra.draw(screen, RETRO_GREEN)
        food_block.draw(screen, RETRO_GREEN)
        wall.draw(screen, RETRO_GREEN)

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
                    break #we only care about one directional key event
            elif event.key == pygame.K_RIGHT:
                if not SNAKE_DIRECTION == 3:
                    SNAKE_DIRECTION = 1
                    break #we only care about one directional key event
            elif event.key == pygame.K_DOWN:
                if not SNAKE_DIRECTION == 0:
                    SNAKE_DIRECTION = 2
                    break #we only care about one directional key event
            elif event.key == pygame.K_LEFT:
                if not SNAKE_DIRECTION == 1:
                    SNAKE_DIRECTION = 3
                    break #we only care about one directional key event
            elif event.key == pygame.K_RETURN:
                if game_state == GameState.START:
                    game_state = GameState.PLAYING
            elif event.key == pygame.K_q:
                playing = False
            elif event.key == pygame.K_r:
                theme = Themes.RETRO
            elif event.key == pygame.K_n:
                theme = Themes.NORMAL
            elif event.key == pygame.K_s:
                game_state = GameState.START
            
    
    #Game Logic
    game_logic()
    
    #Clear display
    if theme == Themes.NORMAL:
        screen.fill(WHITE)
    elif theme == Themes.RETRO:
        screen.fill(BLACK)
    
    #Drawings
    drawing()
    
    #Update display
    pygame.display.flip()
    
    #limit to 15 frames per second
    clock.tick(10)
    
#end the game
pygame.display.quit()
pygame.quit()
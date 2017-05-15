# -*- coding: utf-8 -*-
"""
Created on Sun May 14 16:15:39 2017

@author: jklei
"""
import pygame

class Block:
    
    block_size = 50
    
    def __init__(self, x, y):
        self.queue = []
        self.x = x
        self.y = y
        
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, [self.x, self.y, Block.block_size, Block.block_size])
        
    #0: up, 1: right, 2: down, 3: left
    def add_move(self, id):
        self.queue.append(id)
        
    def move(self):
        direction = self.queue.pop(0)
        
        #0: up, 1: right, 2: down, 3: left
        if direction == 0:
            self.y = self.y - Block.block_size
        elif direction == 1:
            self.x = self.x + Block.block_size
        elif direction == 2:
            self.y = self.y + Block.block_size
        elif direction == 3:
            self.x = self.x - Block.block_size
            
    def set_x(self, x):
        self.x = x
        
    def set_y(self, y):
        self.y = y
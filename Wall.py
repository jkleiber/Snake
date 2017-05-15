# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:30:32 2017

@author: jklei
"""
import pygame
from Block import Block

class Wall:
    
    def __init__(self, width, height):
        self.wall_list = []
        
        #figure out how many blocks we need for the 2 different lengths
        w_blocks = width / Block.block_size
        h_blocks = height / Block.block_size
        
        #Create and add the top and bottom wall
        for i in range(0, w_blocks):
            self.wall_list.append(Block(i * Block.block_size, 0))
            self.wall_list.append(Block(i * Block.block_size, height - Block.block_size))
        
        #Create and add the left and right wall
        for i in range(0, h_blocks):
            self.wall_list.append(Block(0, i * Block.block_size))
            self.wall_list.append(Block(width - Block.block_size, i * Block.block_size))
            
    def draw(self, screen, color):
        for block in self.wall_list:
            block.draw(screen, color)
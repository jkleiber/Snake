# -*- coding: utf-8 -*-
"""
Created on Sun May 14 16:13:46 2017

@author: jklei
"""
from Block import Block

class Cobra:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.start_x = x
        self.start_y = y
        
        #Snake body manager
        self.blocks = []
        
        #Create the snake's body
        self.blocks.append(Block(self.x, self.y))
        self.blocks.append(Block(self.x-20, self.y))
        self.blocks.append(Block(self.x-40, self.y))
        
        #start by going right
        self.blocks[0].add_move(1)
        
        #add offset for block 2 (id = 1)
        self.blocks[1].add_move(1)
        self.blocks[1].add_move(1)
        
        #add offset for block 3 (id = 2)
        self.blocks[2].add_move(1)
        self.blocks[2].add_move(1)
        self.blocks[2].add_move(1)
        
    def draw(self, screen, color):
        for block in self.blocks:
            block.draw(screen, color)
            
    def move_snake(self, direction):
        #0: up, 1: right, 2: down, 3: left
        
        #add the current direction to each block's queue and move the block
        for i in range (0,len(self.blocks)):
                self.blocks[i].add_move(direction)
                self.blocks[i].move()
        
        #update the coordinates of the cobra
        self.x = self.blocks[0].x
        self.y = self.blocks[0].y
                            
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        
        #Snake body manager
        self.blocks = []
        
        #Create the snake's body
        self.blocks.append(Block(self.x, self.y))
        self.blocks.append(Block(self.x - Block.block_size, self.y))
        self.blocks.append(Block(self.x - (2 * Block.block_size), self.y))
        
        #start by going right
        self.blocks[0].add_move(1)
        
        #add offset for block 2 (id = 1)
        self.blocks[1].add_move(1)
        self.blocks[1].add_move(1)
        
        #add offset for block 3 (id = 2)
        self.blocks[2].add_move(1)
        self.blocks[2].add_move(1)
        self.blocks[2].add_move(1)
        
    def add_block(self):
        last_block = self.blocks[len(self.blocks)-1]
        
        #check to see which way the back end of the snake is going so we can
        #add the new block tangent to the last one
        if last_block.queue[0] == 0:      #up
            #so put the new block below
            new_block = Block(last_block.x, last_block.y + Block.block_size)
            new_block.queue.append(0)
        elif last_block.queue[0] == 1:    #right
            #so put the new block to the left
            new_block = Block(last_block.x - Block.block_size, last_block.y)
            new_block.queue.append(1)
        elif last_block.queue[0] == 2:    #down
            #so put the new block above
            new_block = Block(last_block.x, last_block.y - Block.block_size)
            new_block.queue.append(2)
        elif last_block.queue[0] == 3:    #left
            #so put the new block to the right
            new_block = Block(last_block.x + Block.block_size, last_block.y)
            new_block.queue.append(3)
        
        #follow the last block in the chain
        new_block.queue.extend(last_block.queue)
        
        self.blocks.append(new_block)
        
    def get_score(self):
        return len(self.blocks)
    
    #Has the snake eaten itself?
    def check_snakicide(self):
        for i in range(1, len(self.blocks)):
            if self.blocks[0].x == self.blocks[i].x:
                if self.blocks[0].y == self.blocks[i].y:
                    return True
        return False
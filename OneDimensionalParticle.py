import pygame
import random 
from global_variables import one_dimensional_possible_directions

class OneDimensionalParticle:
    
    def __init__(self, x:int, v:int, dot_size:int, positions_array, screen):
    
        self.x = x
        self.height = 60 # fixed could change later
        self.v = v
        self.dot_size = dot_size
        self.positions_array = positions_array
        self.screen = screen
        
        # Keep track for when I update
        self.previous_x = x
    
    # def clear_old_position(self):
    #     background_color = (0, 0, 0) # Black
    #     pygame.draw.rect(self.screen, background_color, pygame.Rect(self.previous_x * self.dot_size,
    #                                                                 self.height * self.dot_size,
    #                                                                 self.dot_size, self.dot_size))

    # def draw(self, screen, color=(255, 255, 255)):
    #     pygame.draw.rect(screen, color, pygame.Rect(self.x * self.dot_size,
    #                                                 self.height * self.dot_size,
    #                                                 self.dot_size, self.dot_size))
        
    def update_particle(self, delta):
        self.previous_x = self.x

        # probability to change direction
        if random.random() < delta:
            self.v = random.choice(one_dimensional_possible_directions) # including the one it already had

        # Move the particle, whichever way it's going
        new_x = (self.x + self.v) % len(self.positions_array) # make sure len(self.positions_array) works

        # Making the necessary updates to the self.positions_array
        if self.positions_array[new_x] == 0: # move to new place only if the new place is empty
            self.positions_array[self.x] = 0 # clear old position
            self.x = new_x
            self.positions_array[self.x] = 1 # Update board with new position


        # Drawing stuff 
        # self.clear_old_position() # only draws a black rectangle, doesn't update board, I do it above
        # self.draw(self.screen)

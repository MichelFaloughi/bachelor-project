import pygame
import random 
from global_variables import one_dimensional_possible_directions

class OneDimensionalParticle:
    
    def __init__(self, x:int, v:int, active:bool, dot_size:int, positions_array, screen):
    
        self.x = x
        self.height = 60 # fixed could change later
        self.v = v
        self.active = active
        self.dot_size = dot_size
        self.positions_array = positions_array
        self.screen = screen
        
        # Keep track for when I update
        self.previous_x = x


        
    def update_particle(self, delta, epsilon):
        self.previous_x = self.x

        # When the particle is NOT active
        if self.active == False:
            random_direction = random.choice(one_dimensional_possible_directions) # just choosing -1 or 1
            new_x = (self.x + random_direction) % len(self.positions_array)
        
        
        else: # if is IS active
            # probability to change direction
            if random.random() < delta:
                self.v = random.choice(one_dimensional_possible_directions) # including the one it already had

            if random.random() < epsilon:
                # Move the particle, whichever way it's going
                new_x = (self.x + self.v) % len(self.positions_array) # make sure len(self.positions_array) works
            else:
                # do the same thing we would do if we were not active
                random_direction = random.choice(one_dimensional_possible_directions) # just choosing -1 or 1
                new_x = (self.x + random_direction) % len(self.positions_array)
        
        # Making the necessary updates to the self.positions_array
        if self.positions_array[new_x] == 0: # move to new place only if the new place is empty
            self.positions_array[self.x] = 0 # clear old position
            self.positions_array[new_x] = 1 # Update board with new position
            self.x = new_x

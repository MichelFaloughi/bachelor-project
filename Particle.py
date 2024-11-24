# This class is meant to represent one particle in our particle system
import pygame
import random
from global_variables import global_possible_directions


class Particle:
    def __init__(self, x_position: int, y_position: int, velocity_vector: list, active: bool,  dot_size, board, screen):
        
        assert velocity_vector is None or len(velocity_vector) == 2, "Velocity vector should have 2 components"

        # Position, velocity, and drawing properties
        self.x = x_position
        self.y = y_position
        self.v = velocity_vector
        self.active = active
        self.size = dot_size
        self.board = board
        self.screen = screen

        # Track previous position for clearing
        self.previous_x = x_position
        self.previous_y = y_position

        # Place the particle on the board
        self.board[self.x, self.y] = 1




    def update_particle(self, delta, epsilon):
        """Update particle position based on random movement probability `delta`."""
        # Store the current position as the previous position
        self.previous_x, self.previous_y = self.x, self.y


        if self.active == False: # if the particle is not an active particle, assume epsilon = 1
            # (ie particle will always randomly move, not sure if that epsilon = 1 or 0 actually, too lazy to check)
            random_direction = random.choice(global_possible_directions)
            new_x = (self.x + random_direction[0]) % self.board.shape[0]
            new_y = (self.y + random_direction[1]) % self.board.shape[1]

        else: # if it is an active particle
            if random.random() < delta:  # Change direction randomly
                self.v = random.choice(global_possible_directions)
            
            if random.random() < epsilon: # business as usual 
                # Calculate new position with wrapping around edges
                new_x = (self.x + self.v[0]) % self.board.shape[0]
                new_y = (self.y + self.v[1]) % self.board.shape[1]
            else: 
                # That is not assigned to the particle, its like a temp direction
                random_direction = random.choice(global_possible_directions)
                new_x = (self.x + random_direction[0]) % self.board.shape[0]
                new_y = (self.y + random_direction[1]) % self.board.shape[1]



        # Move only if new position is empty
        if self.board[new_x, new_y] == 0:
            self.board[self.x, self.y] = 0  # Clear old position
            self.x, self.y = new_x, new_y
            self.board[self.x, self.y] = 1  # Update board with new position

        # Redraw particle
        self.clear_old_position()
        self.draw(self.screen)






    def clear_old_position(self):
        """Clear the previous position by drawing over it with the background color."""
        background_color = (0, 0, 0)  # Black background
        pygame.draw.rect(self.screen, background_color, pygame.Rect(self.previous_x * self.size,
                                                                    self.previous_y * self.size, 
                                                                    self.size, self.size))

    def draw(self, screen, color=(255, 255, 255)):
        """Draw the particle at the current position."""
        pygame.draw.rect(screen, color, pygame.Rect(self.x * self.size,
                                                    self.y * self.size, 
                                                    self.size, self.size))













# if I screw up, this is how the update function looked like:
#     def update_particle(self, delta, epsilon):
#         """Update particle position based on random movement probability `delta`."""
#         # Store the current position as the previous position
#         self.previous_x, self.previous_y = self.x, self.y
        
#         if random.random() < delta:  # Change direction randomly
#             self.v = random.choice(global_possible_directions)
        
#         if random.random() < epsilon: # business as usual 
#             # Calculate new position with wrapping around edges
#             new_x = (self.x + self.v[0]) % self.board.shape[0]
#             new_y = (self.y + self.v[1]) % self.board.shape[1]
#         else: 
#             # That is not assigned to the particle, its like a temp direction
#             random_direction = random.choice(global_possible_directions)
#             new_x = (self.x + random_direction[0]) % self.board.shape[0]
#             new_y = (self.y + random_direction[1]) % self.board.shape[1]



#         # Move only if new position is empty
#         if self.board[new_x, new_y] == 0:
#             self.board[self.x, self.y] = 0  # Clear old position
#             self.x, self.y = new_x, new_y
#             self.board[self.x, self.y] = 1  # Update board with new position

#         # Redraw particle
#         self.clear_old_position()
#         self.draw(self.screen)


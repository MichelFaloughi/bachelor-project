# This class is meant to represent a Particle object in our particle system
import pygame

class Particle:

    def __init__( self, x_position:int, y_position:int, velocity_vector:list, board):
        
        assert len(velocity_vector) == 2, 'Problem with the velocity vector'

        self.x = x_position
        self.y = y_position
        self.v = velocity_vector
        self.board = board

        self.image = pygame.image.load('white_dot.png')
        # For icons, a useful link is https://www.flaticon.com/search?word=acrade%20space

        self.board[self.x, self.y] = 1


    def update_position(self):
        new_x = (self.x + self.v[0]) % self.board.shape[0]  # Wrap horizontally
        new_y = (self.y + self.v[1]) % self.board.shape[1]  # Wrap vertically

        # Only move if the new position is empty
        if self.board[new_x, new_y] == 0:
            self.board[self.x, self.y] = 0  # Clear the old position
            self.x, self.y = new_x, new_y
            self.board[self.x, self.y] = 1  # Update the board with new position


    def update_velocity(self, new_velocity):
        self.v = new_velocity

    def draw(self, screen):
        screen.blit(self.image, (max(0, int(self.x)), max(0, int(self.y))))

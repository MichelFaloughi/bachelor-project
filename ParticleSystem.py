# This class is meant to represent our Worl (our Taurus) where the Particle System lives
# from Particle import Particle
from global_variables import global_possible_directions
import pygame
import random
import numpy as np

class ParticleSystem:

    def __init__( self, width:int, height:int, delta:float, mu:float, 
            world_title:str='Interactive Particle System', icon_file_path:str='kcl.png' ):
        
        assert mu > 0 and mu < 1 and delta > 0 and delta < 1

        self.width = width
        self.height = height
        self.delta = delta # probability to change direction
        self.mu = mu # probability to spawn
        
        
        self.board = np.zeros((self.width, self.height), dtype=int)
        self.possible_directions = global_possible_directions
        
        self.particles = self.generate_random_particles()
        self.num_particles = len(self.particles)

        self.world_title = world_title
        self.icon = pygame.image.load(icon_file_path)
        self.screen = pygame.display.set_mode((self.width, self.height))


    ############################
    ## Running the Simulation ##
    ############################
    

    def draw_board(self): 
        for particle in self.particles:
            particle.draw(self.screen)
    
    def draw_tile(self, x, y, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(x,y))

    def generate_random_particles(self) -> list:
        return_list = []

        for y in range(self.height):
            for x in range(self.width):
                num = random.random() # random number between 0 and 1
                v = random.choice(self.possible_directions)

                if num < self.mu:
                    self.board[x, y] = 1  # Set particle on the board
                    return_list.append(Particle(x, y, v, self.board))  # Create particle
                        
        return return_list










    def run_simulation(self):
        pygame.init()

        # Game Loop
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Pick a particle uniformly at random, we can show that we 
            # are fairly confident that no particle will be left out
            p = random.choice(self.particles)
            p.update_particle(self.delta)

            self.draw_board()  # Draw all particles after updating their positions
            pygame.display.update()  # Update the display




# This class is meant to represent a Particle object in our particle system
import pygame

class Particle:

    def __init__(self, x_position:int, y_position:int, velocity_vector:list, board):
        
        assert len(velocity_vector) == 2, 'Problem with the velocity vector'

        self.x = x_position
        self.y = y_position
        self.v = velocity_vector
        self.board = board

        self.image = pygame.image.load('white_dot.png')
        # For icons, a useful link is https://www.flaticon.com/search?word=acrade%20space

        self.board[self.x, self.y] = 1



    # pick a particle at random before calling this
    def update_particle(self, delta):
        
        assert delta < 1 and delta > 0
        num = random.random() # random number between 0 and 1

        if num < delta: # change direction/velocity, possible to re-pick current direction
            
            self.v = random.choice(global_possible_directions)
            # we don't move ! only chance velocity

        else:
            # Move the particle by one amount of its velocity
            new_x = (self.x + self.v[0]) % self.board.shape[0]  # Wrap horizontally
            new_y = (self.y + self.v[1]) % self.board.shape[1]  # Wrap vertically

            # Only move if the new position is empty
            if self.board[new_x, new_y] == 0:
                self.board[self.x, self.y] = 0  # Clear the old position
                self.x, self.y = new_x, new_y
                self.board[self.x, self.y] = 1  # Update the board with new position


    def draw(self, screen):
        screen.blit(self.image, (max(0, int(self.x)), max(0, int(self.y))))





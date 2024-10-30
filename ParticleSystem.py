# This class is meant to represent our Worl (our Taurus) where the Particle System lives
from global_variables import global_possible_directions
import pygame
import random
import numpy as np

class ParticleSystem:

    def __init__( self, width:int, height:int, delta:float, mu:float, dot_size:int, 
            world_title:str='Interactive Particle System', icon_file_path:str='kcl.png' ):
        
        assert mu > 0 and mu < 1 and delta > 0 and delta < 1

        self.width = width
        self.height = height
        self.delta = delta # probability to change direction
        self.mu = mu # probability to spawn, also known as density 
        self.dot_size = dot_size
        self.num_iterations = self.width * self.height ** 2
        
        self.refresh_rate = mu * width * height 
        # self.refresh_rate = 1
        self.num_updates = 0


        self.board = np.zeros((self.width, self.height), dtype=int)
        self.possible_directions = global_possible_directions
        
        self.particles = self.generate_random_particles()
        self.num_particles = len(self.particles)

        self.world_title = world_title
        self.icon = pygame.image.load(icon_file_path)

        self.screen = pygame.display.set_mode((self.width * self.dot_size,
                                                self.height * self.dot_size
                                                ))
    
    def draw_board(self): 
        for particle in self.particles:
            particle.draw(self.screen)

    def generate_random_particles_square_start(self) -> list:
        return_list = []

        half_width = self.width // 2
        half_height = self.height // 2

        width_possible_values = range(half_width - 7, half_width + 7)
        height_possible_values = range(half_height - 7, half_height + 7)


        for y in range(self.height):
            for x in range(self.width):

                if x in width_possible_values and y in height_possible_values:
                    num = 0

                else:
                    num = random.random() # random number between 0 and 1
                
                
                v = random.choice(self.possible_directions)

                if num < self.mu:
                    self.board[x, y] = 1  # Set particle on the board
                    return_list.append(Particle(x, y, v, self.dot_size, self.board))  # Create particle
                        
        return return_list
    
    def generate_random_particles(self) -> list:
        return_list = []

        for y in range(self.height):
            for x in range(self.width):
                num = random.random() # random number between 0 and 1
                v = random.choice(self.possible_directions)

                if num < self.mu:
                    self.board[x, y] = 1  # Set particle on the board
                    return_list.append(Particle(x, y, v, self.dot_size, self.board))  # Create particle
                        
        return return_list



    def run_simulation(self):
        pygame.init()
        pygame.display.set_caption(self.world_title)  # Title
        pygame.display.set_icon(self.icon)  # Icon

        # Initialize font
        font = pygame.font.Font(None, 36)  # Use default font; set size to 36

        paused = False
        for current_iteration in range(self.num_iterations):
            
            # Clear screen
            self.screen.fill((0, 0, 0))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.refresh_rate *= 5
                    if event.key == pygame.K_s:
                        self.refresh_rate *= 0.5
                    if event.key == pygame.K_SPACE:
                        paused = not paused

            # Update particles if not paused
            if not paused:
                p = random.choice(self.particles)
                p.update_particle(self.delta)
                self.num_updates += 1

            # Update screen with new positions and iteration count
            if self.num_updates >= self.refresh_rate:
                self.draw_board()
                
                # Render the iteration text
                text_surface = font.render(
                    f"Iteration: {current_iteration + 1}/{self.num_iterations}", 
                    True, 
                    (255, 255, 0)
                )
                
                # Draw text on screen at the top-left corner
                self.screen.blit(text_surface, (10, 10))

                pygame.display.update()  # Refresh display
                self.num_updates = 0

        pygame.quit()

            


# This class is meant to represent a Particle object in our particle system
import pygame

class Particle:

    def __init__(self, x_position:int, y_position:int, velocity_vector:list, dot_size, board):
        
        assert len(velocity_vector) == 2, 'Problem with the velocity vector'

        self.x = x_position 
        self.y = y_position
        self.v = velocity_vector
        self.size = dot_size
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
        
        # screen.blit(self.image, (max(0, int(self.x)), max(0, int(self.y))))

        # other way
        color = (255,0,255)
        pygame.draw.rect(screen, color, pygame.Rect(self.x * self.size,
                                                    self.y * self.size, 
                                                    self.size, # this is dot size
                                                    self.size  # this too
                                                    ))


















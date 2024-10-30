# This class is meant to represent our Worl (our Taurus) where the Particle System lives
# from Particle import Particle
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

        # self.refresh_rate = mu * width * height 
        self.refresh_rate = 8
        self.num_updates = 0


        self.board = np.zeros((self.width, self.height), dtype=int)
        self.possible_directions = global_possible_directions
        
        self.screen = pygame.display.set_mode((self.width * self.dot_size,
                                                self.height * self.dot_size
                                                ))
        
        self.particles = self.generate_random_particles()
        self.num_particles = len(self.particles)

        self.world_title = world_title
        self.icon = pygame.image.load(icon_file_path)
    
    def draw_board(self): 
        for particle in self.particles:
            particle.draw(self.screen)

    def generate_random_particles(self) -> list:
        return_list = []

        for y in range(self.height):
            for x in range(self.width):
                num = random.random() # random number between 0 and 1
                v = random.choice(self.possible_directions)

                if num < self.mu:
                    self.board[x, y] = 1  # Set particle on the board
                    return_list.append(Particle(x, y, v, self.dot_size, self.board, self.screen))  # Create particle
                        
        return return_list
    
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
    

    def run_simulation(self):
        pygame.init()
        pygame.display.set_caption(self.world_title)  # Title
        pygame.display.set_icon(self.icon)  # Icon

        # Initialize font
        font = pygame.font.Font(None, 36)  # Use default font; set size to 36

        # Game Loop
        # running = True
        paused = False
        
        for current_iteration in range(self.num_iterations):
            
            # Clear screen
            self.screen.fill((0, 0, 0))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:  # Check if a key has been pressed
                    # print(f'{event.key} has been pressed')

                    if event.key == pygame.K_d:  # INCREASE REFRESH RATE
                        self.refresh_rate *= 5

                    if event.key == pygame.K_s:  # DECREASE REFRESH RATE
                        self.refresh_rate *= 0.5

                    if event.key == pygame.K_SPACE:  # PAUSE or RESUME
                        paused = not paused  # Toggle pause state

            if not paused:
                # Pick a particle uniformly at random
                p = random.choice(self.particles)
                p.update_particle(self.delta)                
                self.num_updates += 1

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

                pygame.display.update()  # Only update the display once after all particles are drawn
                self.num_updates = 0

        pygame.quit()



# This class is meant to represent a Particle object in our particle system
import pygame

class Particle:

    def __init__(self, x_position:int, y_position:int, velocity_vector:list, dot_size, board, screen):
        assert len(velocity_vector) == 2, 'Problem with the velocity vector'

        self.x = x_position 
        self.y = y_position
        self.v = velocity_vector
        self.size = dot_size
        self.board = board

        self.previous_x = x_position  # Keep track of the previous position
        self.previous_y = y_position

        self.board[self.x, self.y] = 1

        self.screen = screen

    def update_particle(self, delta):
        assert delta < 1 and delta > 0
        num = random.random()  # random number between 0 and 1

        # Save current position as previous position before moving
        self.previous_x, self.previous_y = self.x, self.y

        if num < delta:  # Change direction/velocity
            self.v = random.choice(global_possible_directions)

        else:
            # Move the particle by its velocity
            new_x = (self.x + self.v[0]) % self.board.shape[0]  # Wrap horizontally
            new_y = (self.y + self.v[1]) % self.board.shape[1]  # Wrap vertically

            # Only move if the new position is empty
            if self.board[new_x, new_y] == 0:
                self.board[self.x, self.y] = 0  # Clear the old position
                self.x, self.y = new_x, new_y
                self.board[self.x, self.y] = 1  # Update the board with new position

            self.clear_old_position(self.screen)
            self.draw(self.screen)



    def clear_old_position(self, screen):
        """Clear the previous position by drawing over it with the background color."""
        background_color = (0, 0, 0)  # Black background
        pygame.draw.rect(screen, background_color, pygame.Rect(self.previous_x * self.size,
                                                               self.previous_y * self.size, 
                                                               self.size, self.size))

    def draw(self, screen):
        """Draw the particle at the current position."""
        color = (255, 255, 255)  # White color
        pygame.draw.rect(screen, color, pygame.Rect(self.x * self.size,
                                                    self.y * self.size, 
                                                    self.size,  # dot size
                                                    self.size))

















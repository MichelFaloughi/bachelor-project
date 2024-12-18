# This class is meant to represent our One Dimensional Particle System, duhh
import pygame
import numpy as np
import random
from global_variables import one_dimensional_possible_directions
from OneDimensionalParticle import OneDimensionalParticle

class OneDimensionalParticleSystem:

    def __init__(self, N:int, screen_width:int, screen_height:int, mu:float, 
                 dot_size:int, num_iterations:int, init_refresh_rate:int=8, 
                 init_paused_status:bool=False, 
                 world_title: str = 'One-Dimensional Interactive Particle System',
                 icon_file_path: str = 'kcl.png' ):
        # Checkers
        assert 0 <= mu  <= 1, 'Mu aint no probability big boi'

        self.N = N
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mu = mu # density, or Probability to spawn
        self.dot_size = dot_size
        self.refresh_rate = init_refresh_rate
        self.paused_status = init_paused_status

        if num_iterations is None:
            self.num_iterations = self.screen_width ** 3 
        else:
            self.num_iterations = num_iterations


        self.important_number = N / screen_width # feels like i will need this
        self.L = (N/screen_width) / 2 # +- interval where we'll look for heat map
        self.num_updates = 0

        self.board_array = np.zeros(N)
        self.possible_directions = one_dimensional_possible_directions

        # Set up display
        self.screen = pygame.display.set_mode((screen_width * dot_size, screen_height * dot_size))
        pygame.display.set_caption(world_title)

        # Load the icon
        self.icon = pygame.image.load(icon_file_path)
        pygame.display.set_icon(self.icon)


        self.particles = self.generate_random_particles()
        self.num_particles = len(self.particles)

    def generate_random_particles(self):
        return_list = []
        for x in range(self.N):
            
            if random.random() < self.mu:  # Spawn particle with probability m
                self.board_array[x] = 1
                v = random.choice(self.possible_directions) # choose Particle's velocity (direction)

                return_list.append(OneDimensionalParticle(x, v, self.dot_size, self.board_array, self.screen))

        return return_list

    def draw_board_array(self):
        """ Draw all particles on the screen """
        for particle in self.particles:
            particle.draw(self.screen)


    def run_simulation(self):
        font = pygame.font.Font(None, 36)

        for current_iteration in range(self.num_iterations):

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_user_key(event.key)

            while self.paused_status:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        self.handle_user_key(event.key)
                # Display pause message
                text_surface = font.render("Paused - Press SPACE to resume", True, (0, 0, 255))
                self.screen.blit(text_surface, (10, 50))
                pygame.display.update() 

            # Update particles
            for _ in range(self.refresh_rate):
                p = random.choice(self.particles)
                p.update_particle()
            self.num_updates += 1

            # Only refresh display at intervals
            if self.num_updates >= self.refresh_rate:
                self.screen.fill((0, 0, 0))  # Clear the screen
                self.draw_board_array()  # Draw particles
                
                # Draw the iteration text last
                text_surface = font.render(f"Iteration: {current_iteration + 1}/{self.num_iterations}", True, (255, 0, 0))
                self.screen.blit(text_surface, (10, 10))  # Draw iteration count on top
                
                pygame.display.update()  # Update display with iteration count visible
                self.num_updates = 0




    def handle_user_key(self, key):

        # Handling pause case
        if key == pygame.K_SPACE:
            self.paused_status = not self.paused_status

        # Handling increasing speed case
        elif key == pygame.K_d: # Increase refresh rate
            if self.refresh_rate > 0:
                self.refresh_rate = min(self.refresh_rate * 2, 150)
            else:
                self.refresh_rate = 1
        
        # Handling decreasing speed case
        elif key == pygame.K_s:  # Decrease refresh rate

            if self.refresh_rate > 0:
                self.refresh_rate = max(self.refresh_rate // 2, 1)
            else:
                self.refresh_rate = 1

        # Handling rendering or not
        # elif key == pygame.K_r:
        #     self.is_rendering = not self.is_rendering

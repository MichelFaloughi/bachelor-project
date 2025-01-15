# This class is meant to represent our One Dimensional Particle System, duhh
import pygame
import numpy as np
import random
from global_variables import one_dimensional_possible_directions
from OneDimensionalParticle import OneDimensionalParticle

# Invariants:
# - We will have screen_height / dot_size rows to be displayed

# Ideas: 
# - Maybe we could have like a two-dimensional list called history, and keep adding rows
# of colors (ex: [(0,0,255), (0,0,0), (210,109,49), etc..] )
# Then make the screen render the first xyz rows from the top ? 

# So, keep track of the self.positions_array, then every self.refresh_rate iterations, convert that 
# positions_array into a list to be inserted as a row in the self.color_history_matrix

# self.positions_array is length N or screen_width
class OneDimensionalParticleSystem:

    def __init__(self, N:int, screen_width:int, screen_height:int, mu:float, delta:float,
                 dot_size:int, num_iterations:int, init_refresh_rate:int=8, 
                 init_paused_status:bool=False, 
                 world_title: str = 'One-Dimensional Interactive Particle System',
                 icon_file_path: str = 'kcl.png' ):
        # Checkers
        assert 0 <= mu  <= 1, 'Mu aint no probability big boi'

        # Initialize pygame
        pygame.init()

        self.N = N
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mu = mu # density, or Probability to spawn
        self.delta = delta # Probability to change direction
        self.dot_size = dot_size
        self.refresh_rate = init_refresh_rate
        self.paused_status = init_paused_status

        if num_iterations is None:
            self.num_iterations = self.screen_width ** 3 
        else:
            self.num_iterations = num_iterations


        self.L = N / screen_width # interval where we'll look for heat map, DO I HAVE TO REDIVIDE BY DOT_SIZE ?
        self.num_updates = 0

        # [ 1 0 0 1 1 0 1 0 1 ... 0 1 0 1] length: 300 000
        # screen_width = 900, dot_size = 10, remember screen_width / dot_size = 90
        # color_history_matrix = [ [ 0.2342, 0.7645, 0.4350, ...],
        #                          [ blablabla                  ],
        #
        #                           ]
        self.positions_array = np.zeros(N) # where all the current info about the particle is
        self.possible_directions = one_dimensional_possible_directions # basically left and right
        self.color_history_matrix = list(np.zeros((screen_height, screen_width)))


        # Set up display
        self.screen = pygame.display.set_mode((screen_width * dot_size, screen_height * dot_size))
        pygame.display.set_caption(world_title)

        # Load the icon
        self.icon = pygame.image.load(icon_file_path)
        pygame.display.set_icon(self.icon)


        self.particles = self.generate_random_particles()
        self.num_particles = len(self.particles)

    # A list of 1D particles
    def generate_random_particles(self):
        return_list = []
        for x in range(self.N):
            
            if random.random() < self.mu:  # Spawn particle with probability mu
                self.positions_array[x] = 1
                v = random.choice(self.possible_directions) # choose Particle's velocity (direction)

                return_list.append(OneDimensionalParticle(x, v, self.dot_size, self.positions_array, self.screen))

        return return_list

    # useful but i don't want it
    # Draw all particles on the screen
    # def draw_positions_array(self):
    #     for particle in self.particles:
    #         particle.draw(self.screen)



    # Gives a row of numbers between 0 and 1 inclusive
    def get_color_row_from_positions_array(self):
    
        row = np.zeros(self.screen_width)
    
        for i in range(self.screen_width):
            row[i] = 







    # takes a new_row from the above method and appends it the the chm, and removes the last one
    # i can pop because chm is a list of np arrays (a matrix basically)
    def update_color_history_matrix(self, new_row):
        return None

    # does what the name suggests
    def draw_color_history_matrix(self):

        return None

    def run_simulation(self):
        font = pygame.font.Font(None, 36)

        for current_iteration in range(self.num_iterations):

            # Event handling, keys pressed and ending game
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_user_key(event.key)
            
            # Pause case
            while self.paused_status:
                
                # Same as before
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
                p = random.choice(self.particles) # pick a particle uniformly at random
                p.update_particle(self.delta)     # then update it
            self.num_updates += 1

            # Only refresh display at intervals
            if self.num_updates >= self.refresh_rate:
                self.screen.fill((0, 0, 0))  # Clear the screen
                # self.draw_positions_array()  # Draw particles         APPARENTLY USELESS, LET'S SEE
                
                # make sure to update color_history matrix before i draw it

                self.draw_color_history_matrix()
                
                # Draw the iteration text last
                text_surface = font.render(f"Iteration: {current_iteration + 1}/{self.num_iterations}", True, (255, 0, 0))
                self.screen.blit(text_surface, (10, 10))  # Draw iteration count on top
                
                pygame.display.update()  # Update display with iteration count visible
                self.num_updates = 0     # reset self.num_updates back to 0




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

# Import necessary modules and global settings
import pygame
import random
import numpy as np
from global_variables import global_possible_directions, global_weights  # Ensure this file is available
import math
from Particle import Particle
import pandas as pd

class ParticleSystem:

    def __init__(self, width: int, height: int, delta: float, mu: float, epsilon: float, alpha: float,
                 dot_size: int, middle_cluster_size:int=-1,
                 num_iterations:int=None, init_refresh_rate:int=8, init_paused_status:bool=False,
                 init_one_step_mode:bool=False,
                 world_title: str = 'Interactive Particle System', icon_file_path: str = 'kcl.png'):
        
        # Validations
        assert 0 <= mu <= 1 and 0 <= delta <= 1

        # Initialize pygame
        pygame.init()

        # Simulation parameters
        self.width = width
        self.height = height
        self.delta = delta  # Probability to change direction
        self.mu = mu        # Probability to spawn, also known as density 
        self.epsilon = epsilon
        self.alpha = alpha   # Probability for a particle to be active
        self.dot_size = dot_size
        self.middle_cluster_size = middle_cluster_size

        if num_iterations is None:
            self.num_iterations = int(self.width * self.height ** 2 )
        else:
            self.num_iterations = (num_iterations)


        self.refresh_rate = init_refresh_rate
        self.display_run_info = True # run id and iterations, 
        # self.refresh_rate = 0
        self.num_updates = 0

        # Set up the board, particles, and screen
        self.board = np.zeros((self.width, self.height), dtype=int)
        self.coordinates = [(x, y) for x in range(self.board.shape[0]) for y in range(self.board.shape[1])] # useful later in clusteredness
        # beware there are more efficient ways to get the coordinates if you want

        self.possible_directions = global_possible_directions
        
        # Set up display
        self.screen = pygame.display.set_mode((self.width * self.dot_size, self.height * self.dot_size))
        pygame.display.set_caption(world_title)

        # Say if you want the world to be rendered or not (affects run_simulation)
        self.is_rendering = True # user can change by pressing R
        
        # Load the icon
        try:
            self.icon = pygame.image.load(icon_file_path)
            pygame.display.set_icon(self.icon)
        except FileNotFoundError:
            print(f"Warning: Icon file {icon_file_path} not found.")
        
        # Generate particles
        self.particles = self.generate_middle_cluster()
        self.num_particles = len(self.particles)


        # Deciding the origin
        self.origin_x = self.width // 2
        self.origin_y = self.height // 2

        # Initializing pause to false
        self.paused_status = init_paused_status

        self.one_step_mode = init_one_step_mode

        # Initializing ring coordinates list
        self.ring_coordinates_list = self.get_ring_coordinates_list()

        self.id = self.read_and_increment_run_id(2) 

        self.log_run(excel_path="ParticleSystem_database.xlsx") # log the run in the database



    ###################
    ## Admin methods ##
    ###################

    def draw_board(self):
        """Draw all particles on the screen."""
        for particle in self.particles:
            # Check if particle is at the origin
            if particle.x == self.origin_x and particle.y == self.origin_y:
                particle.draw(self.screen, color=(255, 0, 0))  # Draw origin particle in red (or any color)
            else:
                particle.draw(self.screen)



    def generate_random_particles(self) -> list:
        """Generate particles randomly on the board based on density `mu`."""
        return_list = []
        for y in range(self.height):
            for x in range(self.width):
                
                if random.random() < self.mu:  # Spawn particle with probability mu
                    self.board[x, y] = 1

                    if random.random() < self.alpha: # Spawn active particle with probability alpha
                        active = True

                        # remember possible_directions should look like this [ [0,1], [1,0], [0,-1], [-1,0] ]
                        v = random.choice(self.possible_directions)
                    
                    else: 
                        active = False
                        v = None

                    return_list.append(Particle(x, y, v, active, self.dot_size, self.board, self.screen))

        return return_list
    

    # When self.middle_cluster_size = -1 , this is the same as generating randim particles
    def generate_middle_cluster(self) -> list:
        
        # Here all particles are active ?
        return_list = []
        for y in range(self.height):
            for x in range(self.width):
                

                self.origin_x = self.width // 2 # maybe this could even be outside the nested for loops, does it change ? 
                self.origin_y = self.height // 2

                if (abs(y - self.origin_y) <= self.middle_cluster_size and abs(x - self.origin_x) <= self.middle_cluster_size) or random.random() < self.mu:
                    
                    self.board[x, y] = 1
                    
                    if random.random() < self.alpha:
                        active = True
                        # remember possible_directions should look like this [ [0,1], [1,0], [0,-1], [-1,0] ]
                        v = random.choices(self.possible_directions,
                                          weights= global_weights,
                                                   k=1  # i think num choices
                                                   )[0]
                        # v = [1,0]
                    else:
                        active = False
                        v = None

                    return_list.append(Particle(x, y, v, active, self.dot_size, self.board, self.screen))
        
        
        return return_list
    
    def get_ring_coordinates_list(self):
        """
        Compute the coordinates of the points on the square ring around the origin.
        The ring has a radius of 5% of self.width (rounded to the nearest integer).
        Updates self.ring_coordinates_list with these coordinates.
        """
        # Calculate the radius as 5% of the width, rounded to the nearest integer
        radius = max(1, round(self.width * 0.05))  # Ensure radius is at least 1

        # Initialize the list to store the coordinates
        ring_coordinates = []

        # Calculate the bounds of the square
        min_x = self.origin_x - radius
        max_x = self.origin_x + radius
        min_y = self.origin_y - radius
        max_y = self.origin_y + radius

        # Iterate over the bounds to capture the ring
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                # Add only the points on the edges of the square
                if (
                    (x == min_x or x == max_x) or  # Top and bottom edges
                    (y == min_y or y == max_y)    # Left and right edges
                ):
                    # Ensure the coordinates are within bounds
                    if 0 <= x < self.width and 0 <= y < self.height:
                        ring_coordinates.append((x, y))

        return ring_coordinates 


    def read_and_increment_run_id(self, line_number):
        assert line_number == 2, 'This is for 2D Particle Systems !'

        file_path = "run_ids.txt"

        with open(file_path, "r") as file:
            lines = file.readlines()

        # Extract the first number from the specified line
        first_part = lines[line_number - 1].split()[0]  # Extracts '00000001'
        new_id = int(first_part) + 1  # Increment by 1

        # Format it back to match the original 8-digit format
        new_id_str = f"{new_id:08d}"  

        # Replace the first number in the line while keeping the rest unchanged
        lines[line_number - 1] = new_id_str + "   " + " ".join(lines[line_number - 1].split()[1:]) + "\n"

        # Write the updated content back to the file
        with open(file_path, "w") as file:
            file.writelines(lines)

        return first_part

    # This is the function that will write to the 'ParticleSystem_database.xlsx' 
    def log_run(self, excel_path="ParticleSystem_database.xlsx"):

        new_data = {
            "ID": [self.id],  
            "mu": [self.mu],
            "delta": [self.delta],
            "epsilon": [self.epsilon],
            "alpha": [self.alpha],
            "width": [self.width],
            "height": [self.height],
            "num_particles": [self.num_particles],
            "num_iterations": [self.num_iterations]
        }

        new_df = pd.DataFrame(new_data)

        # Append to the existing Excel file
        with pd.ExcelWriter(excel_path, mode="a", if_sheet_exists="overlay", engine="openpyxl") as writer:
            existing_df = pd.read_excel(excel_path, engine="openpyxl")
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            updated_df.to_excel(writer, index=False)




    ###################
    ## Run functions ##
    ###################

    def run_simulation(self):
        """Main loop to run the particle system simulation."""
        # Set up font for displaying the iteration count
        font = pygame.font.Font(None, 36)

        for current_iteration in range(int(self.num_iterations)):

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_user_key(event.key)

            # If self.paused_status is True, enter a loop that only breaks when SPACE is pressed again
            while self.paused_status:
                
                self.one_step_mode = False

                # Check for events to allow unpausing and adjusting refresh rate
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        self.handle_user_key(event.key) # 

                
                if self.display_run_info:
                    # Display pause message
                    text_surface = font.render("Paused - Press SPACE to resume", True, (0, 0, 255))
                    self.screen.blit(text_surface, (10, 50))
                pygame.display.update()


            # if one step mode is true, make sure to set pause to true so that next iteration we stop
            if self.one_step_mode:
                self.paused_status = True


            # Update particles
            for _ in range(self.refresh_rate):
                p = random.choice(self.particles)
                p.update_particle(self.delta, self.epsilon)
            self.num_updates += 1


            # Only render world if we want to
            if self.is_rendering:

                # Only refresh display at intervals
                if self.num_updates >= self.refresh_rate:
                    self.screen.fill((0, 0, 0))  # Clear the screen
                    self.draw_board()  # Draw particles
                    
                    if self.display_run_info:

                        # Draw the iteration text last
                        text_surface = font.render(f"Iteration: {current_iteration + 1}", True, (255, 0, 0))
                        self.screen.blit(text_surface, (10, 10))  # Draw iteration count on top

                        # Display the ParticleSystem's ID
                        text_surface = font.render(f"Run ID: {self.id}", True, (0, 255, 0))
                        self.screen.blit(text_surface, (10, 30))  # Draw ID on top

                    pygame.display.update()  # Update display with iteration count visible
                    self.num_updates = 0
            
            # I can keep the counter but not the world if you want, up to you prof Stauffer
                    

            








    def run_simulation_calculations_only(self, render_iterations=False, update_interval=300):
        """Main loop to run the particle system simulation without rendering for faster calculations."""
        
        
        if render_iterations:
            print("Rendering is enabled")  # Debug statement
            # Render code block
        else:
            print("Rendering is disabled")  # Debug statement
            # Calculation-only code block

        if render_iterations:

            font = pygame.font.Font(None, 36)

            for current_iteration in range(int(self.num_iterations)):

                # Event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        self.handle_user_key(event.key)

                # If self.paused_status is True, enter a loop that only breaks when SPACE is pressed again
                while self.paused_status:
                    self.one_step_mode = False

                    # Check for events to allow unpausing and adjusting refresh rate
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN:
                            self.handle_user_key(event.key)

                # If one-step mode is enabled, set pause to true to stop at the next iteration
                if self.one_step_mode:
                    self.paused_status = True

                # Update particles without rendering
                for _ in range(self.refresh_rate):
                    p = random.choice(self.particles)
                    p.update_particle(self.delta, self.epsilon)
                self.num_updates += 1

                
                # Render iteration count only at specified intervals
                if current_iteration % update_interval  == 0 or current_iteration == self.num_iterations - 1:
                # if current_iteration % self.refresh_rate  == 0 or current_iteration == self.num_iterations - 1:
                
                    self.screen.fill((0, 0, 0))  # Clear the screen
                    text_surface = font.render(f"Iteration: {current_iteration + 1}", True, (255, 255, 255))
                    self.screen.blit(text_surface, (10, 10))  # Draw the iteration count text
                    pygame.display.update()  # Update display with iteration count only
        
        else:

            for current_iteration in range(int(self.num_iterations)):

                # Event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        self.handle_user_key(event.key)

                # If self.paused_status is True, enter a loop that only breaks when SPACE is pressed again
                while self.paused_status:
                    self.one_step_mode = False

                    # Check for events to allow unpausing and adjusting refresh rate
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN:
                            self.handle_user_key(event.key)

                # If one-step mode is enabled, set pause to true to stop at the next iteration
                if self.one_step_mode:
                    self.paused_status = True

                # Update particles without rendering
                for _ in range(self.refresh_rate):
                    p = random.choice(self.particles)
                    p.update_particle(self.delta, self.epsilon)
                self.num_updates += 1


    # now this doesn't allow to stop mid way
    def run_simulation_keep_track_of_middle_cluster_size(self, calculation_interval=100, calculation_method='ring'):
        """Runs the particle simulation while keeping track of cluster size at specified intervals."""
        # first just set the method
        if calculation_method == 'ring':
            cluster_calculation_method = self.get_ring_cluster_cardinality
        else:
            cluster_calculation_method = self.get_curr_cluster_cardinality


        records_df = pd.DataFrame(columns=['Iteration', 'Cluster Cardinality'])

        for current_iteration in range(int(self.num_iterations)):
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_user_key(event.key)

            # If self.paused_status is True, enter a loop that only breaks when SPACE is pressed again
            while self.paused_status:
                self.one_step_mode = False

                # Check for events to allow unpausing and adjusting refresh rate
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        self.handle_user_key(event.key)

            # If one-step mode is enabled, set pause to true to stop at the next iteration
            if self.one_step_mode:
                self.paused_status = True

            # Update particles without rendering
            for _ in range(self.refresh_rate):
                p = random.choice(self.particles)
                p.update_particle(self.delta, self.epsilon)
            self.num_updates += 1

            # Record cluster size at specified intervals
            if current_iteration % calculation_interval == 0 or current_iteration == self.num_iterations - 1:
                curr_cluster_cardinality = cluster_calculation_method()
                
                # Add the record to DataFrame
                records_df.loc[current_iteration] = [
                    current_iteration,
                    curr_cluster_cardinality,
                ]

        # Save the records to a CSV file
        records_df.to_csv('latest_run_cluster_records.csv', index=False)





    # This is a fucntion that will run until we record the first instance of the world having a single cluster
    # We will not check at EACH iteration, and there are a lot of optimizations (short circuiting) to have but
    # for now this is what we have 
    # This method is made to run alone, and will return an iteration, unless stopped earlier
    def run_simulation_get_iteration_of_first_single_cluster(self, refresh_rate=100, check_rate=40000, init_render_status=False, first_check=200000, min_cluster_size=500):
        num_updates_for_cluster_checking = 0 # initialization, this is the counter
        self.refresh_rate = refresh_rate 
        self.is_rendering = init_render_status

        # Set up font for displaying the iteration count
        font = pygame.font.Font(None, 36)

        for current_iteration in range(int(self.num_iterations)):

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_user_key(event.key)

            # If self.paused_status is True, enter a loop that only breaks when SPACE is pressed again
            while self.paused_status:
                
                self.one_step_mode = False

                # Check for events to allow unpausing and adjusting refresh rate
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        self.handle_user_key(event.key) # 

                
                if self.display_run_info:
                    # Display pause message
                    text_surface = font.render("Paused - Press SPACE to resume", True, (0, 0, 255))
                    self.screen.blit(text_surface, (10, 50))
                pygame.display.update()

            # if one step mode is true, make sure to set pause to true so that next iteration we stop
            if self.one_step_mode:
                self.paused_status = True


            # Update particles
            for _ in range(self.refresh_rate):
                p = random.choice(self.particles)
                p.update_particle(self.delta, self.epsilon)
            self.num_updates += 1
            num_updates_for_cluster_checking += 1


            # Only render world if we want to
            if self.is_rendering:

                # Only refresh display at intervals
                if self.num_updates >= self.refresh_rate:
                    self.screen.fill((0, 0, 0))  # Clear the screen
                    self.draw_board()  # Draw particles
                    
                    if self.display_run_info:

                        # Draw the iteration text last
                        text_surface = font.render(f"Iteration: {current_iteration + 1}", True, (255, 0, 0))
                        self.screen.blit(text_surface, (10, 10))  # Draw iteration count on top

                        # Display the ParticleSystem's ID
                        text_surface = font.render(f"Run ID: {self.id}", True, (0, 255, 0))
                        self.screen.blit(text_surface, (10, 30))  # Draw ID on top

                    pygame.display.update()  # Update display with iteration count visible
                    self.num_updates = 0
            
            # I can keep the counter but not the world if you want, up to you prof Stauffer
                    
            # Check when we get one cluster
            if num_updates_for_cluster_checking >= check_rate and current_iteration > first_check: # we won't check else this
                    
                # ASSUMING IT WILL ALWAYS CONVERGE TO 1, WHICH MIGHT BE A BAD ASSUMPTION
                curr_num_clusters = len(self.get_curr_cluster_sizes(stop_at=2, min_cluster_size=min_cluster_size))

                if curr_num_clusters == 1: 
                    pygame.quit()
                    return current_iteration
                
                num_updates_for_cluster_checking = 0 # reset


    # Similar to function above, just simpler without rendering etc
    def SIMPLE_run_simulation_get_iteration_of_first_single_cluster(self, refresh_rate=100, check_rate=40000, init_render_status=False, first_check=200000):
        num_updates_for_cluster_checking = 0 # initialization, this is the counter
        self.refresh_rate = refresh_rate 
        self.is_rendering = init_render_status

        for current_iteration in range(int(self.num_iterations)):

            # Update particles
            for _ in range(self.refresh_rate):
                p = random.choice(self.particles)
                p.update_particle(self.delta, self.epsilon)
            self.num_updates += 1
            num_updates_for_cluster_checking += 1

            if num_updates_for_cluster_checking >= check_rate and current_iteration > first_check: # we won't check else this
                    
                # ASSUMING IT WILL ALWAYS CONVERGE TO 1, WHICH MIGHT BE A BAD ASSUMPTION
                curr_num_clusters = len(self.get_curr_cluster_sizes(stop_at=2))
                
                if curr_num_clusters == 1: #  or current_iteration >= 10000000:  it was a stupid idea ...
                    pygame.quit()
                    return current_iteration
                
                num_updates_for_cluster_checking = 0 # reset

    # RETURNS A DATAFRAME of iterations, num_clusters_id as columns
    def run_simulation_get_num_clusters_at_each_iteration(self, min_cluster_size, refresh_rate=100, check_rate=3000, init_render_status=False):
        num_updates_for_cluster_checking = 0 # initialization, this is the counter
        self.refresh_rate = refresh_rate # default to make it faster ...
        self.is_rendering = init_render_status
        
        df = pd.DataFrame(columns=["Iteration", f"ParticleSystem_{str(int(self.id))}"]) # the nested str int structure is to remove the left 0s 

        # Set up font for displaying the iteration count
        font = pygame.font.Font(None, 36)

        for current_iteration in range(int(self.num_iterations)):

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_user_key(event.key)

            # If self.paused_status is True, enter a loop that only breaks when SPACE is pressed again
            while self.paused_status:
                
                self.one_step_mode = False

                # Check for events to allow unpausing and adjusting refresh rate
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        self.handle_user_key(event.key) # 

                
                if self.display_run_info:
                    # Display pause message
                    text_surface = font.render("Paused - Press SPACE to resume", True, (0, 0, 255))
                    self.screen.blit(text_surface, (10, 50))
                pygame.display.update()

            # if one step mode is true, make sure to set pause to true so that next iteration we stop
            if self.one_step_mode:
                self.paused_status = True


            # Update particles
            for _ in range(self.refresh_rate):
                p = random.choice(self.particles)
                p.update_particle(self.delta, self.epsilon)
            self.num_updates += 1
            num_updates_for_cluster_checking += 1


            # Only render world if we want to
            if self.is_rendering:

                # Only refresh display at intervals
                if self.num_updates >= self.refresh_rate:
                    self.screen.fill((0, 0, 0))  # Clear the screen
                    self.draw_board()  # Draw particles
                    
                    if self.display_run_info:

                        # Draw the iteration text last
                        text_surface = font.render(f"Iteration: {current_iteration + 1}", True, (255, 0, 0))
                        self.screen.blit(text_surface, (10, 10))  # Draw iteration count on top

                        # Display the ParticleSystem's ID
                        text_surface = font.render(f"Run ID: {self.id}", True, (0, 255, 0))
                        self.screen.blit(text_surface, (10, 30))  # Draw ID on top

                    pygame.display.update()  # Update display with iteration count visible
                    self.num_updates = 0
            
            # I can keep the counter but not the world if you want, up to you prof Stauffer
                    
            # Check when we get one cluster
            if num_updates_for_cluster_checking >= check_rate: # and current_iteration > first_check 
                    
                
                # ASSUMING IT WILL ALWAYS CONVERGE TO 1, WHICH MIGHT BE A BAD ASSUMPTION
                curr_num_clusters = len(self.get_curr_cluster_sizes(min_cluster_size=min_cluster_size))
                
                df.loc[len(df)] = [current_iteration, curr_num_clusters]
                
                num_updates_for_cluster_checking = 0 # reset

        return df



    # this will run de experiment described on 27/02/2025 in the log book
    # returns a dict (a new row to be added to whatever dataframe I am writing to)
    def run_simulation_latest_experiement(self, min_cluster_size, refresh_rate=100, check_rate=3000, init_render_status=False):

        # record min(iteration of first time we get one single cluster, self.num_iterations)                   -- a single number
        # num large clusters at the end of the simulations                                                     -- a single number   
        # num particles in large clusters at the end of the simulation                                         -- a list (one number per cluster)
        # num particles in total in the system (can get at time 0) to compute density of clustered particles   -- a single number 
        # density of clustered particles                                                                       -- a single number in (0,1)

        first_single_cluster_recorded = False # swap to true when we do to stop checking, use stop_at when checking

        num_updates_for_cluster_checking = 0 # initialization, this is the counter
        self.refresh_rate = refresh_rate # default to make it faster ...
        self.is_rendering = init_render_status
        
        iteration_of_first_single_cluster = None # we have to set it to None until we find one, we might not

        # This is what will be returned
        return_row = {'Run ID': int(self.id),
                      'Iteration of first single cluster': None,          # placeholder
                      'Num clusters at end': None,                        # placeholder
                      'Num particles per cluster at end': None,           # placeholder
                      'Total num particles in clusters at end': None,     # placeholder
                      'Total num particles': self.num_particles,  
                      'Density of clustered particles': None,             # placeholder, assert this is in (0,1)
                      }
       
        font = pygame.font.Font(None, 36)
        for current_iteration in range(int(self.num_iterations)):
                    
                # Event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        self.handle_user_key(event.key)
                # If self.paused_status is True, enter a loop that only breaks when SPACE is pressed again
                while self.paused_status:
                    
                    self.one_step_mode = False

                    # Check for events to allow unpausing and adjusting refresh rate
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN:
                            self.handle_user_key(event.key) # 

                    
                    if self.display_run_info:
                        # Display pause message
                        text_surface = font.render("Paused - Press SPACE to resume", True, (0, 0, 255))
                        self.screen.blit(text_surface, (10, 50))
                    pygame.display.update()
                #if one step mode is true, make sure to set pause to true so that next iteration we stop
                if self.one_step_mode:
                    self.paused_status = True


                # Update particles
                for _ in range(self.refresh_rate):
                    p = random.choice(self.particles)
                    p.update_particle(self.delta, self.epsilon)
                self.num_updates += 1
                num_updates_for_cluster_checking += 1

                # Only render world if we want to
                if self.is_rendering:

                    # Only refresh display at intervals
                    if self.num_updates >= self.refresh_rate:
                        self.screen.fill((0, 0, 0))  # Clear the screen
                        self.draw_board()  # Draw particles
                        
                        if self.display_run_info:

                            # Draw the iteration text last
                            text_surface = font.render(f"Iteration: {current_iteration + 1}", True, (255, 0, 0))
                            self.screen.blit(text_surface, (10, 10))  # Draw iteration count on top

                            # Display the ParticleSystem's ID
                            text_surface = font.render(f"Run ID: {self.id}", True, (0, 255, 0))
                            self.screen.blit(text_surface, (10, 30))  # Draw ID on top

                        pygame.display.update()  # Update display with iteration count visible
                        self.num_updates = 0
                
                
                if (not first_single_cluster_recorded) and (num_updates_for_cluster_checking >= check_rate):
                    # if we haven't found the first cluster yet

                    curr_num_clusters = len(self.get_curr_cluster_sizes(min_cluster_size=min_cluster_size, stop_at=2))
                                        
                    num_updates_for_cluster_checking = 0 # reset

                    if curr_num_clusters == 1:
                        iteration_of_first_single_cluster = current_iteration
                        first_single_cluster_recorded = True




        # now that we are at the end of the system's simulation:
        cluster_sizes                  = self.get_curr_cluster_sizes(min_cluster_size=min_cluster_size)
        num_clusters_at_end            = len(cluster_sizes)
        total_clustered_particles      = sum(cluster_sizes)
        density_of_clustered_particles = round(total_clustered_particles / self.num_particles , 4)

        return_row['Iteration of first single cluster']      = iteration_of_first_single_cluster
        return_row['Num clusters at end']                    = num_clusters_at_end
        return_row['Num particles per cluster at end']       = cluster_sizes
        return_row['Total num particles in clusters at end'] = total_clustered_particles
        return_row['Density of clustered particles']         = density_of_clustered_particles 

        # It is possible that are no single clusters we can't assume that yet
        # assert  return_row['Iteration of first single cluster'] is not None,       "Iteration of first single cluster is None!"
        
        assert  return_row['Num clusters at end'] is not None,                 "Num clusters at the end is None!"
        assert  return_row['Num particles per cluster at end'] is not None,        "Num particles per cluster at end None!"
        assert  return_row['Total num particles in clusters at end'] is not None,  "Total num particles in clusters at end is None!"
        assert  return_row['Density of clustered particles'] is not None,          "Density of clustered particles is None!"
        assert  return_row['Run ID'] is not None,                                  "Run ID is None!"
        assert  return_row['Total num particles'] is not None,                     "Total num particles is None!"

        assert 0 <= return_row["Density of clustered particles"] <= 1,  "Something wrong with the density bruh"
        
        return return_row














    ###########################
    ## Handling Interactions ##
    ###########################

        
    def handle_user_key(self, key):

        # Handling pause case
        if key == pygame.K_SPACE:
            self.paused_status = not self.paused_status  # Exit the pause loop

        # Handling increasing speed case
        elif key == pygame.K_d:  # Increase refresh rate
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
        
        # One step forward
        elif key == pygame.K_f:
            
            self.one_step_mode = True
            self.paused_status = False # pause has to be False to allow one loop to happen
            # the if statement below the pause while loop will set it back to paused
            self.refresh_rate = 1 # or else refresh_rate particles are going to move
        
        # Handling the rendering vs not rendering case
        elif key == pygame.K_r:
            self.is_rendering = not self.is_rendering

        # Handling display of run info, run ID and iteration
        elif key == pygame.K_i:
            self.display_run_info = not self.display_run_info
        
        # Getting origin cluster cardinality for DEBUG or other purposes
        elif key == pygame.K_c:
            origin_cluster_cardinality, nodes = self.get_curr_cluster_STRICT_cardinality(also_return_visited_nodes=True)
            print(origin_cluster_cardinality, '  ', nodes)
        
        # same for cluster size and DEBUG puposes
        elif key == pygame.K_x:
            curr_cluster_sizes: list = self.get_curr_cluster_sizes()
            curr_num_clusters : int = len(curr_cluster_sizes)
            
            print(f'''Cluster Sizes: {curr_cluster_sizes}
                  Num Clusters: {curr_num_clusters}''')



    def get_user_response(self, user_response):
        if user_response == 'r' or user_response == 'R':
            return True
        return False
    



































                                            #############################
############################################## Statistics Calculations ##############################################
                                            #############################

    def get_curr_cluster_cardinality(self, start_x=None, start_y=None, also_return_visited_nodes: bool = False):
        """Calculate the cardinality of the cluster starting from the origin or surrounding cells."""
        # This is to make sure the default values are the origin
        if start_x is None:
            start_x = self.origin_x

        if start_y is None:
            start_y = self.origin_y

        # If the origin has a particle, start the search from the origin
        if self.board[start_x, start_y] == 1:
            queue = [(start_x, start_y)]
        else:
            # Otherwise, check for particles in the neighboring cells
            queue = [
                (start_x + dx, start_y + dy)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]  # N, S, E, W
                if 0 <= start_x + dx < self.width and 0 <= start_y + dy < self.height
                and self.board[start_x + dx, start_y + dy] == 1
            ]

            # If no neighbors have particles, return 0 (no cluster)
            if not queue:
                if also_return_visited_nodes:
                    return 0, []  # Return empty visited nodes when requested
                else:
                    return 0

        # Initialize BFS/DFS
        visited = set(queue)
        length = 0
        nodes_in_cluster = []

        # Directions for North, South, East, West
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1)  # N, S, E, W
        ]

        # Perform BFS/DFS
        while queue:
            x, y = queue.pop(0)  # Use queue.pop() if DFS is preferred
            length += 1  # Count this particle
            nodes_in_cluster.append((x, y))
            # Check all adjacent positions
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Ensure the neighbor is within bounds
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Check if the neighbor has a particle and hasn't been visited
                    if self.board[nx, ny] == 1 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))  # Mark as visited

        if also_return_visited_nodes:
            return length, nodes_in_cluster
        return length
    
    
    # This method differs from the above in that it doesn't check the neighboring cells to start_x and start_y if the formers
    # are empty, it just returns 0 or 0, []
    def get_curr_cluster_STRICT_cardinality(self, start_x=None, start_y=None, also_return_visited_nodes: bool = False):
        """Calculate the cardinality of the cluster starting from the origin cell STRICTLY in a toroidal board."""
        # Ensure default values are the origin
        if start_x is None:
            start_x = self.origin_x
        if start_y is None:
            start_y = self.origin_y

        # If the start position is empty, return 0 immediately
        if self.board[start_x, start_y] == 0:
            return (0, []) if also_return_visited_nodes else 0

        # Initialize BFS/DFS
        queue = [(start_x, start_y)]
        visited = set(queue)
        length = 0
        nodes_in_cluster = []

        # Directions for North, South, East, West
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Perform BFS/DFS
        while queue:
            x, y = queue.pop(0)  # Use queue.pop() for DFS instead
            length += 1  # Count this particle
            nodes_in_cluster.append((x, y))

            # Check all adjacent positions, wrapping around using modulo
            for dx, dy in directions:
                nx = (x + dx) % self.width  # Wrap around horizontally
                ny = (y + dy) % self.height  # Wrap around vertically

                # Check if the neighbor has a particle and hasn't been visited
                if self.board[nx, ny] == 1 and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))  # Mark as visited

        return (length, nodes_in_cluster) if also_return_visited_nodes else length

    




    def get_curr_radius_euclidean_length(self):
        """Returns the Euclidean radius (maximum distance) of the cluster starting from the origin or neighboring cells."""
        # Initialize the queue based on the origin and neighbors
        if self.board[self.origin_x, self.origin_y] == 1:
            queue = [(self.origin_x, self.origin_y)]
        else:
            # Add neighboring cells with particles if the origin is empty
            queue = [
                (self.origin_x + dx, self.origin_y + dy)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),  # N, S, E, W
                            (1, 1), (-1, -1), (1, -1), (-1, 1)]  # NE, NW, SE, SW
                if 0 <= self.origin_x + dx < self.width and 0 <= self.origin_y + dy < self.height
                and self.board[self.origin_x + dx, self.origin_y + dy] == 1
            ]
            
            # If no neighbors have particles, return 0 (no cluster)
            if not queue:
                return 0

        # Initialize BFS
        visited = set(queue)
        max_radius = 1

        # Directions for BFS/DFS
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1)  # N, S, E, W
        ]

        # Perform BFS to find the maximum Euclidean distance
        while queue:
            x, y = queue.pop(0)

            # Calculate Euclidean distance from the origin
            distance = math.sqrt((x - self.origin_x) ** 2 + (y - self.origin_y) ** 2)
            max_radius = max(max_radius, distance)

            # Explore neighbors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[nx, ny] == 1 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))

        return max_radius

    def get_curr_radius_manhattan_length(self):
        """Returns the Manhattan radius (maximum distance) of the cluster starting from the origin or neighboring cells."""
        # Initialize the queue based on the origin and neighbors
        if self.board[self.origin_x, self.origin_y] == 1:
            queue = [(self.origin_x, self.origin_y)]
        else:
            # Add neighboring cells with particles if the origin is empty
            queue = [
                (self.origin_x + dx, self.origin_y + dy)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),  # N, S, E, W
                            (1, 1), (-1, -1), (1, -1), (-1, 1)]  # NE, NW, SE, SW
                if 0 <= self.origin_x + dx < self.width and 0 <= self.origin_y + dy < self.height
                and self.board[self.origin_x + dx, self.origin_y + dy] == 1
            ]
            
            # If no neighbors have particles, return 0 (no cluster)
            if not queue:
                return 0

        # Initialize BFS
        visited = set(queue)
        max_radius = 1

        # Directions for BFS/DFS
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1)  # N, S, E, W
        ]

        # Perform BFS to find the maximum Manhattan distance
        while queue:
            x, y = queue.pop(0)

            # Calculate Manhattan distance from the origin
            distance = abs(x - self.origin_x) + abs(y - self.origin_y)
            max_radius = max(max_radius, distance)

            # Explore neighbors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[nx, ny] == 1 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))

        return max_radius



    # New cluster cardinality that calculates it with the ring thing
    def get_ring_cluster_cardinality(self):

        cardinalities = []

        for coordinates in self.ring_coordinates_list:
            
            x,y  = coordinates
            
            cardinalities.append(self.get_curr_cluster_cardinality(x, y))

        return max(cardinalities)


    # def get_curr_strict_cluster_cardinality(self, start_x=None, start_y=None, also_return_visited_nodes: bool = False):
    #     """Calculate the cardinality of the cluster starting from the origin or surrounding cells."""
    #     # This is to make sure the default values are the origin
    #     if start_x is None:
    #         start_x = self.origin_x

    #     if start_y is None:
    #         start_y = self.origin_y

    #     # If the origin has a particle, start the search from the origin
    #     if self.board[start_x, start_y] == 1:
    #         queue = [(start_x, start_y)]
    #     else:
    #         if also_return_visited_nodes:
    #             return 0, []
    #         return 0

    #     # Initialize BFS/DFS
    #     visited = set(queue)
    #     length = 0
    #     nodes_in_cluster = []

    #     # Directions for North, South, East, West
    #     directions = [
    #         (1, 0), (-1, 0), (0, 1), (0, -1)  # N, S, E, W
    #     ]

    #     # Perform BFS/DFS
    #     while queue:
    #         x, y = queue.pop(0)  # Use queue.pop() if DFS is preferred
    #         length += 1  # Count this particle
    #         nodes_in_cluster.append((x, y))
    #         # Check all adjacent positions
    #         for dx, dy in directions:
    #             nx, ny = x + dx, y + dy

    #             # Ensure the neighbor is within bounds
    #             if 0 <= nx < self.width and 0 <= ny < self.height:
    #                 # Check if the neighbor has a particle and hasn't been visited
    #                 if self.board[nx, ny] == 1 and (nx, ny) not in visited:
    #                     queue.append((nx, ny))
    #                     visited.add((nx, ny))  # Mark as visited

    #     if also_return_visited_nodes:
    #         return length, nodes_in_cluster
    #     return length


    # returns a list of the size of all cmlusters of that time. len(of this) can tell us the num clusters
    # the stop_at argument is used to test if we only have a certain number of cluster, if we have more than stop_at we short-circuit
    def get_curr_cluster_sizes(self, min_cluster_size: int = 50, stop_at=None) -> list:
        cluster_sizes = []  # Track all cluster sizes
        curr_coords = self.coordinates.copy()  # Make a copy

        while curr_coords:  # Process until all coordinates are visited
            x, y = curr_coords.pop(0)  # Get first coordinate and remove it
            length, visited_nodes = self.get_curr_cluster_STRICT_cardinality(
                start_x=x, start_y=y, also_return_visited_nodes=True
            )
            
            # Remove visited nodes from curr_coords
            curr_coords = [coord for coord in curr_coords if coord not in visited_nodes]

            if length >= min_cluster_size:
                cluster_sizes.append(length)

            if stop_at: # ie if it's not None
                if len(cluster_sizes) >= stop_at:
                    return [] # ? I guess arbitrary
            
        assert not curr_coords  # Ensure we visited all coordinates

        return cluster_sizes


        # so here I want to compute the number of white connected components bigger than or equal to some threshold
        # to do so i might want to brush up on the set data structure

        # so i should have a list of all the ppossible coordinates on the board, then loop through them
        # i can use the get cluster cardinality function already defined above.
        # 

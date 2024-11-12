# Import necessary modules and global settings
import pygame
import random
import numpy as np
from global_variables import global_possible_directions  # Ensure this file is available
import math
from Particle import Particle
import pandas as pd

class ParticleSystem:

    def __init__(self, width: int, height: int, delta: float, mu: float, dot_size: int, 
                 middle_cluster_size:int=-1,
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
        self.dot_size = dot_size
        self.middle_cluster_size = middle_cluster_size

        if num_iterations is None:
            self.num_iterations = self.width * self.height ** 2 
        else:
            self.num_iterations = num_iterations


        self.refresh_rate = init_refresh_rate
        # self.refresh_rate = 0
        self.num_updates = 0

        # Set up the board, particles, and screen
        self.board = np.zeros((self.width, self.height), dtype=int)
        self.possible_directions = global_possible_directions
        
        # Set up display
        self.screen = pygame.display.set_mode((self.width * self.dot_size, self.height * self.dot_size))
        pygame.display.set_caption(world_title)
        
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
                    v = random.choice(self.possible_directions)
                    self.board[x, y] = 1
                    return_list.append(Particle(x, y, v, self.dot_size, self.board, self.screen))
        return return_list
    
    def generate_middle_cluster(self) -> list:
        
        return_list = []
        for y in range(self.height):
            for x in range(self.width):
                

                self.origin_x = self.width // 2
                self.origin_y = self.height // 2

                if (abs(y - self.origin_y) <= self.middle_cluster_size and abs(x - self.origin_x) <= self.middle_cluster_size) or random.random() < self.mu:
                    
                    v = random.choice(self.possible_directions)
                    self.board[x, y] = 1
                    return_list.append(Particle(x, y, v, self.dot_size, self.board, self.screen))
        
        
        return return_list
    



    def run_simulation(self):
        """Main loop to run the particle system simulation."""
        # Set up font for displaying the iteration count
        font = pygame.font.Font(None, 36)

        for current_iteration in range(self.num_iterations):

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
                p.update_particle(self.delta)
            self.num_updates += 1

            # Only refresh display at intervals
            if self.num_updates >= self.refresh_rate:
                self.screen.fill((0, 0, 0))  # Clear the screen
                self.draw_board()  # Draw particles
                
                # Draw the iteration text last
                text_surface = font.render(f"Iteration: {current_iteration + 1}/{self.num_iterations}", True, (255, 0, 0))
                self.screen.blit(text_surface, (10, 10))  # Draw iteration count on top
                
                pygame.display.update()  # Update display with iteration count visible
                self.num_updates = 0



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

            for current_iteration in range(self.num_iterations):

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
                    p.update_particle(self.delta)
                self.num_updates += 1

                
                # Render iteration count only at specified intervals
                if current_iteration % update_interval  == 0 or current_iteration == self.num_iterations - 1:
                # if current_iteration % self.refresh_rate  == 0 or current_iteration == self.num_iterations - 1:
                
                    self.screen.fill((0, 0, 0))  # Clear the screen
                    text_surface = font.render(f"Iteration: {current_iteration + 1}/{self.num_iterations}", True, (255, 255, 255))
                    self.screen.blit(text_surface, (10, 10))  # Draw the iteration count text
                    pygame.display.update()  # Update display with iteration count only
        
        else:

            for current_iteration in range(self.num_iterations):

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
                    p.update_particle(self.delta)
                self.num_updates += 1




    def run_simulation_keep_track_of_cluster_size(self, calculation_interval=10):
        """Runs the particle simulation while keeping track of cluster size at specified intervals."""
        
        records_df = pd.DataFrame(columns=['Iteration', 'Cluster Cardinality'])

        for current_iteration in range(self.num_iterations):
            
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
                p.update_particle(self.delta)
            self.num_updates += 1

            # Record cluster size at specified intervals
            if current_iteration % calculation_interval == 0 or current_iteration == self.num_iterations - 1:
                curr_cluster_cardinality = self.get_curr_cluster_cardinality()
                
                # Add the record to DataFrame
                records_df.loc[current_iteration] = [
                    current_iteration,
                    curr_cluster_cardinality,
                ]

        # Save the records to a CSV file
        records_df.to_csv('latest_run_cluster_records.csv', index=False)



















        
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
            


    def get_user_response(self, user_response):
        if user_response == 'r' or user_response == 'R':
            return True
        return False
    

    def get_curr_cluster_cardinality(self):
        """Calculate the cardinality of the cluster starting from the origin or surrounding cells."""
        
        # If the origin has a particle, start the search from the origin
        if self.board[self.origin_x, self.origin_y] == 1:
            queue = [(self.origin_x, self.origin_y)]
        else:
            # Otherwise, check for particles in the neighboring cells
            queue = [
                (self.origin_x + dx, self.origin_y + dy)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),  # N, S, E, W
                               (1, 1), (-1, -1), (1, -1), (-1, 1)  # NE, NW, SE, SW
                                                                    ]  # Adjacent and diagonal cells only
                if 0 <= self.origin_x + dx < self.width and 0 <= self.origin_y + dy < self.height
                and self.board[self.origin_x + dx, self.origin_y + dy] == 1
            ]
            
            # If no neighbors have particles, return 0 (no cluster)
            if not queue:
                return 0

        # Initialize BFS/DFS
        visited = set(queue)
        length = 0

        # Directions for North, South, East, West
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # N, S, E, W
            # (1, 1), (-1, -1), (1, -1), (-1, 1)  # NE, NW, SE, SW
        ]

        # Perform BFS/DFS
        while queue:
            x, y = queue.pop(0)  # Use queue.pop() if DFS is preferred
            length += 1  # Count this particle

            # Check all adjacent positions
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Ensure the neighbor is within bounds
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Check if the neighbor has a particle and hasn't been visited
                    if self.board[nx, ny] == 1 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))  # Mark as visited

        return length


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








    # def get_curr_radius_euclidean_length(self):
    #     """Returns the radius (maximum distance) of the continuous stream of particles starting from the origin."""
    #     # Check if there's a particle at the origin
    #     if self.board[self.origin_x, self.origin_y] == 0:
    #         return 0  # No particle at the origin
        
    #     # Initialize queue for BFS
    #     queue = [(self.origin_x, self.origin_y)]
    #     visited = set(queue)  # To keep track of visited positions
    #     max_radius = 1

    #     # Define directions for all 8 possible neighbors
    #     directions = [
    #         (1, 0), (-1, 0), (0, 1), (0, -1),  # N, S, E, W
    #         # (1, 1), (-1, -1), (1, -1), (-1, 1)  # NE, NW, SE, SW
    #     ]

    #     # Perform BFS to find all connected particles
    #     while queue:
    #         x, y = queue.pop(0)  # Use queue.pop() if DFS is preferred

    #         # Calculate Euclidean distance from the origin
    #         distance = math.sqrt((x - self.origin_x) ** 2 + (y - self.origin_y) ** 2)
    #         max_radius = max(max_radius, distance)  # Update max radius if this is the farthest particle

    #         # Check all adjacent positions
    #         for dx, dy in directions:
    #             nx, ny = x + dx, y + dy

    #             # Ensure the neighbor is within bounds
    #             if 0 <= nx < self.width and 0 <= ny < self.height:
    #                 # Check if the neighbor has a particle and hasn't been visited
    #                 if self.board[nx, ny] == 1 and (nx, ny) not in visited:
    #                     queue.append((nx, ny))
    #                     visited.add((nx, ny))  # Mark as visited

    #     return max_radius

    # def get_curr_radius_manhattan_length(self):

    #     if self.board[self.origin_x, self.origin_y] == 0:
    #         return 0  # No particle at the origin
        
    #     # Initialize queue for BFS
    #     queue = [(self.origin_x, self.origin_y)]
    #     visited = set(queue)  # To keep track of visited positions
    #     max_radius = 1

    #     # Define directions for all 8 possible neighbors
    #     directions = [
    #         (1, 0), (-1, 0), (0, 1), (0, -1),  # N, S, E, W
    #     ]

    #     # Perform BFS to find all connected particles
    #     while queue:
    #         x, y = queue.pop(0)

    #         # Calculate Manhattan distance from the origin
    #         distance = abs(x - self.origin_x) + abs(y - self.origin_y)
    #         max_radius = max(max_radius, distance)  # Update max radius if this is the farthest particle

    #         # Check all adjacent positions
    #         for dx, dy in directions:
    #             nx, ny = x + dx, y + dy

    #             # Ensure the neighbor is within bounds
    #             if 0 <= nx < self.width and 0 <= ny < self.height:
    #                 # Check if the neighbor has a particle and hasn't been visited
    #                 if self.board[nx, ny] == 1 and (nx, ny) not in visited:
    #                     queue.append((nx, ny))
    #                     visited.add((nx, ny))  # Mark as visited

    #     return max_radius


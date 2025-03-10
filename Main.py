from ParticleSystem import ParticleSystem
import pandas as pd

WORLD_WIDTH = 300 # 200 # 20
WORLD_HEIGHT = 100 # 200 # 20
DELTA = 0.0001 # 0.001 # 0.01 # 0.1 # probability to change direction
MU = 0.4 # density
EPSILON = 0.9 # probability to just follow the nomral direction for one iteration (and not randomly move)
ALPHA = 0.8 # probability to be an active (normal) particle
DOT_SIZE = 5 # 4
MIDDLE_CLUSTER_SIZE = -1 # 10
NUM_ITERATIONS =  10 ** 18 # None # 10000
INIT_REFRESH_RATE = 10 # 100
INIT_PAUSED_STATUS = True
DIRECTION_WEIGHTS = [0.1, # right
                     0.11, # down
                     0.1, # left
                     1111  # up
                     ]

running = True
# total_runs = 0
# df = pd.DataFrame(columns=['Run', 'Cluster Cardinality', 'Radius Manhattan Length', 'Radius Euclidean Length'])

while running:
    # total_runs += 1

    world = ParticleSystem(
        WORLD_WIDTH,
        WORLD_HEIGHT,
        DELTA,
        MU,
        EPSILON, 
        ALPHA,
        DOT_SIZE,
        MIDDLE_CLUSTER_SIZE,
        NUM_ITERATIONS,
        INIT_REFRESH_RATE,
        INIT_PAUSED_STATUS

        # , direction_weights=DIRECTION_WEIGHTS
    )

    world.run_simulation()
    # world.run_simulation_calculations_only(render_iterations=True)
    # world.run_simulation_keep_track_of_cluster_size()

    # curr_radius_euclidean_length = world.get_curr_radius_euclidean_length()
    # curr_radius_manhattan_length = world.get_curr_radius_manhattan_length()
    
    # # curr_cluster_cardinality = world.get_curr_cluster_cardinality()
    # curr_cluster_cardinality = world.get_ring_cluster_cardinality()

    # print(f'Total runs: {total_runs}')
    # print(f'Current radius Euclidean length: {curr_radius_euclidean_length}')
    # print(f'Current cluster cardinality: {curr_cluster_cardinality}')
    # print(f'Current radius Manhattan length: {curr_radius_manhattan_length}')

    # # Update DataFrame with results of this run
    # df.loc[total_runs] = [
    #     total_runs,
    #     curr_cluster_cardinality,
    #     curr_radius_manhattan_length,
    #     curr_radius_euclidean_length
    # ]
    
    user_input = input('Press R to restart the simulation. Press any other key to stop:  ')

    # This will set running to either True or False based on the user's input if they want to re-run or not
    running = world.get_user_response(user_input)
    
# Saving results
# df.to_csv('latest_simulation_results.csv', index=False)

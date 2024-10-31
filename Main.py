# from ParticleSystem import ParticleSystem
from trial import ParticleSystem
import pandas as pd

WORLD_WIDTH = 90 # 200 # 20
WORLD_HEIGHT = 90 # 200 # 20
DELTA = 0.1 # probability to move or not to move
MU = 0.3 # density
DOT_SIZE = 10 # 4
NUM_ITERATIONS = 10000
INIT_REFRESH_RATE = 100

running = True
total_runs = 0
df = pd.DataFrame(columns=['Run', 'Cluster Cardinality', 'Radius Manhattan Length', 'Radius Euclidean Length'])

while running:
    
    total_runs += 1

    world = ParticleSystem(
        WORLD_WIDTH,
        WORLD_HEIGHT,
        DELTA,
        MU,
        DOT_SIZE,
        NUM_ITERATIONS,
        INIT_REFRESH_RATE
    )

    world.run_simulation()

    curr_radius_euclidean_length = world.get_curr_radius_euclidean_length()
    curr_radius_manhattan_length = world.get_curr_radius_manhattan_length()
    curr_cluster_cardinality = world.get_curr_cluster_cardinality()

    print(f'Total runs: {total_runs}')
    print(f'Current radius Euclidean length: {curr_radius_euclidean_length}')
    print(f'Current cluster cardinality: {curr_cluster_cardinality}')
    print(f'Current radius Manhattan length: {curr_radius_manhattan_length}')

    # Update DataFrame with results of this run
    df.loc[total_runs] = [
        total_runs,
        curr_cluster_cardinality,
        curr_radius_manhattan_length,
        curr_radius_euclidean_length
    ]
    
    user_input = input('Press R to restart the simulation. Press any other key to stop:  ')


    running = world.get_user_response(user_input)
    

# Optionally, save the DataFrame to a CSV after all runs
df.to_csv('simulation_results.csv', index=False)
print("Simulation results saved to 'simulation_results.csv'")


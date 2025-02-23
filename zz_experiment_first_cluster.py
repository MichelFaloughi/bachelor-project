# How many itereations before one cluster happends
from ParticleSystem import ParticleSystem
import pandas as pd

WORLD_WIDTH = 200 # 90 # 200 # 20
WORLD_HEIGHT = 200 # 90 # 200 # 20
DELTA = 0.001 # 0.001 # 0.01 # 0.1 # probability to change direction
MU = 0.5 # density
EPSILON = 0.99 # probability to just follow the nomral direction for one iteration (and not randomly move)
ALPHA = 0.99 # probability to be an active (normal) particle
DOT_SIZE = 2 # 10 # 4
MIDDLE_CLUSTER_SIZE = -1 # 10
NUM_ITERATIONS =  100000000000000000000 # None # 10000
INIT_REFRESH_RATE = 10 # 100
INIT_PAUSED_STATUS = False

df = pd.DataFrame(columns=["Run ID", "num iterations"])

for i in range(200):

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
    )

    num_iterations_it_took = world.run_simulation_get_iteration_of_first_single_cluster(

        refresh_rate=100, check_rate=60000, init_render_status=True, first_check=200000
        
        )
    

    df.loc[len(df)] = [world.id, num_iterations_it_took] # adds to the df

    print(f'finished iteration: {i}')


# UNCOMMENT TO SAVE RESULTS, BEWARE OF OVERWRITING
    df.to_excel(f'M{MU}D{DELTA}E{EPSILON}A{ALPHA}_{WORLD_WIDTH}x{WORLD_HEIGHT}_first_cluster.xlsx')
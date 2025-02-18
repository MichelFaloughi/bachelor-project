from ParticleSystem import ParticleSystem
import pandas as pd

WORLD_WIDTH = 200 # 90 # 200 # 20
WORLD_HEIGHT = 100 # 90 # 200 # 20
DELTA = 0.001 # 0.001 # 0.01 # 0.1 # probability to change direction
MU = 0.4 # density
EPSILON = 0.99 # probability to just follow the nomral direction for one iteration (and not randomly move)
ALPHA = 0.99 # probability to be an active (normal) particle
DOT_SIZE = 4 # 10 # 4
MIDDLE_CLUSTER_SIZE = -1 # 10
NUM_ITERATIONS =  100000000000000000000 # None # 10000
INIT_REFRESH_RATE = 10 # 100
INIT_PAUSED_STATUS = False


running = True
while running:

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

    world.run_simulation()
    
    user_input = input('Press R to restart the simulation. Press any other key to stop:  ')

    # This will set running to either True or False based on the user's input if they want to re-run or not
    running = world.get_user_response(user_input)

cluster_sizes = world.get_curr_cluster_sizes()


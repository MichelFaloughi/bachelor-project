from ParticleSystem import ParticleSystem
import pandas as pd
import numpy as np 

WORLD_WIDTH = 300 # 90 # 200 # 20
WORLD_HEIGHT = 300 # 90 # 200 # 20
DELTA = 0.0001 # 0.001 # 0.01 # 0.1 # probability to change direction
MUS = np.arange(0.1, 0.7, 0.1)  
EPSILON = 0.9 # probability to just follow the nomral direction for one iteration (and not randomly move)
ALPHA = 0.8 # probability to be an active (normal) particle
DOT_SIZE = 3 # 10 # 4
MIDDLE_CLUSTER_SIZE = -1 # 10
NUM_ITERATIONS =  100000000000000000000 # None # 10000
INIT_REFRESH_RATE = 10 # 100
INIT_PAUSED_STATUS = False

results = []

for MU in MUS:

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

    T = world.run_simulation()

    results.append({'mu': MU, 'T': T})
    print(f'Done for mu = {MU}, T = {T}')

results_df = pd.DataFrame(results)

results_df.to_csv('latest_latest_run.csv')
# For now, we don't have epsilon, delta, alpha, etc. only mu
from OneDimensionalParticleSystem import OneDimensionalParticleSystem
import pandas as pd

WORLD_N = 25000
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
MU = 0.6
DELTA = 0.001
EPSILON = 0.9 # probability to just follow the nomral direction for one iteration (and not randomly move)
ALPHA = 0.8 # probability to be an active (normal) particle
DOT_SIZE = 7
NUM_ITERATIONS = 10 ** 10
INIT_REFRESH_RATE = 30
INIT_PAUSED_STATUS = True
IS_REDENRING = True
INIT_ONE_STEP_MODE = False

running = True
while running: 

    world = OneDimensionalParticleSystem(
        WORLD_N,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        MU,
        DELTA,
        EPSILON,
        ALPHA,
        DOT_SIZE,
        NUM_ITERATIONS,
        INIT_REFRESH_RATE,
        INIT_PAUSED_STATUS,
        IS_REDENRING,
        INIT_ONE_STEP_MODE
    )

    world.run_simulation()
    running = False
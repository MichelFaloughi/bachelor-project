# For now, we don't have epsilon, delta, alpha, etc. only mu
from OneDimensionalParticleSystem import OneDimensionalParticleSystem
import pandas as pd

WORLD_N = 4500
SCREEN_WIDTH = 90
SCREEN_HEIGHT = 90
MU = 0.4
DELTA = 0.0001
EPSILON = 0.9 # probability to just follow the nomral direction for one iteration (and not randomly move)
ALPHA = 0.8 # probability to be an active (normal) particle
DOT_SIZE = 7
NUM_ITERATIONS = 1000000000
INIT_REFRESH_RATE = 1000
INIT_PAUSED_STATUS = False
IS_REDENRING = True


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
        IS_REDENRING
    )

    world.run_simulation()
    running = False
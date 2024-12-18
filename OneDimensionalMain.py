# For now, we don't have epsilon, delta, alpha, etc. only mu
from OneDimensionalParticleSystem import OneDimensionalParticleSystem
import pandas as pd

WORLD_N = 300000
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 1000
MU = 0.4
DOT_SIZE = 3
NUM_ITERATIONS = 100000
INIT_REFRESH_RATE = 10
INIT_PAUSED_STATUS = False

running = True
while running:

    world = OneDimensionalParticleSystem(
        WORLD_N,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        MU,
        DOT_SIZE,
        NUM_ITERATIONS,
        INIT_REFRESH_RATE,
        INIT_PAUSED_STATUS
    )

    world.run_simulation()
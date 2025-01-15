# For now, we don't have epsilon, delta, alpha, etc. only mu
from OneDimensionalParticleSystem import OneDimensionalParticleSystem
import pandas as pd

WORLD_N = 300000
SCREEN_WIDTH = 90
SCREEN_HEIGHT = 90
MU = 0.4
DELTA = 0.1
DOT_SIZE = 10
NUM_ITERATIONS = 100000
INIT_REFRESH_RATE = 1000
INIT_PAUSED_STATUS = False

running = True
while running:

    world = OneDimensionalParticleSystem(
        WORLD_N,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        MU,
        DELTA,
        DOT_SIZE,
        NUM_ITERATIONS,
        INIT_REFRESH_RATE,
        INIT_PAUSED_STATUS
    )

    world.run_simulation()
    running = False
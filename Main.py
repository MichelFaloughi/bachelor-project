# from ParticleSystem import ParticleSystem
from trial import ParticleSystem

WORLD_WIDTH = 90 # 200 # 20
WORLD_HEIGHT = 90 # 200 # 20
DELTA = 0.1 # probability to move or not to move
MU = 0.3 # density
DOT_SIZE = 10 # 4
NUM_ITERATIONS = 10000




world = ParticleSystem(
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DELTA,
    MU,
    DOT_SIZE,
    NUM_ITERATIONS
)

world.run_simulation()







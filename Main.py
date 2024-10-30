# from ParticleSystem import ParticleSystem
from trial import ParticleSystem

WORLD_WIDTH = 90 # 200 # 20
WORLD_HEIGHT = 90 # 200 # 20
DELTA = 0.1
MU = 0.3
DOT_SIZE = 10 # 4

world = ParticleSystem(
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DELTA,
    MU,
    DOT_SIZE
)

world.run_simulation()







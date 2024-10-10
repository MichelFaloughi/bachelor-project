from ParticleSystem import ParticleSystem

WORLD_WIDTH = 200
WORLD_HEIGHT = 200
DELTA = 0.1
MU = 0.1
DOT_SIZE = 4


world = ParticleSystem(
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DELTA,
    MU,
    DOT_SIZE
)

world.run_simulation()

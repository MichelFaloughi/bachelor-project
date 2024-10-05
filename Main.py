from ParticleSystem import ParticleSystem

WORLD_WIDTH = 300
WORLD_HEIGHT = 300
DELTA = 0.1
MU = 0.01

world = ParticleSystem(
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DELTA,
    MU
)

world.run_simulation()

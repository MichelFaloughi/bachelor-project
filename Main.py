from ParticleSystem import ParticleSystem

WORLD_WIDTH = 800
WORLD_HEIGHT = 600
DELTA = 0.5
MU = 0.01

world = ParticleSystem(
    WORLD_WIDTH,
    WORLD_HEIGHT,
    DELTA,
    MU
)

world.run_simulation()

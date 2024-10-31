# from ParticleSystem import ParticleSystem
from trial import ParticleSystem

running = True

while running:

    WORLD_WIDTH = 90 # 200 # 20
    WORLD_HEIGHT = 90 # 200 # 20
    DELTA = 0.1 # probability to move or not to move
    MU = 0.3 # density
    DOT_SIZE = 10 # 4
    NUM_ITERATIONS = 20000


    world = ParticleSystem(
        WORLD_WIDTH,
        WORLD_HEIGHT,
        DELTA,
        MU,
        DOT_SIZE,
        NUM_ITERATIONS
    )

    world.run_simulation()

    user_input = input('Press R to restart the simulation. Press any other key to stop it:  ')

    running = world.get_user_response(user_input)
    





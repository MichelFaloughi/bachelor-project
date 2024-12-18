import pygame

class OneDimensionalParticle:

    def __init__(self, x:int, v:int, dot_size:int, board_array, screen):
        self.x = x
        self.height = 10 # fixed could change later
        self.v = v
        self.dot_size = dot_size
        self.board_array = board_array
        self.screen = screen
        
        # Keep track for when I update
        self.previous_x = x
    
    def clear_old_position(self):
        background_color = (0, 0, 0) # Black
        pygame.draw.rect(self.screen, background_color, pygame.Rect(self.previous_x * self.dot_size,
                                                                    self.height * self.dot_size,
                                                                    self.dot_size, self.dot_size))

    def draw(self, screen, color=(255, 255, 255)):
        pygame.draw.rect(screen, color, pygame.Rect(self.x * self.dot_size,
                                                    self.height * self.dot_size,
                                                    self.dot_size, self.dot_size))
        
    def update_particle(self):
        self.previous_x = self.x

        new_x = (self.x + self.v) % len(self.board_array) # make sure len(self.board_array) works

        if self.board_array[new_x] == 0:
            self.board_array[self.x] = 0 # clear old position
            self.x = new_x
            self.board_array[self.x] = 1 # Update board with new position


        # Drawing stuff 
        self.clear_old_position() # only draws a black rectangle, doesn't update board, I do it above
        self.draw(self.screen)

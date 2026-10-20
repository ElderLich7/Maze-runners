import pygame

# --- PYGAME SPRITE CLASSES ---
class WallSprite(pygame.sprite.Sprite):
    """Represents a single structural wall block block."""
    def __init__(self, grid_x, grid_y, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * size
        self.rect.y = grid_y * size

class PlayerSprite(pygame.sprite.Sprite):
    """Represents the player square entity with internal movement bounds handling."""
    def __init__(self, grid_x, grid_y, size, color):
        super().__init__()
        self.size = size
        self.grid_x = grid_x
        self.grid_y = grid_y
        original_image = pygame.image.load("sprite player.png").convert_alpha()
        
        #cool down for player movement
        self.MOVE_COOLDOWN = 150  
        # Tracker for when the player last moved
        self.last_move_time = 0 
        
        
        #size of the spriterelative to png image
        frame_width = 45
        frame_height = 68

        #each unique frame of the sprite sheet is defined by a rectangle, and then scaled to the desired size
        idle_animation = pygame.Rect( 5 , 8, frame_width, frame_height )
        down = [pygame.Rect( 55 , 8, frame_width, frame_height ),pygame.Rect( 162 , 8, frame_width, frame_height )]
        up = [pygame.Rect( 50 , 233, frame_width, frame_height ),pygame.Rect( 160 , 235, frame_width, frame_height )]
        left = [pygame.Rect( 55 , 84, frame_width, frame_height ),pygame.Rect( 162 , 84, frame_width, frame_height )]
        right = [pygame.Rect( 55 , 166, frame_width, frame_height ),pygame.Rect( 158 , 166, frame_width, frame_height )]

        #define the frames for each direction and scale them to the desired size
        self.frames = {"idle": idle_animation, "down": down, "up": up, "left": left, "right": right}
        for all_frames in self.frames:
            if all_frames != "idle":
                for i in range(len(self.frames[all_frames])):
                    self.frames[all_frames][i] = original_image.subsurface(self.frames[all_frames][i])
                    self.frames[all_frames][i] = pygame.transform.scale(self.frames[all_frames][i], (self.grid_x * self.size, self.grid_y * self.size))
        
        #define the idle frame and scale it to the desired size           
        self.frames["idle"] = original_image.subsurface(idle_animation)
        self.frames["idle"] = pygame.transform.scale(self.frames["idle"], (self.grid_x * self.size, self.grid_y * self.size))
        
        self.current_frame = self.frames["idle"]
        self.cycle_index = 0
        self.last_direction = self.frames["idle"]

    # Updates the current frame of the player sprite based on the direction of movement
    def update_frame(self  , direction = "idle"):
            self.cycle_index += 1
            if self.last_direction != direction:
                            self.cycle_index = 0
                            self.last_direction = direction
            if direction != "idle":
                self.current_frame = self.frames[direction][self.cycle_index % 2]
            else:
                self.current_frame = self.frames["idle"]
            self.image = self.current_frame
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.grid_x * self.size, self.grid_y * self.size)
            self.set_grid_position(self.grid_x, self.grid_y)

    # Sets the grid position of the player sprite and updates its pixel position accordingly 
    def set_grid_position(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect.x = grid_x * self.size
        self.rect.y = grid_y * self.size

    # Moves the player sprite in the specified direction if the target cell is walkable (0) in the maze matrix
    def move(self, dx, dy, maze_matrix):
        # Calculate tentative grid target space
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        # Check against matrix data boundaries (0 = walkable path)
        if maze_matrix[new_y][new_x] == 0:
            self.set_grid_position(new_x, new_y)



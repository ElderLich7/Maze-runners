import pygame
from sprite_loader import Character_Sprites

frames_loader = Character_Sprites()

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
    def __init__(self, grid_x, grid_y, size , mode):
        super().__init__()
        self.size = size
        self.grid_x = grid_x
        self.grid_y = grid_y
        #cool down for player movement
        self.MOVE_COOLDOWN = 200  
        # Tracker for when the player last moved
        self.last_move_time = 0 
        self.mode = mode
        self.is_moving = False
        self.movement_start_time = 0
        self.movement_start = (grid_x * size, grid_y * size)
        self.movement_target = self.movement_start
        self.movement_direction = "idle"

        if mode == "maze":
            frames_loader.subdivide_sprite_into_frames(grid_x , size , grid_y )
            self.frames = frames_loader.frames
        else :
            frames_loader.load_dungeon_player_sprites(size)
            self.frames = frames_loader.player_walk_frames

        self.current_frame = self.frames["idle"]
        self.cycle_index = 0
        self.last_direction = "idle"
        self.image = self.current_frame[0]
        self.rect = self.image.get_rect(topleft=self.movement_start)

    # Updates the current frame of the player sprite based on the direction of movement
    def update_frame(self  , direction = "idle"):
        if self.last_direction != direction:
            self.cycle_index = 0
            self.last_direction = direction
        self.current_frame = self.frames.get(direction, self.frames["idle"])
        self.image = self.current_frame[self.cycle_index % len(self.current_frame)]

    # Sets the grid position of the player sprite and updates its pixel position accordingly 
    def set_grid_position(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect.x = grid_x * self.size
        self.rect.y = grid_y * self.size
        self.movement_start = self.rect.topleft
        self.movement_target = self.rect.topleft
        self.is_moving = False

    # Moves the player sprite in the specified direction if the target cell is walkable (0) in the maze matrix
    def move(self, dx, dy, maze_matrix, current_time):
        if self.is_moving:
            return False

        # Calculate tentative grid target space
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        # Check against matrix data boundaries (0 = walkable path)
        if not (0 <= new_y < len(maze_matrix) and 0 <= new_x < len(maze_matrix[new_y])):
            return False
        if maze_matrix[new_y][new_x] != 0:
            return False

        if dx < 0:
            direction = "left"
        elif dx > 0:
            direction = "right"
        elif dy < 0:
            direction = "up"
        else:
            direction = "down"

        self.movement_start = self.rect.topleft
        self.movement_target = (new_x * self.size, new_y * self.size)
        self.movement_start_time = current_time
        self.movement_direction = direction
        self.is_moving = True
        self.update_frame(direction)
        return True

    def update_movement(self, current_time):
        if not self.is_moving:
            return

        progress = min((current_time - self.movement_start_time) / self.MOVE_COOLDOWN, 1)
        start_x, start_y = self.movement_start
        target_x, target_y = self.movement_target
        self.rect.topleft = (
            round(start_x + (target_x - start_x) * progress),
            round(start_y + (target_y - start_y) * progress),
        )

        frames = self.current_frame
        self.cycle_index = min(int(progress * len(frames)), len(frames) - 1)
        self.image = frames[self.cycle_index]

        if progress >= 1:
            self.grid_x = round(target_x / self.size)
            self.grid_y = round(target_y / self.size)
            self.is_moving = False

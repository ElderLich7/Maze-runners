from email.mime import image
import sys
import pygame

from settings import Settings
from generator import MazeGenerator

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
        
        
        #size of the spriterelative to png image
        frame_width = 45
        frame_height = 68

        #each unique frame of the sprite sheet is defined by a rectangle, and then scaled to the desired size
        idle_animation = pygame.Rect( 5 , 8, frame_width, frame_height )
        down = [pygame.Rect( 55 , 8, frame_width, frame_height ),pygame.Rect( 162 , 8, frame_width, frame_height )]
        up = [pygame.Rect( 50 , 233, frame_width, frame_height ),pygame.Rect( 160 , 235, frame_width, frame_height )]
        left = [pygame.Rect( 55 , 84, frame_width, frame_height ),pygame.Rect( 162 , 84, frame_width, frame_height )]
        right = [pygame.Rect( 55 , 166, frame_width, frame_height ),pygame.Rect( 158 , 166, frame_width, frame_height )]
        
        self.frames = {"idle": idle_animation, "down": down, "up": up, "left": left, "right": right}
        for all_frames in self.frames:
            if all_frames != "idle":
                for i in range(len(self.frames[all_frames])):
                    self.frames[all_frames][i] = original_image.subsurface(self.frames[all_frames][i])
                    self.frames[all_frames][i] = pygame.transform.scale(self.frames[all_frames][i], (self.grid_x * self.size, self.grid_y * self.size))
                    
        self.frames["idle"] = original_image.subsurface(idle_animation)
        self.frames["idle"] = pygame.transform.scale(self.frames["idle"], (self.grid_x * self.size, self.grid_y * self.size))
        
        self.current_frame = self.frames["idle"]
        self.cycle_index = 0
        self.last_direction = self.frames["idle"]

    def update_frame(self  , direction = "idle"):
            if self.last_direction != direction:
                            self.cycle_index = 0
                            self.last_direction = direction
            if direction != "idle":
                self.current_frame = self.frames[direction][self.cycle_index % 2]
            self.image = self.current_frame
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.grid_x * self.size, self.grid_y * self.size)
            self.set_grid_position(self.grid_x, self.grid_y)

        
    def set_grid_position(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect.x = grid_x * self.size
        self.rect.y = grid_y * self.size

    def move(self, dx, dy, maze_matrix):
        # Calculate tentative grid target space
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        # Check against matrix data boundaries (0 = walkable path)
        if maze_matrix[new_y][new_x] == 0:
            self.set_grid_position(new_x, new_y)

# --- WINDOW CONFIGURATION ---
TILE_SIZE = 55
MAZE_WIDTH = 15   
MAZE_HEIGHT = 15  

SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE
SCREEN_HEIGHT = (MAZE_HEIGHT * TILE_SIZE) + 40 

COLOR_WALL = (44, 62, 80)       
COLOR_PATH = (236, 240, 241)     
COLOR_PLAYER = (46, 204, 113)    
COLOR_EXIT = (231, 76, 60)       
COLOR_TEXT = (255, 255, 255)

def build_level_cache(matrix, engine_width, engine_height):
    """Creates wall sprites and bakes them to a flat texture canvas for massive performance gains."""
    wall_group = pygame.sprite.Group()
    
    # Generate structural items
    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            if value == 1:
                wall_sprite = WallSprite(col_idx, row_idx, TILE_SIZE, COLOR_WALL)
                wall_group.add(wall_sprite)
                
    # Bake the sprites permanently to a background plane texture
    bg_surface = pygame.Surface((SCREEN_WIDTH, MAZE_HEIGHT * TILE_SIZE))
    bg_surface.fill(COLOR_PATH) # Default everything to walkable open ground paths
    wall_group.draw(bg_surface) # Stamp the structural wall images right on top
    
    return bg_surface, wall_group

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Procedural Sprite Maze Playground")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16, bold=True)
    
    # Engine state setup
    engine = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
    current_difficulty = "medium"
    maze = engine.generate(current_difficulty)
    
    # Bake current maze into graphic assets
    background_surface, wall_group = build_level_cache(maze, MAZE_WIDTH, MAZE_HEIGHT)
    
    # Initialize Player Sprite
    player = PlayerSprite(1, 1, TILE_SIZE, COLOR_PLAYER)
    player.update_frame()
    all_sprites = pygame.sprite.Group(player)
    
    # Static goal markers
    exit_x, exit_y = MAZE_WIDTH - 2, MAZE_HEIGHT - 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key in (pygame.K_LEFT, pygame.K_a):     
                    dx = -1
                    player.update_frame()
                elif event.key in (pygame.K_RIGHT, pygame.K_d):  
                    dx = 1
                    player.update_frame()
                elif event.key in (pygame.K_UP, pygame.K_w):     
                    dy = -1
                    player.update_frame()
                elif event.key in (pygame.K_DOWN, pygame.K_s):   
                    dy = 1
                    player.update_frame()
                # Use internal sprite logic to evaluate moving into the matrix boundaries
                player.move(dx, dy, maze)
                
                # Regenerate levels if configuration hotkeys are pressed
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    if event.key == pygame.K_1: current_difficulty = "easy"
                    elif event.key == pygame.K_2: current_difficulty = "medium"
                    elif event.key == pygame.K_3: current_difficulty = "hard"
                    
                    maze = engine.generate(current_difficulty)
                    background_surface, wall_group = build_level_cache(maze, MAZE_WIDTH, MAZE_HEIGHT)
                    player.set_grid_position(1, 1)
                    player.current_frame = player.frames["idle"]

        # Win condition evaluation
        if player.grid_x == exit_x and player.grid_y == exit_y:
            maze = engine.generate(current_difficulty)
            background_surface, wall_group = build_level_cache(maze, MAZE_WIDTH, MAZE_HEIGHT)
            player.set_grid_position(1, 1)
            player.current_frame = player.frames["idle"]

        # SCREEN DRAWING SEQUENCE
        screen.fill((30, 30, 30))
        
        # Step 1: Blit the entire pre-baked structural grid instantly 
        screen.blit(background_surface, (0, 0))
        
        # Step 2: Draw target markers
        pygame.draw.rect(screen, COLOR_EXIT, (exit_x * TILE_SIZE, exit_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Step 3: Draw interactive active moving sprite elements
        all_sprites.draw(screen)

        # Step 4: Render UI/HUD text
        hud_surface = font.render(
            f"Difficulty: {current_difficulty.upper()}   |   Regen: Easy(1) Med(2) Hard(3)   |   Move: WASD/Arrows", 
            True, COLOR_TEXT
        )
        screen.blit(hud_surface, (12, MAZE_HEIGHT * TILE_SIZE + 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
import sys 
import pygame

from visual_control import WallSprite, PlayerSprite
class Settings ():

    def __init__(self):
        self.TILE_SIZE = 25
        self.MAZE_WIDTH = 43   
        self.MAZE_HEIGHT = 29  
        self.SCREEN_WIDTH = self.MAZE_WIDTH * self.TILE_SIZE
        self.SCREEN_HEIGHT = (self.MAZE_HEIGHT * self.TILE_SIZE) + 40 
        self.COLOR_WALL = (44, 62, 80)       
        self.COLOR_PATH = (236, 240, 241)     
        self.COLOR_PLAYER = (46, 204, 113)    
        self.COLOR_EXIT = (231, 76, 60)       
        self.COLOR_TEXT = (255, 255, 255)
        self.exit_x = 0
        self.exit_y = 0
        self.camera_type = "world"

        # Speed setting: How many milliseconds must pass between steps (Lower = Faster)

    def create_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Procedural Sprite Maze Playground")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    def background(self ,maze ):
        # Bake current maze into graphic assets
        self.background_surface, self.wall_group = self.build_level_cache(maze, self.MAZE_WIDTH, self.MAZE_HEIGHT)

    def build_level_cache(self,matrix, engine_width, engine_height):
        """Creates wall sprites and bakes them to a flat texture canvas for massive performance gains."""

        wall_group = pygame.sprite.Group()
    
        # Generate structural items
        for row_idx, row in enumerate(matrix):
            for col_idx, value in enumerate(row):
                if value == 1:
                    wall_sprite = WallSprite(col_idx, row_idx, self.TILE_SIZE, self.COLOR_WALL)
                    wall_group.add(wall_sprite)
                
        # Bake the sprites permanently to a background plane texture
        if self.camera_type == "World":
            bg_surface = pygame.Surface((self.SCREEN_WIDTH, self.MAZE_HEIGHT * self.TILE_SIZE))
        else :
            bg_surface = pygame.Surface((engine_width * self.TILE_SIZE,engine_height * self.TILE_SIZE,))
        bg_surface.fill(self.COLOR_PATH) # Default everything to walkable open ground paths
        wall_group.draw(bg_surface) # Stamp the structural wall images right on top
    
        return bg_surface, wall_group

    def camera_settings(self):
        self.VIEW_WIDTH = 800
        self.VIEW_HEIGHT = 600
        self.HUD_HEIGHT = 40
        self.SCREEN_WIDTH = self.VIEW_WIDTH
        self.SCREEN_HEIGHT = self.VIEW_HEIGHT + self.HUD_HEIGHT

    def draw_world_graphics(self , player , engine , current_difficulty ):
        # Win condition evaluation
                if player.grid_x == self.exit_x and player.grid_y == self.exit_y:
                    maze = engine.generate(current_difficulty)
                    background_surface, wall_group = self.build_level_cache(maze, self.MAZE_WIDTH, self.   MAZE_HEIGHT)
                    player.set_grid_position(1, 1)
                    player.update_frame()
        
                # SCREEN DRAWING SEQUENCE
                self.screen.fill((30, 30, 30))
                
                # Step 1: Blit the entire pre-baked structural grid instantly 
                self.screen.blit(self.background_surface, (0, 0))
                
                # Step 2: Draw target markers
                pygame.draw.rect(self.screen, self.COLOR_EXIT, (self.exit_x * self.TILE_SIZE, self.exit_y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                
                # Step 3: Draw interactive active moving sprite elements
                self.all_sprites.draw(self.screen)
        
                # Step 4: Render UI/HUD text
                hud_surface = self.font.render(
                    f"Difficulty: {current_difficulty.upper()}   |   Regen: Easy(1) Med(2) Hard(3)   |   Move: WASD/Arrows", 
                    True, self.COLOR_TEXT
                )
                self.screen.blit(hud_surface, (12, self.MAZE_HEIGHT * self.TILE_SIZE + 10))
        
                pygame.display.flip()
        
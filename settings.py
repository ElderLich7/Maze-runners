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
        # Speed setting: How many milliseconds must pass between steps (Lower = Faster)

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
        bg_surface = pygame.Surface((self.SCREEN_WIDTH, self.MAZE_HEIGHT * self.TILE_SIZE))
        bg_surface.fill(self.COLOR_PATH) # Default everything to walkable open ground paths
        wall_group.draw(bg_surface) # Stamp the structural wall images right on top
    
        return bg_surface, wall_group
        
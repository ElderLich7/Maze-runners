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
        self.current_difficulty = "easy"
        self.mode =  "maze"

        #the exit point of the map
        self.exit_x = 0
        self.exit_y = 0
        self.camera_type = "world"


    #creates the initial display and screen and properties 
    def create_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Procedural Sprite Maze Playground")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    #creates the background of the pygame screen
    def background(self ,maze ):
        # Bake current maze into graphic assets
        self.background_surface, self.wall_group = self.build_level_cache(maze, self.MAZE_WIDTH, self.MAZE_HEIGHT)

    def ui_hud(self):
         self.hud_surface = self.font.render(f"Difficulty: {self.current_difficulty.upper()}    Mode: {self.mode.upper()}   |   Regen: Easy(1) Med(2) Hard(3)    |    Move: WASD/Arrows     |    Mode:  Dungeon(5) Maze(6) ", True, self.COLOR_TEXT  )
         

    #handles building of world and level for better optimization
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
        if self.camera_type == "world":
            bg_surface = pygame.Surface((self.SCREEN_WIDTH, self.MAZE_HEIGHT * self.TILE_SIZE))
        else :
            bg_surface = pygame.Surface((engine_width * self.TILE_SIZE,engine_height * self.TILE_SIZE,))
        bg_surface.fill(self.COLOR_PATH) # Default everything to walkable open ground paths
        wall_group.draw(bg_surface) # Stamp the structural wall images right on top
    
        return bg_surface, wall_group

    #alters the current system to now use camera pov
    def camera_settings(self):
        self.TILE_SIZE = 35
        self.VIEW_WIDTH = 1200
        self.VIEW_HEIGHT = 900
        self.HUD_HEIGHT = 40
        self.SCREEN_WIDTH = self.VIEW_WIDTH
        self.SCREEN_HEIGHT = self.VIEW_HEIGHT + self.HUD_HEIGHT
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def world_settings(self):
        self.SCREEN_WIDTH = self.MAZE_WIDTH * self.TILE_SIZE
        self.SCREEN_HEIGHT = (self.MAZE_HEIGHT * self.TILE_SIZE) + 40 
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    
    #handles drawing to the screen and displaying everything
    def world_pov(self , player , engine ):
        # Win condition evaluation
                if player.grid_x == self.exit_x and player.grid_y == self.exit_y:
                    maze = engine.generate(self.current_difficulty)
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
                
                self.screen.blit(self.hud_surface, (12, self.MAZE_HEIGHT * self.TILE_SIZE + 10))
        
                pygame.display.flip()

    def camera_pov (self , player ):


         # Center the camera on the player, then keep it inside the maze.
        world_width = self.MAZE_WIDTH * self.TILE_SIZE
        world_height = self.MAZE_HEIGHT * self.TILE_SIZE

        camera_x = player.rect.centerx - self.VIEW_WIDTH // 2
        camera_y = player.rect.centery - self.VIEW_HEIGHT // 2

        camera_x = max(0, min(camera_x, max(0, world_width - self.VIEW_WIDTH)))
        camera_y = max(0, min(camera_y, max(0, world_height - self.VIEW_HEIGHT)))

        camera_rect = pygame.Rect( camera_x, camera_y, self.VIEW_WIDTH, self.VIEW_HEIGHT,)

        self.screen.fill((30, 30, 30))

        # Blit only the part of the cached maze visible through the camera.
        self.screen.blit(self.background_surface, (0, 0), camera_rect)

        # Convert the exit's world position to its screen position.
        exit_rect = pygame.Rect( self.exit_x * self.TILE_SIZE - camera_x, self.exit_y * self.TILE_SIZE - camera_y, self.TILE_SIZE, self.TILE_SIZE, )
        pygame.draw.rect(self.screen, self.COLOR_EXIT, exit_rect)

        # Convert the player's world position to its screen position.
        self.screen.blit( player.image, (player.rect.x - camera_x, player.rect.y - camera_y),)

        # Keep the HUD in place rather than making it scroll with the maze.
        pygame.draw.rect( self.screen, (30, 30, 30), (0, self.VIEW_HEIGHT, self.SCREEN_WIDTH, self.HUD_HEIGHT),)
        self.screen.blit(self.hud_surface, (12, self.VIEW_HEIGHT + 10))
        pygame.display.flip()

        
        
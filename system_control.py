import sys 
import pygame

from player_walls_sprites import WallSprite, PlayerSprite

#stores display and screen settings and manages displayy presets
class Settings ():
    '''Manages display and screen settings, handles rendering, and provides utility methods for the maze game using pygame.'''
    def __init__(self):
        """
        Initialize the Settings object with default display, maze, and color parameters.

        Attributes:
            TILE_SIZE (int): Size of one tile in the game.
            MAZE_WIDTH (int): Width of the maze in tiles.
            MAZE_HEIGHT (int): Height of the maze in tiles.
            SCREEN_WIDTH (int): Width of the game screen in pixels.
            SCREEN_HEIGHT (int): Height of the game screen in pixels.
            COLOR_WALL (tuple): RGB color for walls.
            COLOR_PATH (tuple): RGB color for paths.
            COLOR_PLAYER (tuple): RGB color for the player.
            COLOR_EXIT (tuple): RGB color for the exit.
            COLOR_TEXT (tuple): RGB color for text.
            current_difficulty (str): Current maze difficulty.
            mode (str): Current game mode.
            dungeon_level (int): Current dungeon level.
            exit_x (int): X-coordinate of the maze exit.
            exit_y (int): Y-coordinate of the maze exit.
            camera_type (str): Camera view type ("world" or "player").
        """

        self.TILE_SIZE = 25                                         #size of 1 tile in game e.g player / wall
        self.MAZE_WIDTH = 43                                        
        self.MAZE_HEIGHT = 29   
        self.SCREEN_WIDTH = self.MAZE_WIDTH * self.TILE_SIZE           
        self.SCREEN_HEIGHT = (self.MAZE_HEIGHT * self.TILE_SIZE) + 40 
        self.COLOR_WALL = (44, 62, 80)       
        self.COLOR_PATH = (236, 240, 241)     
        self.COLOR_PLAYER = (46, 204, 113)    
        self.COLOR_EXIT = (231, 76, 60)       
        self.COLOR_TEXT = (255, 255, 255)
        self.current_difficulty = "easy"                            #maze difficulty
        self.mode =  "maze"                                         #game mode currently loaded
        self.dungeon_level = 1

        #the exit coordinates of the map
        self.exit_x = 0
        self.exit_y = 0
        self.camera_type = "world"                                  #game view seen : "world" see entire maze displayed , "player" camera fixed and zoomed in on player

        # Runtime resources are initialized when the display and maze are created.
        self.screen = None
        self.clock = None
        self.font = None
        self.hud_surface = None
        self.background_surface = None
        self.wall_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.maze = None
        self.engine = None


    def create_display(self):
        """Initialize the pygame display, set the screen caption, and store the clock and font for rendering."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Procedural Sprite Maze Playground")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    def set_background(self ):
        """creates the background of the pygame screen"""
        # Bake current maze into graphic assets
        self.background_surface, self.wall_group = self.build_level_cache(self.maze, self.MAZE_WIDTH, self.MAZE_HEIGHT)

    def ui_hud(self):
        """ handles the ui drawn onto the screen """
        if self.mode == "maze":
            self.hud_surface = self.font.render(f"Difficulty: {self.current_difficulty.upper()}    Mode: {self.mode.upper()}   |   Regen: Easy(1) Med(2) Hard(3)    |    Move: WASD/Arrows     |    Mode:  Dungeon(5) Maze(6) ", True, self.COLOR_TEXT  )
        elif self.mode == "dungeon":
            self.hud_surface = self.font.render(f"Difficulty: {self.current_difficulty.upper()}    Mode: {self.mode.upper()}   |   Regen: Easy(1) Med(2) Hard(3)    |    Move: WASD/Arrows     |    Mode:  Dungeon(5) Maze(6) ", True, self.COLOR_TEXT  )
    
         

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

    def camera_settings(self):
        ''''''
        self.TILE_SIZE = 45
        self.VIEW_WIDTH = 1200
        self.VIEW_HEIGHT = 900
        self.HUD_HEIGHT = 40
        self.SCREEN_WIDTH = self.VIEW_WIDTH
        self.SCREEN_HEIGHT = self.VIEW_HEIGHT + self.HUD_HEIGHT
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def world_settings(self):
        self.TILE_SIZE = 25                                         #size of 1 tile in game e.g player / wall
        self.MAZE_WIDTH = 43                                        
        self.MAZE_HEIGHT = 29
        self.SCREEN_WIDTH = self.MAZE_WIDTH * self.TILE_SIZE
        self.SCREEN_HEIGHT = (self.MAZE_HEIGHT * self.TILE_SIZE) + 40 
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    
    #handles drawing to the screen and displaying everything
    def world_pov(self , player  ):
        # Win condition evaluation
                if player.grid_x == self.exit_x and player.grid_y == self.exit_y:
                    self.maze = self.engine.generate(self.current_difficulty)
                    self.background_surface, self.wall_group = self.build_level_cache(self.maze, self.MAZE_WIDTH, self.   MAZE_HEIGHT)
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

        
        
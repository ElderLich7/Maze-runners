import sys
import pygame
import random

from system_control import Settings
from maze_gen import MazeGenerator
from player_walls_sprites import PlayerSprite
from dungeon_gen import DungeonGenerator
from game_controls import Controller

# --- WINDOW CONFIGURATION ---
ai_settings = Settings()
def main():

    ai_settings.create_display()
    
    
    # Engine state setup
    maze_engine = MazeGenerator(ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)
    dungeon_engine = DungeonGenerator(ai_settings.MAZE_WIDTH , ai_settings.MAZE_HEIGHT )

    # Default to maze generation; can switch to dungeon_engine if desired
    ai_settings.engine = maze_engine  
    ai_settings.maze =ai_settings.engine.generate(ai_settings.current_difficulty)

    ai_settings.set_background()
    
    # Initialize Player Sprite
    player = PlayerSprite(1, 1, ai_settings.TILE_SIZE, ai_settings.COLOR_PLAYER ,ai_settings.mode)
    player.update_frame()
    ai_settings.all_sprites = pygame.sprite.Group(player)
    
    # Static goal markers
    ai_settings.exit_x, ai_settings.exit_y = ai_settings.MAZE_WIDTH - 2, ai_settings.MAZE_HEIGHT - 2
    game_controls = Controller()
    dungeon_map_size = [ 29 , 29]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN and event.key in ( pygame.K_1 , pygame.K_2 , pygame.K_3 ,pygame.K_5 , pygame.K_6):
                if event.key in ( pygame.K_1 , pygame.K_2 , pygame.K_3 ) :
                    if ai_settings.mode == "maze":
                        game_controls.maze_controls( event , ai_settings )
                        ai_settings.maze = ai_settings.engine.generate(ai_settings.current_difficulty , random.randrange(0,5))
                    
                elif event.key in ( pygame.K_5 , pygame.K_6) :
                    if event.key == pygame.K_5:
                        ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT = dungeon_map_size
                        dungeon_engine = DungeonGenerator(ai_settings.MAZE_WIDTH , ai_settings.MAZE_HEIGHT )
                        ai_settings.engine = dungeon_engine
                        ai_settings.mode = "dungeon"
                        ai_settings.camera_type = 'player'
                        ai_settings.camera_settings()
                        
                        player = PlayerSprite(1, 1, ai_settings.TILE_SIZE, ai_settings.COLOR_PLAYER , ai_settings.mode )
                        player.update_frame()
                        ai_settings.all_sprites = pygame.sprite.Group(player)
                        ai_settings.exit_x, ai_settings.exit_y = ai_settings.MAZE_WIDTH - 2, ai_settings.MAZE_HEIGHT - 2  
                        ai_settings.maze = dungeon_engine.generate(ai_settings.current_difficulty , 3 , 3 , 6)


                    elif event.key == pygame.K_6:
                        ai_settings.engine = maze_engine
                        ai_settings.mode  = "maze"
                        ai_settings.world_settings()
                        ai_settings.camera_type = 'world'
                        player = PlayerSprite(1, 1, ai_settings.TILE_SIZE, ai_settings.COLOR_PLAYER , ai_settings.mode )
                        player.update_frame()
                        ai_settings.all_sprites = pygame.sprite.Group(player)
                        ai_settings.exit_x, ai_settings.exit_y = ai_settings.MAZE_WIDTH - 2, ai_settings.MAZE_HEIGHT - 2  
                        ai_settings.maze = dungeon_engine.generate(ai_settings.current_difficulty , 3 , 3 , 6)
                        
                        
                        ai_settings.maze = ai_settings.engine.generate(ai_settings.current_difficulty)
    
                ai_settings.background_surface, ai_settings.wall_group = ai_settings.build_level_cache( ai_settings.maze , ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)                            
                player.set_grid_position(1, 1)
                player.update_frame()
                    
                    
        current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        game_controls.movement_controls( keys, player, current_time, ai_settings.maze , dx , dy )
        player.update_movement(current_time)
        ai_settings.ui_hud()

        if ai_settings.camera_type == "world":
            ai_settings.world_pov(player)

        elif ai_settings.camera_type == "player":
            ai_settings.camera_pov(player)

        # Limit the frame rate to 60 FPS
        ai_settings.clock.tick(60)

if __name__ == "__main__":
    main()
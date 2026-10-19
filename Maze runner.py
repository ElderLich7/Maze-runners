from email.mime import image
import sys
import pygame

from display_control import Settings
from maze_gen import MazeGenerator
from visual_control import PlayerSprite
from dungeon_gen import DungeonGenerator

# --- WINDOW CONFIGURATION ---
ai_settings = Settings()
def main():

    ai_settings.create_display()
    
    
    # Engine state setup
    maze_engine = MazeGenerator(ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)
    dungeon_engine = DungeonGenerator(ai_settings.MAZE_WIDTH , ai_settings.MAZE_HEIGHT )

    # Default to maze generation; can switch to dungeon_engine if desired
    engine = maze_engine  
    maze =engine.generate(ai_settings.current_difficulty)

    ai_settings.background(maze)
    
    # Initialize Player Sprite
    player = PlayerSprite(1, 1, ai_settings.TILE_SIZE, ai_settings.COLOR_PLAYER)
    player.update_frame()
    ai_settings.all_sprites = pygame.sprite.Group(player)
    
    # Static goal markers
    ai_settings.exit_x, ai_settings.exit_y = ai_settings.MAZE_WIDTH - 2, ai_settings.MAZE_HEIGHT - 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                
                # Regenerate levels if configuration hotkeys are pressed
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3 , pygame.K_5 , pygame.K_6 ):
                    if event.key == pygame.K_1: ai_settings.current_difficulty = "easy"
                    elif event.key == pygame.K_2: ai_settings.current_difficulty = "medium"
                    elif event.key == pygame.K_3: ai_settings.current_difficulty = "hard"
                    elif event.key == pygame.K_5:

                        engine ,ai_settings.mode = dungeon_engine , "dungeon"
                        ai_settings.camera_type = 'player'
                        ai_settings.camera_settings()
                        player = PlayerSprite(1, 1, ai_settings.TILE_SIZE, ai_settings.COLOR_PLAYER)
                        player.update_frame()
                        ai_settings.all_sprites = pygame.sprite.Group(player)
                        ai_settings.exit_x, ai_settings.exit_y = ai_settings.MAZE_WIDTH - 2, ai_settings.MAZE_HEIGHT - 2

                    elif event.key == pygame.K_6:
                        engine ,ai_settings.mode  = maze_engine , "maze"
                        ai_settings.world_settings()
                        ai_settings.camera_type = 'world'

                    maze = engine.generate(ai_settings.current_difficulty)
                    ai_settings.background_surface, ai_settings.wall_group = ai_settings.build_level_cache(maze, ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)
                    
                    player.set_grid_position(1, 1)
                    player.update_frame()


        current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # ONLY process movement if the cooldown period has ended
        if current_time - player.last_move_time >= player.MOVE_COOLDOWN:
    
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx, dy = -1, 0
                player.update_frame("left")
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx, dy = 1, 0
                player.update_frame("right")
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                dx, dy = 0, -1
                player.update_frame("up")
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dx, dy = 0, 1
                player.update_frame("down")

            # If the player is actively pressing a key and trying to move
            if dx != 0 or dy != 0:
                player.move(dx, dy, maze)
        
                # Reset the timer to lock out movement until the next cooldown window
                player.last_move_time = current_time

        ai_settings.ui_hud()

        if ai_settings.camera_type == "world":
            ai_settings.world_pov(player , engine)

        elif ai_settings.camera_type == "player":
            ai_settings.camera_pov(player)

        ai_settings.clock.tick(60)

if __name__ == "__main__":
    main()
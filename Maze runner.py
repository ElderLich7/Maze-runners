from email.mime import image
import sys
import pygame

from settings import Settings
from maze_gen import MazeGenerator
from visual_control import WallSprite, PlayerSprite
from dungeon_gen import DungeonGenerator

# --- WINDOW CONFIGURATION ---
ai_settings = Settings()
def main():
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.SCREEN_WIDTH, ai_settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Procedural Sprite Maze Playground")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16, bold=True)
    
    # Engine state setup
    maze_engine = MazeGenerator(ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)
    dungeon_engine = DungeonGenerator(ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)

    # Default to maze generation; can switch to dungeon_engine if desired
    engine = maze_engine  
    current_difficulty = "medium"
    maze =engine.generate(current_difficulty)
    
    # Bake current maze into graphic assets
    background_surface, wall_group = ai_settings.build_level_cache(maze, ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)
    
    # Initialize Player Sprite
    player = PlayerSprite(1, 1, ai_settings.TILE_SIZE, ai_settings.COLOR_PLAYER)
    player.update_frame()
    all_sprites = pygame.sprite.Group(player)
    
    # Static goal markers
    exit_x, exit_y = ai_settings.MAZE_WIDTH - 2, ai_settings.MAZE_HEIGHT - 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                
                # Regenerate levels if configuration hotkeys are pressed
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3 , pygame.K_5 , pygame.K_6):
                    if event.key == pygame.K_1: current_difficulty = "easy"
                    elif event.key == pygame.K_2: current_difficulty = "medium"
                    elif event.key == pygame.K_3: current_difficulty = "hard"
                    elif event.key == pygame.K_5: engine = dungeon_engine
                    elif event.key == pygame.K_6: engine = maze_engine

                    maze = engine.generate(current_difficulty)
                    background_surface, wall_group = ai_settings.build_level_cache(maze, ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)
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

        # Win condition evaluation
        if player.grid_x == exit_x and player.grid_y == exit_y:
            maze = engine.generate(current_difficulty)
            background_surface, wall_group = ai_settings.build_level_cache(maze, ai_settings.MAZE_WIDTH, ai_settings.   MAZE_HEIGHT)
            player.set_grid_position(1, 1)
            player.update_frame()

        # SCREEN DRAWING SEQUENCE
        screen.fill((30, 30, 30))
        
        # Step 1: Blit the entire pre-baked structural grid instantly 
        screen.blit(background_surface, (0, 0))
        
        # Step 2: Draw target markers
        pygame.draw.rect(screen, ai_settings.COLOR_EXIT, (exit_x * ai_settings.TILE_SIZE, exit_y * ai_settings.TILE_SIZE, ai_settings.TILE_SIZE, ai_settings.TILE_SIZE))
        
        # Step 3: Draw interactive active moving sprite elements
        all_sprites.draw(screen)

        # Step 4: Render UI/HUD text
        hud_surface = font.render(
            f"Difficulty: {current_difficulty.upper()}   |   Regen: Easy(1) Med(2) Hard(3)   |   Move: WASD/Arrows", 
            True, ai_settings.COLOR_TEXT
        )
        screen.blit(hud_surface, (12, ai_settings.MAZE_HEIGHT * ai_settings.TILE_SIZE + 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
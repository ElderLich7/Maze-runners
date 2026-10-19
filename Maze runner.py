from email.mime import image
import sys
import pygame

from settings import Settings
from maze_gen import MazeGenerator
from visual_control import WallSprite, PlayerSprite

# --- WINDOW CONFIGURATION ---
ai_settings = Settings()
def main():
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.SCREEN_WIDTH, ai_settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Procedural Sprite Maze Playground")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16, bold=True)
    
    # Engine state setup
    engine = MazeGenerator(ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)
    current_difficulty = "medium"
    maze = engine.generate(current_difficulty)
    
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
                dx, dy = 0, 0
                if event.key in (pygame.K_LEFT, pygame.K_a):     
                    dx = -1
                    player.update_frame("left")
                elif event.key in (pygame.K_RIGHT, pygame.K_d):  
                    dx = 1
                    player.update_frame("right")
                elif event.key in (pygame.K_UP, pygame.K_w):     
                    dy = -1
                    player.update_frame("up")
                elif event.key in (pygame.K_DOWN, pygame.K_s):   
                    dy = 1
                    player.update_frame("down")
                # Use internal sprite logic to evaluate moving into the matrix boundaries
                player.move(dx, dy, maze)
                
                # Regenerate levels if configuration hotkeys are pressed
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3 ):
                    if event.key == pygame.K_1: current_difficulty = "easy"
                    elif event.key == pygame.K_2: current_difficulty = "medium"
                    elif event.key == pygame.K_3: current_difficulty = "hard"
                        

                    maze = engine.generate(current_difficulty)
                    background_surface, wall_group = ai_settings.build_level_cache(maze, ai_settings.MAZE_WIDTH, ai_settings.MAZE_HEIGHT)
                    player.set_grid_position(1, 1)
                    player.update_frame()

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
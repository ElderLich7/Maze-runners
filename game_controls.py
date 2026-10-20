import pygame

class Controller():
    def __init__(self ):
        pass

    def maze_controls(self , event ,screen ):
            if event.key == pygame.K_1: 
                screen.current_difficulty = "easy"       
            elif event.key == pygame.K_2: 
                screen.current_difficulty = "medium"    
            elif event.key == pygame.K_3: 
                screen.current_difficulty = "hard" 
                
            
    def movement_controls(self , keys ,player , current_time , maze , dx , dy ):
        # ONLY process movement if the cooldown period has ended
        if current_time - player.last_move_time >= player.MOVE_COOLDOWN:
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    dx = -1
                    player.update_frame("left")
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    dx = 1
                    player.update_frame("right")

            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    dy =  -1
                    player.update_frame("up")
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    dy = 1
                    player.update_frame("down")
        
            # If the player is actively pressing a key and trying to move
            if dx != 0 or dy != 0:
                player.move(dx, dy, maze)
                
            # Reset the timer to lock out movement until the next cooldown window
                player.last_move_time = current_time
        
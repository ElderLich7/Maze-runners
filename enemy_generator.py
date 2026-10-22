import pygame,random , numpy as np
#import matplotlib.pyplot as plt

class ExploringRandomWalk:
    def __init__(self):
        self.current = ( 0 , 0 )
        # Track visited spots to block them, and a history stack for backtracking
        self.visited = {}
        self.history_stack = []
        self.path_taken = []  # Chronological order of steps for plotting
      


class NPC(pygame.sprite.Sprite , ExploringRandomWalk ):
    """Represents the player square entity with internal movement bounds handling."""
    def __init__(self, grid_x, grid_y, size , creature_id , creature , frames ):
        super().__init__()
        self.size = size
        self.grid_x = grid_x
        self.grid_y = grid_y
        #cool down for player movement
        self.MOVE_COOLDOWN = 300  
        # Tracker for when the player last moved
        self.last_move_time = 0 
        self.creature = creature
        self.creature_id = creature_id
        self.is_moving = False
        self.movement_start_time = 0
        self.movement_start = (grid_x * size, grid_y * size)
        self.movement_target = self.movement_start
        self.movement_direction = "idle"
        self.frames = frames
        self.current_frame = self.frames["idle"]
        self.cycle_index = 0
        self.last_direction = "idle"
        self.image = self.current_frame[0]
        self.rect = self.image.get_rect(topleft=self.movement_start)

    # Updates the current frame of the player sprite based on the direction of movement
    def update_frame(self  , direction = "idle"):
        if self.last_direction != direction:
            self.cycle_index = 0
            self.last_direction = direction
        self.current_frame = self.frames.get(direction, self.frames["idle"])
        self.image = self.current_frame[self.cycle_index % len(self.current_frame)]

    # Sets the grid position of the player sprite and updates its pixel position accordingly 
    def set_grid_position(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect.x = grid_x * self.size
        self.rect.y = grid_y * self.size
        self.movement_start = self.rect.topleft
        self.movement_target = self.rect.topleft
        self.is_moving = False

    # Moves the player sprite in the specified direction if the target cell is walkable (0) in the maze matrix
    def move(self, dx, dy, dungeon_matrix, current_time):
        if self.is_moving:
            return False

        # Calculate tentative grid target space
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        # Check against matrix data boundaries (0 = walkable path)
        if not (0 <= new_y < len(dungeon_matrix) and 0 <= new_x < len(dungeon_matrix[new_y])):
            return False
        if dungeon_matrix[new_y][new_x] != 0:
            return False

        if dx < 0:
            direction = "left"
        elif dx > 0:
            direction = "right"
        elif dy < 0:
            direction = "up"
        else:
            direction = "down"

        self.movement_start = self.rect.topleft
        self.movement_target = (new_x * self.size, new_y * self.size)
        self.movement_start_time = current_time
        self.movement_direction = direction
        self.is_moving = True
        self.update_frame(direction)
        return True

    def update_movement(self, current_time):
        if not self.is_moving:
            return

        progress = min((current_time - self.movement_start_time) / self.MOVE_COOLDOWN, 1)
        start_x, start_y = self.movement_start
        target_x, target_y = self.movement_target
        self.rect.topleft = (
            round(start_x + (target_x - start_x) * progress),
            round(start_y + (target_y - start_y) * progress),
        )

        frames = self.current_frame
        self.cycle_index = min(int(progress * len(frames)), len(frames) - 1)
        self.image = frames[self.cycle_index]

        if progress >= 1:
            self.grid_x = round(target_x / self.size)
            self.grid_y = round(target_y / self.size)
            self.is_moving = False


    def explore_maze(self , maze , height , width): 
        # Relative movements: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    
        current = self.history_stack[-1]
        valid_moves = []

        # Check all 4 neighboring squares
        for dx, dy in directions:
            next_x, next_y = current[0] + dx, current[1] + dy
            
            # Condition: Inside boundaries AND not a wall AND not visited yet
            if (0 <= next_x < height and 0 <= next_y < width and maze[next_x][ next_y] == 0 and (next_x, next_y) not in self.visited):
                    valid_moves.append((next_x, next_y))

        if valid_moves:
            # Randomly select one of the valid, unvisited paths
            next_step = valid_moves[np.random.choice(len(valid_moves))]
            
            self.visited.add(next_step)
            self.history_stack.append(next_step)
            self.path_taken.append(next_step)
        else:
            # DEAD END: Backtrack to the previous intersection
            self.history_stack.pop()
            if self.history_stack:
                self.path_taken.append(self.history_stack[-1])

        dx , dy = self.path_taken[-1][0] - current[0] ,self.path_taken[-1][1] - current[1]
        return dx , dy 


'''
    
    code to visualize path 
    def plot_walk(self):
        """Visualizes the exploration path."""
        plt.figure(figsize=(10, 7), dpi=100)
        
        # Plot the path as a continuous line showing progression
        plt.plot(self.x_values, self.y_values, linewidth=1, color='blue', alpha=0.7, label='Path')
        
        # Color code the start and end points
        plt.scatter(0, 0, color='green', edgecolors='black', s=100, label='Start', zorder=5)
        plt.scatter(self.x_values[-1], self.y_values[-1], color='red', edgecolors='black', s=100, label='End', zorder=5)
        
        # Customizations
        plt.title(f"Exploring Random Walk ({len(self.visited)} Unique Positions Visited)")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.axis('equal')
        plt.show()

# Run the simulation
explorer = ExploringRandomWalk(num_steps=2000)
explorer.fill_walk()
explorer.plot_walk()'''

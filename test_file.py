import numpy as np
import matplotlib.pyplot as plt

# 1 = Wall, 0 = Open Path
# A simple 10x10 maze layout with dead ends and pathways
MAZE = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])

def explore_maze(maze, start_pos=(1, 1)):
    height, width = maze.shape
    current = start_pos
    
    # Track visited spots to block them, and a history stack for backtracking
    visited = {current}
    history_stack = [current]
    path_taken = [current]  # Chronological order of steps for plotting

    # Relative movements: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while history_stack:
        current = history_stack[-1]
        valid_moves = []

        # Check all 4 neighboring squares
        for dr, dc in directions:
            next_r, next_c = current[0] + dr, current[1] + dc
            
            # Condition: Inside boundaries AND not a wall AND not visited yet
            if (0 <= next_r < height and 0 <= next_c < width and 
                maze[next_r, next_c] == 0 and (next_r, next_c) not in visited):
                valid_moves.append((next_r, next_c))

        if valid_moves:
            # Randomly select one of the valid, unvisited paths
            next_step = valid_moves[np.random.choice(len(valid_moves))]
            
            visited.add(next_step)
            history_stack.append(next_step)
            path_taken.append(next_step)
        else:
            # DEAD END: Backtrack to the previous intersection
            history_stack.pop()
            if history_stack:
                path_taken.append(history_stack[-1])

    return path_taken, visited

# Run the simulation
start = (1, 1)
path, total_visited = explore_maze(MAZE, start)

# --- Visualization ---
plt.figure(figsize=(8, 8))
# Draw the maze layout
plt.imshow(MAZE, cmap='binary', origin='upper')

# Extract coordinates for the path line
rows, cols = zip(*path)
plt.plot(cols, rows, color='orange', linewidth=3, label='Walker Path (with Backtracking)', alpha=0.8)

# Highlight key landmarks
plt.scatter(start[1], start[0], color='green', s=150, zorder=5, label='Start')
plt.scatter(cols[-1], rows[-1], color='red', s=150, zorder=5, label='Final Position')

plt.title(f"Exploratory Random Walk in Maze\nVisited {len(total_visited)} path squares", fontsize=12, fontweight='bold')
plt.legend(loc='upper right')
plt.axis('off')
plt.show()
import random
import pygame
import sys

# --- MAZE GENERATOR ENGINE ---
class MazeGenerator:
    def __init__(self, width, height):
        # Force dimensions to be odd numbers for a perfect block-wall alignment
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        
    def generate(self, difficulty="medium"):
        # Grid dimensions for the underlying mathematical Kruskal cells
        grid_w = self.width // 2
        grid_h = self.height // 2
        
        # Disjoint Set Init
        parent = {(x, y): (x, y) for x in range(grid_w) for y in range(grid_h)}
        
        def find(cell):
            if parent[cell] == cell:
                return cell
            parent[cell] = find(parent[cell])
            return parent[cell]

        def union(cell1, cell2):
            root1 = find(cell1)
            root2 = find(cell2)
            if root1 != root2:
                parent[root1] = root2
                return True
            return False

        # Gather all internal walls
        walls = []
        for x in range(grid_w):
            for y in range(grid_h):
                if x < grid_w - 1:
                    walls.append(((x, y), (x + 1, y)))
                if y < grid_h - 1:
                    walls.append(((x, y), (x, y + 1)))

        # Apply Difficulty Tuning
        if difficulty == "hard":
            # Wavy sorting patterns yield deeply winding corridors and far fewer branches
            walls.sort(key=lambda w: (w[0][0] + w[0][1]) % 3 + random.random())
        else:
            random.shuffle(walls)

        maze_passages = []
        remaining_walls = []
        
        # Core Kruskal Evaluation
        for cell1, cell2 in walls:
            if union(cell1, cell2):
                maze_passages.append((cell1, cell2))
            else:
                remaining_walls.append((cell1, cell2))

        # Easy mode optimization: smash extra walls to allow loops and alternate pathways
        if difficulty == "easy":
            extra_openings = int(len(remaining_walls) * 0.25)
            random.shuffle(remaining_walls)
            for i in range(min(extra_openings, len(remaining_walls))):
                maze_passages.append(remaining_walls[i])
        
        # Step 5: Map passages cleanly into a block matrix (1 = Wall, 0 = Path)
        matrix = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Open up standard nodes
        for x in range(grid_w):
            for y in range(grid_h):
                matrix[2*y + 1][2*x + 1] = 0
                
        # Cut open structural walls matching the Kruskal linkages
        for cell1, cell2 in maze_passages:
            x1, y1 = cell1
            x2, y2 = cell2
            mx1, my1 = 2*x1 + 1, 2*y1 + 1
            mx2, my2 = 2*x2 + 1, 2*y2 + 1
            cx, cy = (mx1 + mx2) // 2, (my1 + my2) // 2
            matrix[cy][cx] = 0
            
        # Guarantee entry and exit points remain clear
        matrix[1][1] = 0
        matrix[self.height - 2][self.width - 2] = 0
        
        return matrix


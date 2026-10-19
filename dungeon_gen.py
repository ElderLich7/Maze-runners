import random

class DungeonGenerator:
    def __init__(self, width, height):
        # Force dimensions to be odd numbers for perfect block-wall alignment
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1

    def generate(self, difficulty="medium", num_rooms=5, min_size=3, max_size=7):
        # Grid dimensions for the underlying mathematical Kruskal cells
        grid_w = self.width // 2
        grid_h = self.height // 2

        # Disjoint Set Init
        parent = {(x, y): (x, y) for x in range(grid_w) for y in range(grid_h)}

        # Disjoint Set Find and Union Functions
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

        # Step 1: Initialize matrix with walls (1 = Wall, 0 = Path)
        matrix = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Step 2: Generate and Carve Rectangular Rooms
        # Rooms use odd coordinate placements to perfectly align with Kruskal nodes
        rooms = []
        for _ in range(num_rooms):
            # Ensure widths and heights are odd so they align cleanly with your tile grid step
            rw = random.randrange(min_size, max_size + 1, 2)
            rh = random.randrange(min_size, max_size + 1, 2)
            rx = random.randrange(1, self.width - rw, 2)
            ry = random.randrange(1, self.height - rh, 2)

            # Simple overlap check against existing rooms
            overlap = False
            for (ox, oy, ow, oh) in rooms:
                if rx < ox + ow and rx + rw > ox and ry < oy + oh and ry + rh > oy:
                    overlap = True
                    break
            
            if not overlap:
                rooms.append((rx, ry, rw, rh))
                # Carve the room out of the matrix
                for x in range(rx, rx + rw):
                    for y in range(ry, rh + ry):
                        matrix[y][x] = 0

                # Step 3: Pre-Union all mathematical Kruskal cells trapped inside this room
                # Maps pixel space (rx, ry) back into Kruskal cell space (cx, cy)
                cell_min_x = rx // 2
                cell_max_x = (rx + rw - 1) // 2
                cell_min_y = ry // 2
                cell_max_y = (ry + rh - 1) // 2

                first_cell = (cell_min_x, cell_min_y)
                for cx in range(cell_min_x, cell_max_x + 1):
                    for cy in range(cell_min_y, cell_max_y + 1):
                        union(first_cell, (cx, cy))

        # Gather all internal walls (Your original code)
        walls = []
        for x in range(grid_w):
            for y in range(grid_h):
                if x < grid_w - 1:
                    walls.append(((x, y), (x + 1, y)))
                if y < grid_h - 1:
                    walls.append(((x, y), (x, y + 1)))

        # Apply Difficulty Tuning (Your original code)
        if difficulty == "hard":
            walls.sort(key=lambda w: (w[0][0] + w[0][1]) % 4 + random.random())
        else:
            random.shuffle(walls)

        maze_passages = []
        remaining_walls = []

        # Core Kruskal Evaluation (Your original code)
        for cell1, cell2 in walls:
            if union(cell1, cell2):
                maze_passages.append((cell1, cell2))
            else:
                remaining_walls.append((cell1, cell2))

        # Easy mode optimization: smash extra walls to allow loops (Your original code)
        if difficulty == "easy":
            extra_openings = int(len(remaining_walls) * 0.25)
            random.shuffle(remaining_walls)
            for i in range(min(extra_openings, len(remaining_walls))):
                maze_passages.append(remaining_walls[i])

        # Open up standard nodes (Your original code)
        for x in range(grid_w):
            for y in range(grid_h):
                matrix[2*y + 1][2*x + 1] = 0

        # Cut open structural walls matching the Kruskal linkages (Your original code)
        for cell1, cell2 in maze_passages:
            x1, y1 = cell1
            x2, y2 = cell2
            mx1, my1 = 2*x1 + 1, 2*y1 + 1
            mx2, my2 = 2*x2 + 1, 2*y2 + 1
            cx, cy = (mx1 + mx2) // 2, (my1 + my2) // 2
            matrix[cy][cx] = 0

        # Guarantee entry and exit points remain clear (Your original code)
        matrix[1][1] = 0
        matrix[self.height - 2][self.width - 2] = 0

        return matrix
    
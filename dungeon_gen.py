import random

class DungeonGenerator:
    def __init__(self, width, height):
        # Force dimensions to be odd numbers for perfect block-wall alignment
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1

    def generate(self, difficulty , num_rooms , min_size , max_size , hard_complexity = 4  ):
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
        room_by_cell = {}
        room_entrances = []

        room_library = {}

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
                room_index = len(rooms) - 1
                room_entrances.append(0)
                # Pre-union the Kruskal cells whose centers lie inside this room.
                room_cells = [
                    (cx, cy)
                    for cx in range(grid_w)
                    for cy in range(grid_h)
                    if rx <= 2 * cx + 1 < rx + rw
                    and ry <= 2 * cy + 1 < ry + rh
                ]
                first_cell = room_cells[0]
                room_left = 2 * min(cx for cx, _ in room_cells) + 1
                room_right = 2 * max(cx for cx, _ in room_cells) + 1
                room_top = 2 * min(cy for _, cy in room_cells) + 1
                room_bottom = 2 * max(cy for _, cy in room_cells) + 1

                # Clear the room interior, but keep its outside boundary walls intact.
                for x in range(room_left, room_right + 1):
                    for y in range(room_top, room_bottom + 1):
                        matrix[y][x] = 0
                        room_library.setdefault(rooms[room_index], []).append(( x , y ))


                for cell in room_cells:
                    room_by_cell[cell] = room_index
                    union(first_cell, cell)

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
            walls.sort(key=lambda w: (w[0][0] + w[0][1]) % hard_complexity + random.random())
        else:
            random.shuffle(walls)

        maze_passages = []
        remaining_walls = []

        def doorway_rooms(cell1, cell2):
            room1 = room_by_cell.get(cell1)
            room2 = room_by_cell.get(cell2)
            if room1 == room2:
                return ()
            return tuple(room for room in (room1, room2) if room is not None)

        # Core Kruskal Evaluation (Your original code)
        for cell1, cell2 in walls:
            connected_rooms = doorway_rooms(cell1, cell2)
            if any(room_entrances[room] >= 2 for room in connected_rooms):
                remaining_walls.append((cell1, cell2))
                continue

            if union(cell1, cell2):
                maze_passages.append((cell1, cell2))
                for room in connected_rooms:
                    room_entrances[room] += 1
            else:
                remaining_walls.append((cell1, cell2))

        # Easy mode optimization: smash extra walls to allow loops (Your original code)
        if difficulty == "easy":
            extra_openings = int(len(remaining_walls) * 0.25)
            random.shuffle(remaining_walls)
            added_openings = 0
            for cell1, cell2 in remaining_walls:
                if added_openings >= extra_openings:
                    break
                connected_rooms = doorway_rooms(cell1, cell2)
                if any(room_entrances[room] >= 2 for room in connected_rooms):
                    continue
                maze_passages.append((cell1, cell2))
                for room in connected_rooms:
                    room_entrances[room] += 1
                added_openings += 1

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

        print(rooms )
        print(room_library)

        return matrix
    
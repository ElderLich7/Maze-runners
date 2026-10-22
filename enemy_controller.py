import random
import pygame

from enemy_generator import NPC


class EnenmyAI():
    def __init__(self , num_enemies , system_tile_size , all_enemy_frames):
        self.num_enemies = num_enemies
        #self.maze = maze
        self.system_tile_size = system_tile_size
        self.enemy_group = pygame.sprite.Group()
        self.enemy_types = ("skeleton",)
        self.enemy_positions = {}

        for id in range(num_enemies):
            creature = random.choice(self.enemy_types)
            frames = {}
            if creature == "skeleton":
                frames = all_enemy_frames.skeleton_walk_frames
            self.enemy_group.add(NPC(1, 1, system_tile_size , id, creature , frames))


    def pick_initial_enemy_positions(self , dungeon_matrix):

        self.available_positions = [
            (x, y)
            for y, row in enumerate(dungeon_matrix)
            for x, value in enumerate(row)
            if value == 0
        ]
        if len(self.available_positions) < len(self.enemy_group):
            raise ValueError("The dungeon does not have enough walkable tiles for all enemies.")

        random.shuffle(self.available_positions)
        for enemy, position in zip(self.enemy_group, self.available_positions):
            enemy.grid_x, enemy.grid_y = position
            enemy.visited = {position}
            enemy.history_stack = [position] 
            enemy.path_taken = [position]
            self.enemy_positions[enemy.creature_id] = position
            enemy.set_grid_position(enemy.grid_x, enemy.grid_y)

        self.possible_paths = self.available_positions

    def enemy_movement(self , current_time , maze , height , width ):
        for enemy in self.enemy_group:
            if not enemy.is_moving and current_time - enemy.last_move_time >= enemy.MOVE_COOLDOWN:
                dx , dy = enemy. explore_maze( maze , height , width, self.enemy_positions)
                self.enemy_positions[enemy.creature_id] = enemy.path_taken[-1]
                if dx != 0 or dy != 0:
                    if enemy.move(dx, dy, maze, current_time):
                        enemy.last_move_time = current_time

        for enemy in self.enemy_group:
            enemy.update_movement(current_time)
import pygame
from pathlib import Path

ASSET_ROOT = Path(__file__).resolve().parent

def load (pic):
       loaded =  pygame.image.load(str(pic)).convert_alpha()
       return loaded

class Character_Sprites():
    def __init__(self):
       self.frames = None
    
    def subdivide_sprite_into_frames( self , grid_x , size , grid_y ):
        original_image = load(ASSET_ROOT / "Sprites/Maze_Sprites/Character/sprite player.png")
        frame_width = 45
        frame_height = 68
        #each unique frame of the sprite sheet is defined by a rectangle, and then scaled to the desired size
        idle_animation = pygame.Rect( 5 , 8, frame_width, frame_height )
        down = [pygame.Rect( 55 , 8, frame_width, frame_height ),pygame.Rect( 162 , 8, frame_width, frame_height )]
        up = [pygame.Rect( 50 , 233, frame_width, frame_height ),pygame.Rect( 160 , 235, frame_width, frame_height )]
        left = [pygame.Rect( 55 , 84, frame_width, frame_height ),pygame.Rect( 162 , 84, frame_width, frame_height )]
        right = [pygame.Rect( 55 , 166, frame_width, frame_height ),pygame.Rect( 158 , 166, frame_width, frame_height )]
            
        #define the frames for each direction and scale them to the desired size
        self.frames = {"idle": [idle_animation], "down": down, "up": up, "left": left, "right": right}
        for direction in self.frames:
            if direction != "idle":
                                for i in range(len(self.frames[direction])):
                                    self.frames[direction][i] = original_image.subsurface(self.frames[direction][i])
                                    self.frames[direction][i] = pygame.transform.scale(self.frames[direction][i], (grid_x * size, grid_y * size))

        #define the idle frame and scale it to the desired size           
        self.frames["idle"] = [original_image.subsurface(idle_animation)]
        self.frames["idle"] = [pygame.transform.scale(frame, (grid_x * size, grid_y * size)) for frame in self.frames["idle"]]

    def load_dungeon_player_sprites(self, size):

           idle_animation = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Player/standard/idle/up/{i}.png"), (size, size)) for i in range(1, 3)]

           up = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Player/standard/walk/up/{i}.png"), (size, size)) for i in range(1, 10)]
           down = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Player/standard/walk/down/{i}.png"), (size, size)) for i in range(1, 10)]
           left = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Player/standard/walk/left/{i}.png"), (size, size)) for i in range(1, 10)]
           right = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Player/standard/walk/right/{i}.png"), (size, size)) for i in range(1, 10)]

           self.player_walk_frames = {"idle": idle_animation, "down": down, "up": up, "left": left, "right": right}

class EnemySprites:
    def __init__(self, size):
        """
        Loads and scales the skeleton NPC's idle and walking animation frames for all directions.

        Parameters:
            size (int): The size (width and height) to scale each frame to.

        Usage:
            Call this method to populate self.skeleton_walk_frames with the skeleton's animation frames.
        """
        
        
        idle_animation = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Npc/Skeleton/idle/up/{i}.png"), (size, size)) for i in range(1, 3)]
           
        up = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Npc/Skeleton/walk/up/{i}.png"), (size, size)) for i in range(1, 10)]
        down = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Npc/Skeleton/walk/down/{i}.png"), (size, size)) for i in range(1, 10)]
        left = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Npc/Skeleton/walk/left/{i}.png"), (size, size)) for i in range(1, 10)]
        right = [pygame.transform.scale(load(ASSET_ROOT / f"Sprites/Dungeon_Sprites/Npc/Skeleton/walk/right/{i}.png"), (size, size)) for i in range(1, 10)]
        
        self.skeleton_walk_frames = {"idle": idle_animation, "down": down, "up": up, "left": left, "right": right}
        skeleton_frames_cache = {
                "idle": idle_animation,
                "down": down,
                "up": up,
                "left": left,
                "right": right
            }
        self.skeleton_walk_frames = skeleton_frames_cache
    
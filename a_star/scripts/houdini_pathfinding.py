import hou
import math
import json
import os

from a_star import AStarPathfinding

def get_maze_from_grid():
    """
    Extracts the maze grid from a Houdini geometry node.

    Returns:
        grid_matrix (list): 2D matrix representing the maze, where 1 is open and 0 is blocked.
    """
    grid = hou.pwd().parm('grid_node').eval()
    geo = hou.node(grid).geometry()
    
    prims = geo.prims()
    num_rows = num_columns = int(math.sqrt(len(prims)))
    
    grid_matrix = []
    
    # Loop through each primitive and determine if it's open or blocked based on color
    for row in range(num_rows):
        new_row = []
        for col in range(num_columns):
            prim_index = row * num_columns + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")
            new_row.append(1 if color == (1.0, 1.0, 1.0) else 0)
        grid_matrix.append(new_row)
  
    return grid_matrix

def position_object(obj_path, row, col, cell_size = 1):
    """
    Moves a Houdini object to a specified grid cell.

    Args:
        obj_path (str): Houdini node path of the object.
        row (int): Row index in the grid.
        col (int): Column index in the grid.
        cell_size (int, optional): Size of each cell in world units. Defaults to 1.

    Returns:
        pos (tuple): The (row, col) position of the object.
    """
    main_char = hou.node(obj_path)
    world_x = col * cell_size
    world_z = row * cell_size
    
    center = main_char.parmTuple("t").eval()
    main_char.parmTuple("t").set((world_x, 0, world_z))
    pos = (row, col)
    
    return pos

def solve_maze():
    """
    Solves the maze for each NPC using A* pathfinding and writes the paths to a JSON file.

    Returns:
        None
    """
    path_dict = {}
    main_char_path = hou.pwd().parm("player_path").eval()
    main_char_pos = hou.pwd().parmTuple("player_pos").eval()
    
    npc_list = hou.pwd().parm('npc_list').eval()
    
    # Loop through each NPC and calculate their path to the player
    for idx in range(npc_list):
        idx = idx + 1
    
        npc_char_path = hou.pwd().parm(f"npc_{idx}").eval()
        npc_char_pos = hou.pwd().parmTuple(f"npc_{idx}_pos").eval()
        if not npc_char_path:
            continue
        
        target_pos = position_object(main_char_path, main_char_pos[0], main_char_pos[1])
        start_pos = position_object(npc_char_path, npc_char_pos[0], npc_char_pos[1])
        
        maze = get_maze_from_grid()
        
        pathFinder = AStarPathfinding(maze, start_pos, target_pos)
        path = pathFinder.find_path()
        
        path_dict[f'npc_{idx}'] = path  # Store the path for each NPC
    
    # Write all NPC paths to a JSON file
    with open(f'{script_path}/path_dict.json', 'w') as f:
        json.dump(path_dict, f, indent = 4)
            
def set_keyframes():
    """
    Sets keyframes for each NPC in Houdini based on the calculated path from the JSON file.

    Returns:
        None
    """
    # Check if the path dictionary file exists
    if not os.path.exists(f'{script_path}/path_dict.json'):
        hou.ui.displayMessage("The Execute command has not been run, please run before setting keyframes")
        return None
    with open(f'{script_path}/path_dict.json', 'r') as f:
        path_dict = json.load(f)
        
    npc_list = hou.pwd().parm('npc_list').eval()
    
    # Loop through each NPC and set keyframes for their movement along the path
    for idx in range(npc_list):
        idx = idx + 1
        npc_char_path = hou.pwd().parm(f"npc_{idx}").eval()
        if not npc_char_path:
            continue
            
        path = path_dict[f"npc_{idx}"]
        
        for frame in range(len(path)):
            key_z = hou.Keyframe()
            key_z.setFrame(frame+1)
            key_z.setValue(path[frame][0])
            
            key_x = hou.Keyframe()
            key_x.setFrame(frame+1)
            key_x.setValue(path[frame][1])
            
            hou.node(npc_char_path).parm('tx').setKeyframe(key_x)
            hou.node(npc_char_path).parm('tz').setKeyframe(key_z)
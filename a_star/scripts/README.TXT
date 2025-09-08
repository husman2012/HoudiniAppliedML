houdini_pathfinding.py contains referenced code for pasting into HDA Scripts

Execute button should call: hou.phm().solve_maze()
Set Keyframes button should call: hou.phm().set_keyframes()

SCRIPT TO ADD IF EMBEDDED HDA DOES NOT HAVE IT:
import sys
#CHANGE PATH BELOW TO POINT TO A-STAR SCRIPTS FOLDER DIRECTORY - THIS WILL ALSO BE USED FOR TEMP JSON FILES
script_path = r"path/to/scripts"
sys.path.append(script_path)

from a_star import AStarPathfinding
from houdini_pathfinding import solve_maze, set_keyframes

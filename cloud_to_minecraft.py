# -*- coding: utf-8 -*-

from laspy import read, open
from numpy import sqrt, vstack, linspace
from open3d import geometry, utility
from mcpi.minecraft import Minecraft
from tqdm import tqdm
from time import sleep

# =============================================================================
# Glob_Var
# =============================================================================

BLOCK_DICT = {
    (200, 110, 70): [5, 4], #planche acacia
    (150, 151, 149): [1, 5], #andésite
    (202, 187, 133): [5, 2], #planches bouleau
    (17, 18, 23): [251, 15], #béton noir
    (43, 30, 25): [159, 15], #terracota noir
    (33, 33, 37): [35, 15], #laine noire
    (47, 48, 140): [251, 11], #beton bleu
    (106, 168, 250): [266], #blue ice
    (78, 64, 91): [159, 11], #blue terracota
    (55, 58, 153): [35, 11], #blue wool
    (181, 100, 82): [45], #bricks
    (99, 62, 39): [251, 12], #brown concrete
    (80, 55, 41): [159, 12], #brown terracota
    (128, 81, 53): [35, 12], #brown wool
    (153, 162, 176): [82], #clay
    (21, 21, 21): [173], #block charbon
    (156, 111, 80): [3], #dirt
    (100, 100, 100): [4], #cobble
    (0, 118, 134): [251, 9], #cyan concrete
    (90, 93, 93): [159, 9], #cyan terracota
    (0, 148, 150): [35, 9], #cyan wool
    (84, 58, 34): [5, 5], #dark oak plank
    (57, 107, 91): [168, 2], #dark prismarine
    (56, 243, 227): [57], #diamond block
    (244, 252, 190): [121], #end stone
    (220, 224, 162): [206], #end stone brick
    (255, 224, 89): [41], #gold block
    (180, 124, 107): [1, 1], #granite
    (57, 60, 63): [251, 7], #gray concrete
    (63, 48, 41): [159, 7], #gray terracota
    (66, 72, 75): [35, 7], #gray wool
    (73, 92, 44): [251, 13], #green concrete
    (78, 85, 50): [159, 13], #green terracota
    (81, 106, 40): [35, 13], #green wool
    (234, 234, 234): [42], #iron block
    (172, 124, 96) : [5, 3], #jungle wood plank
    (27, 61, 139): [22], #lapis
    (0, 136, 196): [251, 3], #light blue concrete
    (114, 109, 136): [159, 3], #terracota
    (0, 170, 211): [35, 3], #wool
    (125, 125, 116): [251, 8], #light gray concrete
    (137, 107, 98): [159, 8], #terracota
    (142, 142, 135): [35, 8], #wool
    (85, 169, 49): [251, 5], #lime concrete
    (101, 116, 59): [159, 5], #terracota
    (103, 186, 52): [35, 5], #wool
    (174, 49, 155): [251, 2], #magenta concrete
    (152, 87, 107): [159, 2], #terracota
    (198, 71, 178): [35, 2], #wool
    (50, 29, 33): [112], #nether bricks
    (110, 11, 12): [214], #nether wart block
    (86, 30, 31): [87], #netherrack
    (170, 134, 87): [5], #oak wood plank
    (232, 97, 33): [251, 1], #orange concrete
    (166, 85, 48): [159, 1], #terracota
    (243, 106, 38): [35, 1], #wool
    (221, 101, 141): [251, 6], #pink concrete
    (167, 80, 82): [159, 6], #terracota
    (251, 139, 170): [35, 6], #wool
    (131, 133, 132): [1, 6], #polished andesite
    (188, 189, 192): [1, 4], #polished diorite
    (168, 115, 98): [1, 2], #granite
    (104, 33, 152): [251, 10], #purple concrete
    (121, 71, 86): [159, 12], #terracota
    (125, 41, 166): [35, 12], #wool
    (238, 229, 221): [155], #quartz
    (148, 38, 41): [251, 14], #red concrete
    (89, 21, 24): [215], #red nether brick
    (150, 65, 54): [159, 14], #terracota
    (164, 42, 41): [35, 14], #wool
    (137, 101, 63): [5, 1], #spruce plank
    (127, 127, 127): [1], #stone
    (159, 93, 69): [172], #hardened clay
    (206, 213, 213): [251, 0], #white concrete
    (213, 180, 162): [159, 0], #terracotta
    (225, 228, 229): [35, 0], #wool
    (245, 173, 53): [251, 4], #yellow concrete
    (190, 133, 52): [159, 4], #terracotta
    (255, 202, 68): [35, 4], #wool
    }

COLORS = list(BLOCK_DICT.keys())

# =============================================================================
# Func
# =============================================================================

def closest_color(rgb):
    r, g, b = rgb
    r*=256;g*=256;b*=256

    color_diffs = []

    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

# =============================================================================
# Main
# =============================================================================

input_path="C:/" #path
dataname="mural.las"

point_cloud = read(input_path + dataname)

pcd = geometry.PointCloud()

pcd.points = utility.Vector3dVector(vstack((point_cloud.x, point_cloud.y,
                                                   point_cloud.z)).transpose())

pcd.colors = utility.Vector3dVector(vstack((point_cloud.red, point_cloud.green,
                                                   point_cloud.blue)).transpose() / 65535)

v_size = 0.10

voxel_grid = geometry.VoxelGrid.create_from_point_cloud(pcd,  voxel_size=v_size)

voxels = voxel_grid.get_voxels()

mc = Minecraft.create(address="localhost", port=4711)
mc.postToChat("Hello world")

for i in tqdm(range(len(voxels))) :

    colorr = voxels[i].color
    index = voxels[i].grid_index
    color = closest_color(colorr)

    mc.setBlock(index[1]-9555, index[2]+40, index[0]-9555, *BLOCK_DICT[color])

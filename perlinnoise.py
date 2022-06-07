
from cmath import phase
import noise
import numpy as np
from PIL import Image

scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

BLACK_VALUE = False
WHITE_VALUE = True

def generate_world(size, world, seed, x_offset, y_offset, beach_mode = False, threshold = 0):
    shape = (size, size)
    for i in range(shape[0]):
        for j in range(shape[1]):
            val = noise.pnoise2((i + x_offset * size) / scale, 
                    (j + y_offset * size) / scale, 
                    octaves=octaves, 
                    persistence=persistence, 
                    lacunarity=lacunarity, 
                    repeatx=size, 
                    repeaty=size, 
                    base=seed)
            if beach_mode: # TODO: Replace threshold on line 28 with threshold_2, and add as function arguments to all functions that use threshold
                world[i][j] = BLACK_VALUE if val > threshold and val < threshold + 0.05 else WHITE_VALUE
            else:
                world[i][j] = WHITE_VALUE if val > threshold else BLACK_VALUE
    return world

def save_world_image(world, filepath):
    Image.fromarray(world).convert('RGB').save(filepath, format="bmp")

def display_world(world):
    Image.fromarray(world).show()

def generate_world_array(size, seed, x_offset, y_offset, beach_mode = False, threshold=0):
    world = np.zeros((size, size))
    world = generate_world(size, world, seed, x_offset, y_offset, beach_mode, threshold=threshold)
    return world

def combine_phase_and_border_world_arrays(size, phase_world, border_world):
    shape = (size, size)
    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if phase_world[i][j] and border_world[i][j]:
                world[i][j] = WHITE_VALUE
            else:
                world[i][j] = BLACK_VALUE
    return world

def generate_phase_array(size, seed1, seed2, x_offset, y_offset, threshold=0):
    phase_world = generate_world_array(size, seed1, x_offset, y_offset, threshold=threshold)
    border_world = generate_world_array(size, seed2, x_offset, y_offset, True, threshold=threshold)
    combined_world = combine_phase_and_border_world_arrays(size, phase_world, border_world)
    return combined_world

if __name__ == "__main__":
    my_array = generate_phase_array(300, 2, 7, 0, 0)
    display_world(my_array)
    my_array = generate_phase_array(100, 2, 7, 0, 0)
    display_world(my_array)
    my_array = generate_phase_array(100, 2, 7, 0, 1)
    display_world(my_array)
    my_array = generate_phase_array(100, 2, 7, 1, 0)
    display_world(my_array)
    my_array = generate_phase_array(100, 2, 7, 1, 1)
    display_world(my_array)
    print(my_array)
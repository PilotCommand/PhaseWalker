def add_elements_in_tuple(tuple1, tuple2):
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])

class PlayerCoordinateManager:
    """
    This class will take care of:
    X Keep track of current chunk coordinate
    X Keep track of player's coordinates within a specific chunk
    X Keep track of which chunks are loaded
    X Handle loading/unloading chunks when crossing chunk boundaries
    X Handle updating player's coordinates within a specific chunk when crossing chunk boundaries

    This class will expose:
    X 1 function to handle movement in any direction (up down left right by x number of spaces)
        X If the move requires loading new chunks, it will return a 3-long list of tuples containing the new chunk coordinates to be generated
        X If the move DOES NOT REQUIRE loading new chunks, it will return nothing
    """

    direction_set_dict = {
        (0,1): [(1,1), (0,1), (-1,1)],
        (1,0): [(1,1), (1,0), (1,-1)],
        (0,-1): [(1,-1), (0,-1), (-1,-1)],
        (-1,0): [(-1,1), (-1,0), (-1,-1)]
    }

    def __init__(self, chunk_size, chunk_render_function):
        if chunk_size < 3:
            raise Exception("Chunk size too small")
        self.chunk_size = chunk_size
        self.chunk_render_function = chunk_render_function
        self.chunk_dictionary = {}
        for x in range(-1, 2):
            for y in range(-1, 2):
                self.chunk_dictionary[(x,y)] = self.chunk_render_function((x,y))
        self.chunk_x = 0
        self.chunk_y = 0
        self.local_x = chunk_size // 2
        self.local_y = chunk_size // 2

    def regenerate_chunk_dictionary(self):
        self.chunk_dictionary = {}
        for x in range(self.chunk_x - 1, self.chunk_x + 2):
            for y in range(self.chunk_y - 1, self.chunk_y + 2):
                self.chunk_dictionary[(x,y)] = self.chunk_render_function((x,y))


    def pretty_print_chunks(self, display_function):
        # print("Local coords: {}, {}".format(self.local_x, self.local_y))
        for x in range(self.chunk_x -1, self.chunk_x + 2):
            for y in range(self.chunk_y -1, self.chunk_y + 2):
                # display_function(self.chunk_dictionary[(x, y)])
                pass

    def handle_chunk_move(self, direction: tuple):
        if direction not in [(1,0), (-1,0), (0, 1), (0,-1)]:
            raise ValueError("Direction must be one of: [(1,0), (-1,0), (0, 1), (0,-1)]")

        # update current chunk coords
        self.chunk_x = self.chunk_x + direction[0]
        self.chunk_y = self.chunk_y + direction[1]

        old_direction = direction[0] * -3, direction[1] * -3

        return_list_of_new_chunks = []

        for new_direction_coords in PlayerCoordinateManager.direction_set_dict[direction]:
            # add the 3 values we moved TOWARD, to the chunk dictionary
            new_chunk_coords = add_elements_in_tuple((self.chunk_x, self.chunk_y), new_direction_coords)
            self.chunk_dictionary[new_chunk_coords] = self.chunk_render_function(new_chunk_coords)
            return_list_of_new_chunks.append(new_chunk_coords)

            # delete the 3 values we moved AWAY FROM, from the chunk dictionary
            old_chunk_coords = add_elements_in_tuple(old_direction, new_chunk_coords)
            del(self.chunk_dictionary[old_chunk_coords])
        
        # print("Moved into chunk: {}".format((self.chunk_x, self.chunk_y)))
        return return_list_of_new_chunks
    
    def handle_local_move(self, direction:tuple, steps:int):
        if direction not in [(1,0), (-1,0), (0, 1), (0,-1)]:
            raise ValueError("Direction must be one of: [(1,0), (-1,0), (0, 1), (0,-1)]")
        if steps < 1:
            raise ValueError("Steps must be greater than 0")
        if steps > self.chunk_size:
            raise ValueError("Steps must be less than or equal to chunk size")

        direction = direction[0] * steps, direction[1] * steps
        self.local_x, self.local_y = add_elements_in_tuple((self.local_x, self.local_y), direction)

        if self.local_x < 0:
            self.local_x += self.chunk_size
            return self.handle_chunk_move((-1, 0))
        if self.local_y < 0:
            self.local_y += self.chunk_size
            return self.handle_chunk_move((0, -1))
        if self.local_x >= self.chunk_size:
            self.local_x -= self.chunk_size
            return self.handle_chunk_move((1, 0))
        if self.local_y >= self.chunk_size:
            self.local_y -= self.chunk_size
            return self.handle_chunk_move((0, 1))

    def get_chunk_data(self, chunk_coords):
        return self.chunk_dictionary[chunk_coords]

    def get_player_local_coords(self):
        return (self.local_x, self.local_y)

    def set_player_local_coords(self, new_local_coords):
        self.local_x, self.local_y = new_local_coords

    def get_player_chunk_coords(self):
        return (self.chunk_x, self.chunk_y)
    
    def get_screen_coords(self, offset=(0,0)):
        # Returns the player's local coords LOCAL TO chunk (0,0)
        screen_x = self.chunk_x * self.chunk_size + self.local_x + offset[0]
        screen_y = self.chunk_y * self.chunk_size + self.local_y + offset[1]
        return (screen_x, screen_y)
         



if __name__ == "__main__":
    pcm = PlayerCoordinateManager(5, lambda x: "chunk {}".format(x))

    for x in range(100):
        if pcm.handle_local_move((1,0), 1):
            print("NEW CHUNK RENDERED! ITERATION {}".format(x))

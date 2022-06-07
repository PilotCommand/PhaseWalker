import playercoordinatemanager
import perlinnoise

class PhaseChunks:
    def __init__(self, chunk_size, threshold):
        self.chunk_size = chunk_size
        self.threshold = threshold
        self.chunk_generator_function = lambda chunk_coords: perlinnoise.generate_phase_array(
            self.chunk_size, 
            3, 
            7, 
            chunk_coords[0], 
            chunk_coords[1],
            self.threshold)
        self.pcm = playercoordinatemanager.PlayerCoordinateManager(chunk_size, self.chunk_generator_function)

    def get_pcm(self):
        return self.pcm
    
    def change_threshold(self, threshold_delta):
        self.threshold += threshold_delta
        self.chunk_generator_function = lambda chunk_coords: perlinnoise.generate_phase_array(
            self.chunk_size, 
            2, 
            7, 
            chunk_coords[0], 
            chunk_coords[1],
            self.threshold)
        self.pcm.regenerate_chunk_dictionary()

if __name__ == "__main__":
    phase_chunks_instance = PhaseChunks(50)
    player_coordinate_manager_instance = phase_chunks_instance.get_pcm()
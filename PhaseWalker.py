import pygame
import phasechunks
import math

class HamudiGame:
    def __init__(self, screen_width, screen_height, chunk_size, view_distance, player_size, step_size, starting_threshold, threshold_delta, debug=False):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_offset_x = 0
        self.screen_offset_y = 0
        self.screen_resolution = self.screen_width * 2, self.screen_height * 2
        self.chunk_size = chunk_size
        self.view_distance = view_distance
        self.player_size = player_size
        self.step_size = step_size
        self.starting_threshold = starting_threshold
        self.threshold_delta = threshold_delta
        self.game_run = True
        self.boost = 1
        self.debug = debug
        pygame.init()

    def run_game(self):
        self.game_screen =  pygame.display.set_mode(self.screen_resolution)
        self.virtual_screen = pygame.Surface((self.screen_width, self.screen_height))
        self.game_clock = pygame.time.Clock()
        self.phase_chunks_instance = phasechunks.PhaseChunks(self.chunk_size, self.starting_threshold)
        self.player_coordinates_manager_instance = self.phase_chunks_instance.get_pcm()
        self.player_coordinates_manager_instance.set_player_local_coords((0,0))
        self.player_has_moved = True
        self.game_loop()

    def game_loop(self):
        while self.game_run:
            if self.player_has_moved:
                self.virtual_screen.fill(0)
                self.draw_world()
                self.draw_player()
                self.game_screen.blit(pygame.transform.scale2x(self.virtual_screen),(0,0))
                pygame.display.update()
                self.player_has_moved = False
            self.game_clock.tick(60)
            self.quit_handler()
            self.key_handler()

    def draw_player(self):
        player_position_on_screen = self.player_coordinates_manager_instance.get_screen_coords((self.screen_width//2 + self.screen_offset_x, self.screen_height//2 + self.screen_offset_y))
        self.player_rectangle = pygame.draw.rect(
            self.virtual_screen, 
            (255,0,0), 
            player_position_on_screen + (self.player_size, self.player_size))

    def draw_world(self):
        pixel_array = pygame.PixelArray(self.virtual_screen)
        for chunk_coords, chunk_image_data in self.player_coordinates_manager_instance.chunk_dictionary.items():
            chunk_x, chunk_y = chunk_coords
            for x in range(self.chunk_size):
                for y in range (self.chunk_size):
                    screen_x = x + self.chunk_size * chunk_x + self.screen_width//2 + self.screen_offset_x
                    screen_y = y + self.chunk_size * chunk_y + self.screen_height//2 + self.screen_offset_y
                    if screen_x < 0 or \
                            screen_y < 0 or \
                            screen_x >= self.screen_width or \
                            screen_y >= self.screen_height or \
                            math.dist(self.player_coordinates_manager_instance.get_screen_coords((self.screen_width//2 + self.screen_offset_x, self.screen_height//2 + self.screen_offset_y)), (screen_x, screen_y)) > self.view_distance:
                        continue
                    
                    if math.dist(self.player_coordinates_manager_instance.get_screen_coords((self.screen_width//2 + self.screen_offset_x, self.screen_height//2 + self.screen_offset_y)), (screen_x, screen_y)) - self.view_distance > -1:
                        color = (0,255,0)
                    elif self.debug and (x == 0 or y == 0):
                        color = (255,0,0) # DEBUG: chunk borders are red
                    elif chunk_image_data[x][y]:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                    pixel_array[screen_x, screen_y] = pygame.Color(color)
        pixel_array.close()

    def key_handler(self):
        keys = pygame.key.get_pressed() #gets all the keys that are pressed
        if keys[pygame.K_a]: #if the a key is pressed...
            self.player_coordinates_manager_instance.handle_local_move((-1,0), self.step_size * self.boost)
            self.player_has_moved = True
            self.handle_new_screen()
        if keys[pygame.K_d]: #if the d key is pressed...
            self.player_coordinates_manager_instance.handle_local_move((1, 0), self.step_size * self.boost)
            self.player_has_moved = True
            self.handle_new_screen()
        if keys[pygame.K_w]: #if the w key is pressed...
            self.player_coordinates_manager_instance.handle_local_move((0,-1), self.step_size * self.boost)
            self.player_has_moved = True
            self.handle_new_screen()
        if keys[pygame.K_s]: #if the s key is pressed...
            self.player_coordinates_manager_instance.handle_local_move((0, 1), self.step_size * self.boost)
            self.player_has_moved = True
            self.handle_new_screen()
        if keys[pygame.K_n]: #if the n key is pressed...
            self.phase_chunks_instance.change_threshold(self.threshold_delta)
            self.player_has_moved = True
            self.handle_new_screen()
        if keys[pygame.K_m]: #if the m key is pressed...
            self.phase_chunks_instance.change_threshold(-self.threshold_delta)
            self.player_has_moved = True
            self.handle_new_screen()
        if keys[pygame.K_LSHIFT]:
            self.boost = 2
        else:
            self.boost = 1

    def quit_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_run = False
    
    def handle_new_screen(self):
        player_x, player_y = self.player_coordinates_manager_instance.get_screen_coords((self.screen_width//2 + self.screen_offset_x, self.screen_height//2 + self.screen_offset_y))
        if player_x > self.screen_width:
            self.screen_offset_x -= self.screen_width
        if player_x < 0:
            self.screen_offset_x += self.screen_width
        if player_y > self.screen_height:
            self.screen_offset_y -= self.screen_height
        if player_y < 0:
            self.screen_offset_y += self.screen_height




hamudi_game = HamudiGame(400, 300, 50, 50, 5, 2, 0, 0.01, debug=False)
hamudi_game.run_game()
from wall import Wall

class SC:
    screen_size = screen_width, screen_height = 671, 744
    player_start_pos = (screen_width / 2, screen_height * 4/5)
    wall_velocity = 1
    initial_player_accel = 0.3
    background = 255, 255, 255
    score_color = 0, 0, 0
    frame_time = 0.007
    wall_gap_size = 317
    wall_frequency = 377
    wall_width = Wall.default_width
    wall_height = Wall.default_height
    wall_range = (int(-.9 * wall_width), int(screen_width - wall_gap_size - 1.1 * wall_width))
    wall_start_y = -200
    frozen_frames_after_input = 10
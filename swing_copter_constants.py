from platform import Platform

class SC:
    screen_size = screen_width, screen_height = 671, 744
    player_start_pos = (screen_width / 2, screen_height * 4/5)
    platform_velocity = 1
    initial_player_accel = 0.3
    background = 61, 186, 234
    score_color = 0, 0, 0
    frame_time = 0.007
    platform_gap_size = 318
    platform_frequency = 377
    platform_width = Platform.default_width
    platform_height = Platform.default_height
    platform_range = (int(-.9 * platform_width), int(screen_width - platform_gap_size - 1.1 * platform_width))
    platform_start_y = -200
    frozen_frames_after_input = 10
    # MCTS Settings
    mcts_num_games = 50
    mcts_num_charges = 20
    mcts_max_charge_depth = 10000
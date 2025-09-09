'''Settings for Alien Invasion game.'''
class Settings:
    def __init__(self):
        '''Initialize the game's settings.'''
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_speed = 1
        self.ship_limit = 3

        '''Bullet settings.'''
        self.bullet_speed_factor=2
        self.bullet_width=10
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullets_allowed = 5

        '''Alien settings.'''
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        self.speedup_scale = 1.05
        self.score_scale = 1.5

        self.alien_drop_interval = 500  # 每 秒下降一次

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game.'''
        self.ship_speed = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed settings.'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

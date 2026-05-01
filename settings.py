class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (100, 0, 20)
        self.ship_speed = 5
        self.bullet_speed = 8
        self.bullet_limit = 3

        # Alien movement
        self.alien_speed = 1.5
        self.fleet_drop_speed = 20
        self.fleet_direction = 1   # 1 = right, -1 = left

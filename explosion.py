import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """Brief animated explosion drawn directly to the screen."""

    def __init__(self, screen, center):
        super().__init__()
        self.screen = screen
        self.center = center
        self.lifetime = 22
        self.max_lifetime = 22
        self.max_radius = 30

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

    def draw_explosion(self):
        progress = 1.0 - (self.lifetime / self.max_lifetime)
        radius = max(4, int(self.max_radius * progress))

        # Outer ring: fades from orange to dark red
        r = 255
        g = max(0, int(165 * (1.0 - progress)))
        outer_color = (r, g, 0)
        pygame.draw.circle(self.screen, outer_color, self.center, radius)

        # Bright inner core
        inner_radius = max(2, radius // 2)
        brightness = int(255 * (self.lifetime / self.max_lifetime))
        inner_color = (255, 255, brightness)
        pygame.draw.circle(self.screen, inner_color, self.center, inner_radius)

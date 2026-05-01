import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, screen, settings, x, y):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.width = 36
        self.height = 28

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_alien()

        # image is required by pygame.sprite.Group.draw()
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Float x for smooth sub-pixel horizontal movement
        self.x = float(self.rect.x)

    def _draw_alien(self):
        w, h = self.width, self.height
        body_color = (60, 200, 60)
        outline_color = (20, 120, 20)
        eye_color = (255, 50, 50)

        # Body
        pygame.draw.ellipse(self.surface, body_color, (4, 8, w - 8, h - 8))
        pygame.draw.ellipse(self.surface, outline_color, (4, 8, w - 8, h - 8), 2)

        # Head dome
        pygame.draw.ellipse(self.surface, body_color, (8, 0, w - 16, 16))
        pygame.draw.ellipse(self.surface, outline_color, (8, 0, w - 16, 16), 2)

        # Eyes
        pygame.draw.circle(self.surface, eye_color, (w // 2 - 6, 10), 4)
        pygame.draw.circle(self.surface, eye_color, (w // 2 + 6, 10), 4)

        # Antennae
        pygame.draw.line(self.surface, outline_color, (10, 4), (4, 0), 2)
        pygame.draw.line(self.surface, outline_color, (w - 10, 4), (w - 4, 0), 2)

        # Side arms
        pygame.draw.line(self.surface, outline_color, (4, 14), (0, 20), 2)
        pygame.draw.line(self.surface, outline_color, (w - 4, 14), (w, 20), 2)
        pygame.draw.line(self.surface, outline_color, (4, 20), (0, 26), 2)
        pygame.draw.line(self.surface, outline_color, (w - 4, 20), (w, 26), 2)

    def check_edges(self):
        """Return True if this alien is touching either side of the screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = int(self.x)

import pygame


class Ship:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Build the ship surface (40x60 triangle-style shape)
        self.width = 40
        self.height = 60
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw the ship body (light gray)
        body_color = (180, 180, 200)
        cockpit_color = (100, 180, 255)
        thruster_color = (255, 140, 0)

        # Main hull: filled triangle pointing up
        hull_points = [
            (self.width // 2, 0),           # nose
            (0, self.height - 10),           # bottom-left
            (self.width, self.height - 10),  # bottom-right
        ]
        pygame.draw.polygon(self.surface, body_color, hull_points)

        # Cockpit: small blue circle near the top
        pygame.draw.circle(self.surface, cockpit_color,
                           (self.width // 2, self.height // 3), 7)

        # Thruster base: rectangle at the bottom center
        thruster_rect = pygame.Rect(self.width // 2 - 6, self.height - 10, 12, 10)
        pygame.draw.rect(self.surface, thruster_color, thruster_rect)

        # Position the ship at midbottom of the screen
        self.rect = self.surface.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed

    def blitme(self):
        self.screen.blit(self.surface, self.rect)

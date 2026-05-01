import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, screen, settings, ship):
        super().__init__()
        self.screen = screen

        self.color = (255, 220, 50)
        self.width = 4
        self.height = 15
        self.speed = settings.bullet_speed

        # Create the bullet rect at the ship's midtop
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = ship.rect.midtop

        # Store position as float for smooth movement
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.speed
        self.rect.y = int(self.y)

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

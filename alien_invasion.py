import pygame
import sys

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion


def _check_events(event, ai_settings, screen, ship, bullets):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if len(bullets) < ai_settings.bullet_limit:
                bullet = Bullet(screen, ai_settings, ship)
                bullets.add(bullet)
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


def _create_fleet(ai_settings, screen, aliens):
    """Fill the top of the screen with a grid of aliens."""
    alien_width = 36
    margin_x = 20
    margin_y = 50
    spacing_x = 60
    spacing_y = 50
    rows = 3

    cols = (ai_settings.screen_width - 2 * margin_x) // spacing_x
    for row in range(rows):
        for col in range(cols):
            x = margin_x + col * spacing_x
            y = margin_y + row * spacing_y
            aliens.add(Alien(screen, ai_settings, x, y))


def _reset_fleet(ai_settings, screen, ship, aliens, bullets):
    """Clear the board and spawn a fresh fleet."""
    bullets.empty()
    aliens.empty()
    ai_settings.fleet_direction = 1
    ship.rect.midbottom = ship.screen_rect.midbottom
    ship.moving_left = False
    ship.moving_right = False
    _create_fleet(ai_settings, screen, aliens)


def _drop_and_reverse(ai_settings, aliens):
    """Drop every alien down one step and reverse horizontal direction."""
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def _check_fleet_edges(ai_settings, aliens):
    """If any alien touches a screen edge, drop the fleet and reverse."""
    for alien in aliens:
        if alien.check_edges():
            _drop_and_reverse(ai_settings, aliens)
            break


def _update_bullets(bullets, aliens, explosions):
    """Move bullets, cull off-screen ones, and detect alien hits."""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Bullet-alien collision: remove both and spawn an explosion
    hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
    for alien_list in hits.values():
        for alien in alien_list:
            explosions.add(Explosion(alien.screen, alien.rect.center))


def _update_aliens(ai_settings, screen, ship, aliens, bullets, explosions):
    """Move fleet, check for breach / ship collision / fleet cleared."""
    _check_fleet_edges(ai_settings, aliens)
    aliens.update()

    screen_rect = screen.get_rect()
    ship_top = screen_rect.bottom - ship.height

    # Any alien reached the bottom row → reset
    for alien in aliens:
        if alien.rect.bottom >= ship_top:
            _reset_fleet(ai_settings, screen, ship, aliens, bullets)
            return

    # Any alien collides directly with the ship → reset
    if pygame.sprite.spritecollide(ship, aliens, False,
                                   collided=lambda s, a: s.rect.colliderect(a.rect)):
        _reset_fleet(ai_settings, screen, ship, aliens, bullets)
        return

    # All aliens destroyed → new wave
    if not aliens:
        _reset_fleet(ai_settings, screen, ship, aliens, bullets)


def _update_screen(ai_settings, screen, ship, bullets, aliens, explosions):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets:
        bullet.draw_bullet()
    aliens.draw(screen)
    for exp in explosions:
        exp.draw_explosion()
    ship.blitme()
    pygame.display.flip()


def main():
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(screen, ai_settings)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    clock = pygame.time.Clock()

    _create_fleet(ai_settings, screen, aliens)

    while True:
        for event in pygame.event.get():
            _check_events(event, ai_settings, screen, ship, bullets)

        ship.update()
        _update_bullets(bullets, aliens, explosions)
        _update_aliens(ai_settings, screen, ship, aliens, bullets, explosions)
        explosions.update()
        _update_screen(ai_settings, screen, ship, bullets, aliens, explosions)
        clock.tick(60)


if __name__ == "__main__":
    main()

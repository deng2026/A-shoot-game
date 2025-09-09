import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, ai_settings,screen):
        super().__init__()
        self.screen = screen
        self.settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load("img/GGbond.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.last_drop_time = 0  # 上次下降的时间

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self):
        """Move the alien to the right."""
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x
        
        current_time = pygame.time.get_ticks()
        # 检查是否到了下降时间
        if  current_time - self.last_drop_time > self.settings.alien_drop_interval:
            # 执行下降操作
            self.rect.y += self.settings.fleet_drop_speed
            self.last_drop_time = current_time  # 重置计时器
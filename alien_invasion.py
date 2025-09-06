import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien 
import game_functions as gf
from game_stats import GameStats
from button import Button
from pygame.sprite import Group
from scoreboard import Scoreboard

def run_game():
    # Initialize the game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(ai_settings, screen)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    gf.create_fleet(ai_settings, screen, aliens,ship)

    pygame.display.set_caption("Alien Invasion!!!")

    play_button = Button(ai_settings, screen, "Play")
    # play_button.draw_button()

    alien=Alien(ai_settings, screen)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, play_button, stats, aliens, sb)
        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_settings, stats, screen, ship, aliens,bullets, sb)
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, sb, stats)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button,stats,sb)

run_game() 
import sys
import random
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    '''reflection of key'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
                ship.moving_right = False
    elif event.key == pygame.K_LEFT:
                ship.moving_left = False
    elif event.key == pygame.K_UP:
                ship.moving_up = False
    elif event.key == pygame.K_DOWN:
                ship.moving_down = False

def check_events(ai_settings,screen,ship,bullets,play_button,stats,aliens,sb):
    '''Check for events and handle them.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, screen, ship,aliens, bullets, play_button, mouse_x, mouse_y,sb)

        # Add more event handling as needed.

def check_play_button(ai_settings, stats, screen, ship, aliens,bullets, play_button, mouse_x, mouse_y,sb):
    '''Start a new game when the player clicks Play.'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the high score.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Create a new fleet of aliens. 
        aliens.empty()
        bullets.empty()
        #create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

def update_screen(ai_settings,screen, ship, bullets, aliens, play_button,stats,sb):
        # Fill the screen with a color.
        screen.fill(ai_settings.bg_color)
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        sb.show_score()
        if not stats.game_active:
            play_button.draw_button()
        # Make the most recently drawn screen visible.
        pygame.display.flip()

def update_bullets(ai_settings, screen, ship,aliens, bullets,sb, stats):
    '''Update position of bullets and get rid of old bullets.'''
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    print(len(bullets))
    # Check for bullet-alien collisions.
    check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens,sb, stats)

def check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens,sb, stats):
    '''Respond to bullet-alien collisions.'''
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(alien)
            sb.prep_score()
        check_high_score(stats, sb)
    if not aliens:
        # Destroy existing bullets and create a new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        # Create a new fleet of aliens.
        #create_fleet(ai_settings, screen, aliens, ship)



def fire_bullet(ai_settings, screen, ship, bullets):
    '''Fire a bullet if limit not reached yet.'''
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, aliens,ship):
    '''Create a full fleet of aliens.'''
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)

def create_random_alien(ai_settings, screen, aliens):
     '''creat a row random alien'''
     alien = Alien(ai_settings, screen)
     alien_width = alien.rect.width
     number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
     alien_num=random.randint(0, number_aliens_x - 1)
     random_numbers = random.sample(range(0, number_aliens_x), alien_num)
     for alien_location in random_numbers:
          create_alien(ai_settings, screen, aliens, alien_location)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
     ''''''
     available_space_y=(ai_settings.screen_height-3*alien_height-ship_height)
     number_rows=int(available_space_y/(2*alien_height))
     return number_rows

def create_alien(ai_settings, screen, aliens, alien_number,row_number=0):
    '''Create a single alien and place it in the fleet.'''
    alien = Alien(ai_settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens, bullets, sb):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= ai_settings.screen_height:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break
    

def update_aliens(ai_settings, stats, screen, ship, aliens,bullets,sb):
    '''Update the positions of all aliens in the fleet.'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()  #这里的Group用了alien的方法
    # if aliens:  # 确保已有外星人时才生成新行
    #     # 找到当前最上方外星人的y坐标
    #     min_y = min(alien.rect.y for alien in aliens.sprites())
    #     # 当最上方外星人下降超过自身高度时，生成新行
    #     if min_y > aliens.rect.height:
    #         create_random_alien(ai_settings, screen, aliens)

    add_alien_flag = 1
    for alien in aliens.sprites():
        if alien.y < 2 * alien.rect.height:
            add_alien_flag = 0
    if add_alien_flag == 1:
        create_random_alien(ai_settings, screen, aliens)

    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!")
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens, bullets,sb)

def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_alien_direction(ai_settings, alien)
            # break

def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change the fleet's direction.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def change_alien_direction(ai_settings,alien):
     '''change a alien's way'''
     
     ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb):
    '''Respond to ship being hit by alien.'''
    if stats.ships_left > 0:
        # Decrement ships_left and update the scoreboard.
        stats.ships_left -= 1
        # update_scoreboard(stats, screen)
        sb.prep_ships()
        # Empty the lists of aliens and bullets.
        aliens.empty()
        bullets.empty()

        #create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False

def check_high_score(stats, sb):
    '''Check to see if there's a new high score.'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

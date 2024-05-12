import pygame
import random
pygame.display.init()
pygame.font.init()


def menu():
    print('menu()')
    global run
    loop = True
    while loop:
        global text_score
        clock.tick(0)
        screen.fill((255, 255, 255))

        # render font to image
        text_score = font.render('Score: ' + str(score), True, (0, 0, 0))
        # temp block - text_miss = font.render('Miss: ' + str(miss), True, (0, 0, 0))
        text_menu1 = menu_font.render('Press Escape to exit', True, (0, 0, 0))
        text_menu2 = menu_font.render('Press Enter to continue', True, (0, 0, 0))

        # add rendered images to screen
        screen.blit(text_hiscore, (0, 0))
        screen.blit(text_score, (0, 30))
        # temp block - screen.blit(text_miss, (0, 60))
        screen.blit(text_menu1, (0, (screen_height/2-40)))
        screen.blit(text_menu2, (0, screen_height/2))
        pygame.display.flip()
        response = True
        while response:
            for menu_event in pygame.event.get():
                if events.type == pygame.QUIT:
                    print('\npygame.QUIT')
                    response = False
                    run = False
                if menu_event.type == pygame.KEYDOWN:
                    if menu_event.key == pygame.K_ESCAPE:
                        print('\nescape')
                        response = False
                        print('response = False')
                        run = False
                        print('run = False')
                        print('quit()')
                        quit()
                    elif menu_event.key == pygame.K_RETURN:
                        print('\nkey pressed, enter')
                        response = False
                        print('event for loop break')
                        break
        print('response while loop break')
        break
    print('return from menu()')
    return

# player dimensions, screen dimensions, font type, line placements
player_diameter = 120
stage_size = 5 # TO-DO: Feature: Select stage_size before game starts

screen_width = player_diameter * stage_size
screen_height = 540

font = pygame.font.SysFont('franklingothicbook', 21)
menu_font = pygame.font.SysFont('franklingothicbook', 36)
score = 0
hiscore = 0
miss = 0
life = 3

player_x_pos = round((screen_width/stage_size)+(round(player_diameter/2)))
player_y_pos = round(screen_height-(round(player_diameter/2)))

obstacle_diameter = round(player_diameter/2)
obstacle_x_pos = round((screen_width/2))
# TO-DO: Refactor list of possible obstacle spawn points using list comprehension, based on player diameter
# obstacle_x_random = [round((screen_width/2)), round((screen_width/2))-round(screen_width/3),
#                      round((screen_width/2))+round(screen_width/3)]
obstacle_x_random = [player_diameter*(size+1) for size in range(stage_size)]
print(obstacle_x_random, screen_width)

obstacle_y_pos = round(obstacle_diameter/2)
obstacle_y_speed = 10

# generate coordinates of lanes to draw later
lanes_list = []
for i in range(stage_size):
    lanes_list.append([((player_diameter*i)-1,0), ((player_diameter*i)-1, screen_height)])

# make screen, title
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Ball On Three Lanes")

# game loop
tick = 30
clock = pygame.time.Clock()
run = True
while run:

    # render text to image
    text_score = font.render('Score: '+str(score), True, (0, 0, 0))
    text_hiscore = font.render('High Score: ' + str(hiscore), True, (0, 0, 0))
    text_life = font.render('Life: ' + str(life), True, (0, 0, 0))

    # fill screen with white
    screen.fill((255, 255, 255))

    # draw lane lines
    for lane in lanes_list:
        pygame.draw.lines(screen, (0, 0, 0), True, lane, 2)

    # add rendered text images to screen
    screen.blit(text_hiscore, (0, 0))
    screen.blit(text_score, (0, 30))
    screen.blit(text_life, (0, 60))

    # obstacle
    obstacle = pygame.draw.circle(screen, (255, 0, 0), [obstacle_x_pos, obstacle_y_pos], round(obstacle_diameter/2) - 1)

    # draw player
    player = pygame.draw.circle(screen, (0, 0, 0), [player_x_pos, player_y_pos], round(player_diameter/2)-1)

    # event triggers
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
        if events.type == pygame.KEYDOWN:

            # escape key brings up menu
            if events.key == pygame.K_ESCAPE:
                print('escape key pressed')
                menu()

            # left right keys to set player x positions for player drawing
            if events.key == pygame.K_LEFT:
                player_x_pos -= round(player_diameter)
            if events.key == pygame.K_RIGHT:
                player_x_pos += round(player_diameter)

    # if player moves out of x bounds, reset player_x_pos to respective side of screen
    if player_x_pos < 0:
        player_x_pos = round(player_diameter/2)
    if player_x_pos > screen_width:
        player_x_pos = round(screen_width - player_diameter/2)

    # obstacle movement check & loop
    if 0 < obstacle_y_pos < screen_height:
        obstacle_y_pos += obstacle_y_speed

    # score counting
    if obstacle_y_pos == player_y_pos:
        if obstacle_x_pos <= player_x_pos+1 and obstacle_x_pos >= player_x_pos-1:
            score += 1
            tick += 1
        if score >= hiscore+1:
            hiscore += 1

    # miss counting
    if obstacle_y_pos >= player_y_pos:
        if obstacle_x_pos != player_x_pos:
            miss += 1
            life -= 1
        elif obstacle_x_pos <= player_x_pos+1 and obstacle_x_pos >= player_x_pos-1:
            score += 1
            tick += 1
            if score >= hiscore+1:
                hiscore += 1
        obstacle_y_pos = round(obstacle_diameter/4)
        obstacle_x_pos = random.choice(obstacle_x_random)-round(obstacle_diameter)
        
    if life < 1:
        life = 3
        score = 0
        tick = 30
        menu()

    pygame.display.flip()
    clock.tick(tick)

quit()

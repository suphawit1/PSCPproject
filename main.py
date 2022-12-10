import pygame
from Fighter import Fighter

pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle of Stickman")

#set framerate
clock = pygame.time.Clock()
FPS = 60


#define colors
Red = (255, 0, 0)
Yellow = (255, 255, 0)
White = (255, 255, 255)

#define game variables
intro_count = 3
las_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

bg_image = pygame.image.load("assets/bg2.png").convert_alpha()


#load victory image
victory_img = pygame.image.load("assets/victory.png").convert_alpha()

#define font
count_font = pygame.font.Font("assets/turok.ttf", 80)
score_font = pygame.font.Font("assets/turok.ttf", 30)
subtext = pygame.font.Font("assets/turok.ttf", 20)

#function for drawing text

def load_images(sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * 400, y * 410, 400, 400)
                temp_img_list.append(pygame.transform.scale(temp_img, (400, 400)))
            animation_list.append(temp_img_list)
        return animation_list

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#function fighter health bars 
def draw_health_bar(hrealth, x, y):
    ratio = hrealth / 100
    pygame.draw.rect(screen, White, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, Red, (x, y, 400, 30))
    pygame.draw.rect(screen, Yellow, (x, y, 400 * ratio, 30))

#mode selection interface
modeselect = True
mode_bgimmage = pygame.image.load("assets/maxresdefault.jpg").convert_alpha()
playmode = 0
press = False
while True:
    while modeselect:
        clock.tick(FPS)
        if press == True and pygame.time.get_ticks() - keypressdelay > 300:
            press = False
        key = pygame.key.get_pressed()
        scaled_bg = pygame.transform.scale(mode_bgimmage, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))
        draw_text("Player vs Player", score_font, Red, 200, 400)
        draw_text("Play with Bot", score_font, Red, 600, 400)
        draw_text("(Press Enter to continue)", subtext, Red, 0, 575)
        
        if playmode == 0:
            pygame.draw.rect(screen, Red, pygame.Rect(182, 370, 250, 100), 5)
        elif playmode == 1:
            pygame.draw.rect(screen, Red, pygame.Rect(585, 370, 210, 100), 5)
        if (key[pygame.K_a] or key[pygame.K_d] or key[pygame.K_LEFT] or key[pygame.K_RIGHT]) and press == False:
            keypressdelay = pygame.time.get_ticks()
            press = True
            if playmode == 0:
                playmode = 1
            else:
                playmode = 0
        if key[pygame.K_RETURN] and press == False:
            press = True
            keypressdelay = pygame.time.get_ticks()
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()

    charrector_selection = True
    charselect1 = 0
    charselect2 = 0
    playerorbot = {0:"Player 2", 1:"Bot"}
    player = playerorbot[playmode]
    keypressdelay = pygame.time.get_ticks()
    charname = ["stickman", "Hammer", "samurai"]
    idle_spritesheet = pygame.image.load("assets/Sprite Sheet/Idle.png").convert_alpha()
    idle_step = [7, 9, 7]
    idle_list = load_images(idle_spritesheet, idle_step)
    update_time = pygame.time.get_ticks()
    update_time2 = pygame.time.get_ticks()
    idle_cooldow = 80
    frame_index = 0
    frame_index2 = 0
    while charrector_selection:
        clock.tick(FPS)
        charrector1 = charname[charselect1]
        charrector2 = charname[charselect2]
        if press == True and (pygame.time.get_ticks() - keypressdelay > 500):
            press = False
        key = pygame.key.get_pressed()
        scaled_bg = pygame.transform.scale(mode_bgimmage, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))
        draw_text("Player 1", score_font, Red, 100, 50)
        draw_text(player, score_font, Red, 750, 50)
        draw_text("(Press Enter to continue)", subtext, Red, 0, 575)
        draw_text(charrector1, score_font, Red, 100, 500)
        draw_text(charrector2, score_font, Red, 730, 500)
        draw_text("A-D to select charlector", subtext, Red, 60, 545)
        draw_text("LEFT-RIGHT to select charlector", subtext, Red, 650, 545)
        image1 = idle_list[charselect1][frame_index]
        image2 = idle_list[charselect2][frame_index2]
        image2 = pygame.transform.flip(image2, True, False)
        screen.blit(image1, (20,60))
        screen.blit(image2, (580,60))
        if pygame.time.get_ticks() - update_time > idle_cooldow:
            frame_index += 1
            update_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - update_time2 > idle_cooldow:
            frame_index2 += 1
            update_time2 = pygame.time.get_ticks()
        if frame_index >= len(idle_list[charselect1]):
            frame_index = 0
        if frame_index2 >= len(idle_list[charselect2]):
            frame_index2 = 0
        
        if key[pygame.K_a] and press == False:
            if charselect1 == 0:
                charselect1 = 2
            else:
                charselect1 -= 1
            frame_index = 0
            keypressdelay = pygame.time.get_ticks()
            press = True
        if key[pygame.K_d] and press == False:
            if charselect1 == 2:
                charselect1 = 0
            else:
                charselect1 += 1
            frame_index = 0
            keypressdelay = pygame.time.get_ticks()
            press = True
        if key[pygame.K_LEFT] and press == False:
            if charselect2 == 0:
                charselect2 = 2
            else:
                charselect2 -= 1
            frame_index2 = 0
            keypressdelay = pygame.time.get_ticks()
            press = True
            
        if key[pygame.K_RIGHT] and press == False:
            if charselect2 == 2:
                charselect2 = 0
            else:
                charselect2 += 1
            frame_index2 = 0
            keypressdelay = pygame.time.get_ticks()
            press = True

        if key[pygame.K_RETURN] and press == False:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
        

    charrector = {0:([348, 0.7, [120, 80]], [7, 5, 1, 4, 4, 3, 6], 0), 1:([35, 7, [12, 9]], [9, 6, 1, 7, 3, 7], 1), 2:([400, 0.6, [150, 100]], [7, 6, 1, 7, 3, 9], 1)}
    demo = pygame.image.load("assets/Sprite Sheet/sheetdemo.png").convert_alpha()
    hammer = pygame.image.load("assets/Sprite Sheet/hammer.png").convert_alpha()
    samurai = pygame.image.load("assets/Sprite Sheet/samurai.png").convert_alpha()
    charsheet = [demo, hammer, samurai]
    STICKMAN_DATA, ANIMATION_STEP, NUMBER_ATTACK_TYPE = charrector[charselect1]
    STICKMAN_DATA1, ANIMATION_STEP1, NUMBER_ATTACK_TYPE1 = charrector[charselect2]
    stickman_sheet = charsheet[int(charselect1)]
    stickman_sheet1 = charsheet[int(charselect2)]

    #show tag if same charctor
    tag = False
    if stickman_sheet == stickman_sheet1:
        tag = True



    fighter_1 = Fighter(1, 200, 310, False, STICKMAN_DATA, stickman_sheet, ANIMATION_STEP)
    fighter_2 = Fighter(2+playmode, 700, 310, True, STICKMAN_DATA1, stickman_sheet1, ANIMATION_STEP1)
    run = True
    while run:

        clock.tick(FPS)

        draw_bg()

        key = pygame.key.get_pressed()

        #show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, Red, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, Red, 580, 60)
        draw_text("Press ESC to go back to main manu", subtext, Red, 0, 575)
        
        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            #display count timer
            draw_text(str(intro_count), count_font, Red, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            #update count timer
            if (pygame.time.get_ticks() - las_count_update) >= 1000:
                intro_count -= 1
                las_count_update = pygame.time.get_ticks()

        #update fighter
        fighter_1.update(NUMBER_ATTACK_TYPE)
        fighter_2.update(NUMBER_ATTACK_TYPE1)

        fighter_1.draw(screen, tag)
        fighter_2.draw(screen, tag)

        #check for player defeat
        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            #display victory image
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, STICKMAN_DATA, stickman_sheet, ANIMATION_STEP)
                fighter_2 = Fighter(2+playmode, 700, 310, True, STICKMAN_DATA1, stickman_sheet1, ANIMATION_STEP1)
        if key[pygame.K_ESCAPE]:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    
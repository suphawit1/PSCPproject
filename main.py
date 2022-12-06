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

#charactor selection
charselect = input("Charactor Select -> ")
if charselect == "0":
    STICKMAN_SIZE = 348
    STICKMAN_SCALE = 0.7
    STICKMAN_OFFSET = [120, 80]
    STICKMAN_DATA = [STICKMAN_SIZE, STICKMAN_SCALE, STICKMAN_OFFSET]
    stickman_sheet = pygame.image.load("assets/Sprite Sheet/sheetdemo.png").convert_alpha()
    TEST_ANIMATION_STEP = [7, 5, 1, 4, 4, 3, 6]
    NUMBER_ATTACK_TYPE = 0 #0 = 2 atktpye
elif charselect == "1":
    STICKMAN_SIZE = 35
    STICKMAN_SCALE = 7
    STICKMAN_OFFSET = [12, 9]
    STICKMAN_DATA = [STICKMAN_SIZE, STICKMAN_SCALE, STICKMAN_OFFSET]
    stickman_sheet = pygame.image.load("assets/Sprite Sheet/hammer.png").convert_alpha()
    TEST_ANIMATION_STEP = [9, 6, 1, 7, 3, 7]
    NUMBER_ATTACK_TYPE = 1 #1 = 1 atktype
elif charselect == "2":
    STICKMAN_SIZE = 400
    STICKMAN_SCALE = 0.6
    STICKMAN_OFFSET = [150, 100]
    STICKMAN_DATA = [STICKMAN_SIZE, STICKMAN_SCALE, STICKMAN_OFFSET]
    stickman_sheet = pygame.image.load("assets/Sprite Sheet/samurai.png").convert_alpha()
    TEST_ANIMATION_STEP = [7, 6, 1, 7, 3, 9]
    NUMBER_ATTACK_TYPE = 1 #1 = 1 atktype


#define game variables
intro_count = 0
las_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter cariable
#STICKMAN_SIZE = 35
#STICKMAN_SCALE = 7
#STICKMAN_OFFSET = [12, 9]
#STICKMAN_DATA = [STICKMAN_SIZE, STICKMAN_SCALE, STICKMAN_OFFSET]
bg_image = pygame.image.load("assets/bg2.png").convert_alpha()

#sheet load
#stickman_sheet = pygame.image.load("assets/Hammer/hammer.png").convert_alpha()

#load victory image
victory_img = pygame.image.load("assets/victory.png").convert_alpha()

#define font
count_font = pygame.font.Font("assets/turok.ttf", 80)
score_font = pygame.font.Font("assets/turok.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
#set step animation
#TEST_ANIMATION_STEP = [9, 6, 1, 7, 3, 7]
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#function fighter health bars 
def draw_health_bar(hrealth, x, y):
    ratio = hrealth / 100
    pygame.draw.rect(screen, White, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, Red, (x, y, 400, 30))
    pygame.draw.rect(screen, Yellow, (x, y, 400 * ratio, 30))

fighter_1 = Fighter(1, 200, 310, False, STICKMAN_DATA, stickman_sheet, TEST_ANIMATION_STEP)
fighter_2 = Fighter(2, 700, 310, True, STICKMAN_DATA, stickman_sheet, TEST_ANIMATION_STEP)
run = True
while run:

    clock.tick(FPS)

    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, Red, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, Red, 580, 60)
    
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
    fighter_2.update(NUMBER_ATTACK_TYPE)

    fighter_1.draw(screen)
    fighter_2.draw(screen)

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
            fighter_1 = Fighter(1, 200, 310, False, STICKMAN_DATA, stickman_sheet, TEST_ANIMATION_STEP)
            fighter_2 = Fighter(2, 700, 310, True, STICKMAN_DATA, stickman_sheet, TEST_ANIMATION_STEP)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
pygame.quit()

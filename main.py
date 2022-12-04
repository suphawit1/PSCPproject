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
#define colors
Red = (255, 0, 0)
Yellow = (255, 255, 0)
White = (255, 255, 255)

#define fighter cariable
#STICKMAN_SIZE = 35
#STICKMAN_SCALE = 7
#STICKMAN_OFFSET = [12, 9]
#STICKMAN_DATA = [STICKMAN_SIZE, STICKMAN_SCALE, STICKMAN_OFFSET]
bg_image = pygame.image.load("assets/bg2.png").convert_alpha()

#sheet load
#stickman_sheet = pygame.image.load("assets/Hammer/hammer.png").convert_alpha()


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

fighter_1 = Fighter(200, 310, False, STICKMAN_DATA, stickman_sheet, TEST_ANIMATION_STEP)
fighter_2 = Fighter(700, 310, True, STICKMAN_DATA, stickman_sheet, TEST_ANIMATION_STEP)
run = True
while run:

    clock.tick(FPS)

    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
    #fighter_2.move()
    
    #update fighter
    fighter_1.update(NUMBER_ATTACK_TYPE)
    fighter_2.update(NUMBER_ATTACK_TYPE)

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
pygame.quit()

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

#define fighter cariable
STICKMAN_SIZE = 348
STICKMAN_SCALE = 0.7
STICKMAN_OFFSET = [120, 80]
STICKMAN_DATA = [STICKMAN_SIZE, STICKMAN_SCALE, STICKMAN_OFFSET]
bg_image = pygame.image.load("assets/bg2.png").convert_alpha()

#sheet load
test_sheet = pygame.image.load("assets/demostick/sheetdemo.png").convert_alpha()

#set step animation
TEST_ANIMATION_STEP = [7, 5, 1, 4, 4, 3, 6]
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#function fighter health bars 
def draw_health_bar(hrealth, x, y):
    ratio = hrealth / 100
    pygame.draw.rect(screen, White, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, Red, (x, y, 400, 30))
    pygame.draw.rect(screen, Yellow, (x, y, 400 * ratio, 30))

fighter_1 = Fighter(200, 310, False, STICKMAN_DATA, test_sheet, TEST_ANIMATION_STEP)
fighter_2 = Fighter(700, 310, True, STICKMAN_DATA, test_sheet, TEST_ANIMATION_STEP)
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
    fighter_1.update()
    fighter_2.update()

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
pygame.quit()

import pygame
import random

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.healthbot = 100
        self.alive = True
        self.bot = 4
        self.state = pygame.time.get_ticks()
        self.fallback = pygame.time.get_ticks()
        self.randomaction = [4]
    

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list



    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        #keypress

        key = pygame.key.get_pressed()
        #can only perfrom other action if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False and self.hit == False:
            #check player 1 control
            if self.player == 1:
            #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    #which attack type were used
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2


            #check player 2 control
            if self.player == 2:
            #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    #which attack type were used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2
            if key[pygame.K_TAB]:
                if self.tag == True:
                    self.tag = False
                else:
                    self.tag = True


            #nolmalbot
            if self.player == 3:
                attacking_range = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
                goforatk = [1, 0, 0, 0] #1 changestate
                if self.healthbot > self.health:
                    if self.rect.x - (self.offset[0] * self.image_scale) < target.rect.x - (target.offset[0] * target.image_scale):
                        self.randomaction = [0, 0, 3]
                    else:
                        self.randomaction = [1, 1, 3]
                    self.healthbot = self.health
                    
                elif pygame.time.get_ticks()- self.fallback > 50:
                    state = random.choice(goforatk)
                    self.fallback = pygame.time.get_ticks()
                    if attacking_range.colliderect(target.rect) and state == 1:
                        self.randomaction = [2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4]#0runleft #1runright #2attack #3jump #4 idle
                    elif self.rect.x - (self.offset[0] * self.image_scale) < target.rect.x - (target.offset[0] * target.image_scale) and state == 1:
                        self.randomaction = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 4, 4, 4, 4, 4, 4, 4]
                    elif self.rect.x - (self.offset[0] * self.image_scale) > target.rect.x - (target.offset[0] * target.image_scale) and state == 1:
                        self.randomaction = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4]
                changestate_cooldown = 50
                if pygame.time.get_ticks() - self.state > changestate_cooldown:
                    self.bot = (random.choice(self.randomaction))
                    self.state = pygame.time.get_ticks()
                if self.bot == 0:
                    dx = -SPEED
                    self.running = True
                elif self.bot == 1:
                    dx = SPEED
                    self.running = True
                elif self.bot == 2:
                    self.attack(target)
                    attacktype = [1, 2]
                    y = (random.choice(attacktype))
                    self.attack_type = y
                elif self.bot == 3 and self.jump == False:
                    jumpdirection = [0, 1]
                    z = random.choice(jumpdirection)
                    if z == 0:
                        dx, self.vel_y = -SPEED, -30
                    elif z == 1:
                        dx, self.vel_y = SPEED, -30
                    self.jump = True


        #apply gravity    
        self.vel_y += GRAVITY
        dy += self.vel_y
        
        #player on screen
        if self.rect.left + dx < 0:
            dx = 0 -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 -self.rect.bottom
        
        #ensure players face to each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        #attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #update player position
        self.rect.x += dx
        self.rect.y += dy

    #animation update
    def update(self, animationrow):
        #check action
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6 - animationrow)
        elif self.hit == True:
            self.update_action(5 - animationrow)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4 - animationrow)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)
        animation_cooldow = [80, 50, 50, 60, 80, 80, 80]
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldow[self.action]:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            #if player dead
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #if attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 30
                #check if damage was taken
                if self.action == 5 or self.action == 4:
                    self.hit = False
                    #if was player in middle of attck
                    self.attacking = False
                    self.attack_cooldown = 30

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if self.action == 5 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 30
            if attacking_rect.colliderect(target.rect) and self.attacking == True:
                target.health -= 10
                target.hit = True

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    
    def draw(self, surface, tag):
        font = pygame.font.Font("assets/turok.ttf", 30)
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        
        if tag == True:
            if self.player == 1:
                img = font.render("P1", True, (0, 0, 255))
            elif self.player == 2:
                img = font.render("P2", True, (0, 255, 0))
            else:
                img = font.render("BOT", True, (0, 255, 0))
            surface.blit(img, (self.rect.x+90 - (self.offset[0] * self.image_scale), self.rect.y-20 - (self.offset[1] * self.image_scale)))

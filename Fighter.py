import pygame

class Fighter():
    def __initpp__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
    

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        #keypress

        key = pygame.key.get_pressed()
        #can only perfrom other action if not currently attacking
        if self.attacking == False:
            #movement
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED
            #jump
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            #attack
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                #which attack type were used
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2
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
        
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            print("HIT")
        
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)


    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
import pygame

class Fighter():
    def _init_(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))


def draw(self, surface):
    pygame.draw.rect(surface, (255, 0, 0), self.rect)

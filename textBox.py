import pygame


class text_box:
    def __init__(self, text, size, color, background, location):
        self.background = background
        self.text_color = color

        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.size = self.text_rect.size
        self.surface = pygame.surface.Surface(self.size)
        self.rect = self.surface.get_rect(topleft=location)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def update(self):
        self.surface.fill(self.background)
        self.size = self.text_rect.size
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.surface.blit(self.text_surface, self.text_rect)
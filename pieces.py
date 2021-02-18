import pygame

class piece:
    offset_x = 0
    def __init__(self, pos, team, rects):
        self.pos = pos
        self.team = team
        self.rects = list()
        for rectIt in range(len(rects)):
            self.rects.append([pygame.rect.Rect(rects[rectIt]), [0, 0]])
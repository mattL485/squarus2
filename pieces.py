import pygame

class piece:
    drag = False
    square_count = 0
    square_list = list()
    def __init__(self, pos, team, rects):
        self.pos = pos
        self.team = team
        self.rects = list()
        for rectIt in range(len(rects)):
            self.rects.append([pygame.rect.Rect(rects[rectIt]), [0, 0]])
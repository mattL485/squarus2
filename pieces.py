import pygame

class piece:
    drag = False
    set = False
    square_count = 0
    square_list = list()
    def __init__(self, pos, team, rects):
        self.pos = pos  # this is the location of the piece in reference to the first piece in the rects list
        self.team = team  # this is the integer that indicates the piece's team.
        self.rects = list()  # this is the list of rectangles that are placed on the board
        self.start_rects = list()  # this is an un-utilized list
        for rectIt in range(len(rects)):
            self.rects.append([pygame.rect.Rect(rects[rectIt]), [0, 0]])

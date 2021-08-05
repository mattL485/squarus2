import pygame

class piece:

    def __init__(self, ID, team, pos, rects):
        self.pos = pos  # this is the location of the piece in reference to the first piece in the rects list
        self.team = team  # this is the integer that indicates the piece's team.
        self.rects = list()  # this is the list of rectangles that are placed on the board
        self.start_rects = list()  # this is an un-utilized list
        self.drag = False
        self.set = False
        self.valid = False
        self.square_count = 0
        self.square_list = list()  # this list stores the square-ID and the board space index.
        self.ID = ID
        for rectIt in range(len(rects)):
            self.rects.append([pygame.rect.Rect(rects[rectIt]), [0, 0]])

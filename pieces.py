import pygame
import copy

class piece:

    def __init__(self, ID, team, pos, rects):
        self.pos = pos  # this is the location of the piece in reference to the first piece in the rects list
        self.team = team  # this is the integer that indicates the piece's team.
        self.rects = list()  # this is the list of rectangles that are placed on the board
        self.drag = False
        self.set = False
        self.valid = False
        self.square_count = 0
        self.square_list = list()  # this list stores the square-ID and the board space index.
        self.ID = ID
        self.snapped = False
        for rectIt in range(len(rects)):
            self.rects.append([pygame.rect.Rect(rects[rectIt]), [0, 0]])

        # this is the list that is used to store the original piece location.
        self.start_rects = copy.deepcopy(self.rects)
        self.relational_pos = self.convert_to_relational(self.rects)

    # this helper method converts a list of positions into a list of positional relations that can be used
    # to check the arrangements for a piece.
    def convert_to_relational(self, rects):
        relational_list = list()
        if not rects:
            print('error: empty positional rects list!')
            return
        last_pos = rects[0]
        for rect in rects:
            diff = [rect[0].x - last_pos[0].x, rect[0].y - last_pos[0].y]
            relational_list.append([diff[0] / 50, diff[1] / 50])
            last_pos.append(rect)
        return relational_list

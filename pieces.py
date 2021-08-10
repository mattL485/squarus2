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
        self.ID = ID    # this ID is used to re-assemble a piece if it becomes arranged incorrectly
        self.snapped = False    # this piece stores whether a piece has been snapped or not.
        self.corners = list()
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
        rects.sort()
        last_pos = rects[0]
        for rect in rects:
            diff = [rect[0].x - last_pos[0].x, rect[0].y - last_pos[0].y]
            relational_list.append([diff[0] / 50, diff[1] / 50])
            last_pos.append(rect)
        return relational_list

    def get_corners(self, relations, rects):
        corners = list()
        rect_index = 0
        for relation in relations:
            LEFT = False
            UP = False
            RIGHT = False
            DOWN = False
            adjacent_piece_count = 0
            for rel_index in range(len(relations)):
                if rel_index < len(relations) and relations[rel_index] != relation:
                    diff_x = relations[rel_index][0] - relation[0]
                    diff_y = relations[rel_index][1] - relation[1]
                    if diff_x == -1 and diff_y == 0:
                        LEFT = True
                        adjacent_piece_count += 1
                    elif diff_x == 1 and diff_y == 0:
                        RIGHT = True
                        adjacent_piece_count += 1
                    if diff_x == 0 and diff_y == -1:
                        UP = True
                        adjacent_piece_count += 1
                    elif diff_x == 0 and diff_y == 1:
                        DOWN = True
                        adjacent_piece_count += 1
            if LEFT:
                if adjacent_piece_count == 1:
                    corners.append(rects[rect_index][0].topright)
                    corners.append(rects[rect_index][0].bottomright)
                elif adjacent_piece_count == 2:
                    if UP:
                        corners.append(rects[rect_index][0].bottomright)
                    elif DOWN:
                        corners.append(rects[rect_index][0].topright)
            elif RIGHT:
                if adjacent_piece_count == 1:
                    corners.append(rects[rect_index][0].topleft)
                    corners.append(rects[rect_index][0].bottomleft)
                elif adjacent_piece_count == 2:
                    if UP:
                        corners.append(rects[rect_index][0].bottomleft)
                    elif DOWN:
                        corners.append(rects[rect_index][0].topleft)
            elif UP:
                if adjacent_piece_count == 1:
                    corners.append(rects[rect_index][0].bottomright)
                    corners.append(rects[rect_index][0].bottomleft)
            elif DOWN:
                if adjacent_piece_count == 1:
                    corners.append(rects[rect_index][0].topright)
                    corners.append(rects[rect_index][0].topleft)
            elif adjacent_piece_count == 0:
                corners.append(rects[rect_index][0].topright)
                corners.append(rects[rect_index][0].bottomright)
                corners.append(rects[rect_index][0].topleft)
                corners.append(rects[rect_index][0].bottomleft)
            rect_index += 1
        return corners


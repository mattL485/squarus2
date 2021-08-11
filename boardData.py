from pieces import piece
import copy

class board_data:
    num_teams = 2
    occupied = list()
    piece_ID = list()
    min_x = 850
    min_y = 100
    start_min_x = copy.deepcopy(min_x)  # this is a copy of the left side so that min_x can be reset
    start_min_y = copy.deepcopy(min_y)  # this is a copy of the left side so that min_x can be reset
    max_x = 1500
    max_y = 800

    def __init__(self):
        pass

    def import_pieces(self, filename):
        file = open(filename, "r")
        input_text = file.readlines()
        imported_pieces = list()
        id_count = [0]
        for line in input_text:
            piece_team = 0
            relational_list, coord_list, rects_list = list(), list(), list()
            if line[0].isnumeric():
                piece_team = int(line[0])
                line = line[1:]
                line.strip()
                # this loop extracts the relative positions
                negative = False
                for char in line:
                    if char.isnumeric():
                        if negative:
                            coord_list.append(-1 * int(char))
                            negative = False
                        else:
                            coord_list.append(int(char))
                    elif char == '-':
                        negative = True
                    elif char == ']':
                        relational_list.append(copy.deepcopy(coord_list))
                        coord_list.clear()
                imported_pieces.append(self.place_pieces(relational_list, id_count, piece_team))
                for i in range(self.num_teams - 1):
                    imported_pieces.append(copy.deepcopy(imported_pieces[len(imported_pieces) - 1]))
                    imported_pieces[len(imported_pieces) - 1].team += 1
                    imported_pieces[len(imported_pieces) - 1].ID = id_count[0]
                    id_count[0] += 1
            elif line[0] == '#':
                continue
            elif str.__contains__(line, "numplayers="):
                self.num_teams = int(line[len(line) - 2])
                continue
            else:
                print("Please ensure that pieces are formatted as follows: 1 [0,0],[0,1],[1,1]- exiting.")
                exit
        return imported_pieces

    def place_pieces(self, relational_list, id_count, piece_team):
        rects_list = list()
        # this is the logic for deciding where the piece will go:
        rel_min_x = min(relational_list, key=lambda x: x[0])
        rel_min_y = min(relational_list, key=lambda x: x[1])
        rel_max_x = max(relational_list, key=lambda x: x[0])
        rel_max_y = max(relational_list, key=lambda x: x[1])
        diff_x = rel_max_x[0] - rel_min_x[0] + 2
        diff_y = rel_max_y[1] - rel_min_y[1] + 1
        # this adds the piece with the smallest x value first.
        if (self.min_x + 50 * diff_x) > self.max_x:
            self.min_x = copy.deepcopy(self.start_min_x)
            self.min_y += 300
        temp_min = [self.min_x - 50 * rel_min_x[0], self.min_y - 50 * rel_min_x[1]]
        for relation in relational_list:
            rects_list.append((temp_min[0] + relation[0] * 50, temp_min[1] + relation[1] * 50, 50, 50))
        return_piece = piece(id_count[0], piece_team, temp_min, rects_list)
        self.min_x += (diff_x - 0.5) * 50
        id_count[0] += 1
        return return_piece
    # TODO: add validity board counter to keep track of how many pieces should be on each board after setting.


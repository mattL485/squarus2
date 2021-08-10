import sys, pygame, math
from pieces import piece
from boardData import board_data
from textBox import text_box
import copy

pygame.init()
board_data = board_data()

print(pygame.display.Info())

# display initializations
# TODO: extract display info and scale
size = width, height = 1536, 864
speed = [2, 2]  # moving down and right
black = 0, 0, 0  # standard rgb value
screen = pygame.display.set_mode(size)

# model initializations
minDimension = min(size)
maxSquares = round((minDimension - 200) / 50)
maxSquares = 12    # comment out to make maximum square size dynamic
board, board_rect = list(), list()
for row in range(maxSquares):
    for col in range(maxSquares):
        # board and board_rect creation
        board.append(pygame.image.load("50-50BoardTile.png"))
        board_rect.append(board[len(board) - 1].get_rect())
        board_rect[len(board) - 1].x = col * 50
        board_rect[len(board) - 1].y = row * 50
        # board_data insertion
        board_data.occupied.append(False)
        board_data.piece_ID.append(False)

# font and text initializations:
quit_text = text_box('Quit', 32, (0, 0, 0), (255, 255, 255), (1400, 50))
set_text = text_box('Confirm Placement', 32, (0, 0, 0), (255, 255, 255), (1200, 800))
current_message_text = text_box('Tip: drag a green squarus piece to the top left corner to begin play!', 24, (0, 0, 0), (255, 255, 255), (20, 800))

# initialize pieces:
pieces = list()
pieces = board_data.import_pieces("pieces.txt")


# rectDist = math.dist([0, 0], [25, 25])
rectDist = 20

# set Team to 0
current_team = 0

# the last touched piece:
last_piece = pieces[0]


def check_valid(placementPiece):
    print("checking validity of pieces.")
    # checks for: overlap, corner, multiple pieces, and side touching of adjacent pieces:

    # overlap logic:
    # if the board space is occupied already, do not allow setting
    for piece_iterator in range(len(placementPiece.square_list)):
        board_index = placementPiece.square_list[piece_iterator][1]
        if board_data.occupied[board_index]:
            current_message_text.text = 'Tip: make sure that pieces do not overlap before placing them!'
            current_message_text.update()
            print(board_index)
            return False
    print("the piece does not overlap with another!")

    # corner touching check:
    valid_corner = False
    #TODO: compare order of corner iteration vs board iteration.
    for corner in placementPiece.corners:
        for board_piece in pieces:
            if not board_piece.set or board_piece.team != current_team:
                continue
            if corner not in board_piece.corners:
                continue
            else:
                # the corner of a piece on the board matches a corner for the piece.
                valid_corner = True
                break
        if corner == board_rect[0].topleft or corner == board_rect[len(board_rect) - 1].bottomright or valid_corner:
            valid_corner = True
            break
    if not valid_corner:
        current_message_text.text = 'Tip: Please place the first piece in the top left corner'
        current_message_text.update()
        return False

    # adjacency check:
    for square in placementPiece.square_list:
        if square[1] > 1 and board_data.occupied[square[1] - 1] and board_data.piece_ID[square[1] - 1] == current_team:
            current_message_text.text = 'Tip: Please place pieces corner to corner, not side to side!'
            current_message_text.update()
            return False
        elif square[1] + 1 < len(board_data.occupied) and board_data.occupied[square[1] + 1] and board_data.piece_ID[
            square[1] + 1] == current_team:
            current_message_text.text = 'Tip: Please place pieces corner to corner, not side to side!'
            current_message_text.update()
            return False
        elif square[1] > 12 and board_data.occupied[square[1] - 12] and board_data.piece_ID[
            square[1] - 12] == current_team:
            current_message_text.text = 'Tip: Please place pieces corner to corner, not side to side!'
            current_message_text.update()
            return False
        elif square[1] + 12 < len(board_data.occupied) and board_data.occupied[square[1] + 12] and board_data.piece_ID[
            square[1] + 12] == current_team:
            current_message_text.text = 'Tip: Please place pieces corner to corner, not side to side!'
            current_message_text.update()
            return False

    # this checks to make sure that the piece is in a snapped position.
    if not piece.snapped:
        return False
    current_message_text.text = 'Tip: Piece is in a valid location!'
    current_message_text.update()
    return True


def snap_pieces(piece, board_rect):
    print("snapping pieces!")
    for pieceIt in range(len(piece.rects)):
        # iterates through the pieces and snaps them to their closest board location
        piece.rects[piece.square_list[pieceIt][0]][0].x = board_rect[
            piece.square_list[pieceIt][1]].x
        piece.rects[piece.square_list[pieceIt][0]][0].y = board_rect[
            piece.square_list[pieceIt][1]].y
    test = piece.convert_to_relational(piece.rects)
    if test == piece.relational_pos:
        print("the pieces are oriented the same!")
        piece.snapped = True
        piece.corners.clear()
        piece.corners = piece.get_corners(piece.relational_pos, piece.rects)
        print("current corners: ")
        print(piece.corners)
    else:
        piece.rects = copy.deepcopy(piece.start_rects)
        print("the pieces are being reset!")
        piece.snapped = False
    return 0


def set_occupied(piece):
    for piece_iterator in range(len(piece.square_list)):
        board_index = piece.square_list[piece_iterator][1]
        board_data.occupied[board_index] = True
        board_data.piece_ID[board_index] = piece.team
    pieces[piece.ID].set = True


# main event loop
while 1:
    # if there is a current event:
    for event in pygame.event.get():
        # QUIT event
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # mouse press event
                mouse_x, mouse_y = event.pos
                for piece in pieces:
                    # iterate through the piece list
                    if piece.set:
                        continue
                    for rectIt in range(len(piece.rects)):
                        # collision check:
                        if piece.rects[rectIt][0].collidepoint(event.pos) and piece.team == current_team:
                            piece.drag = True
                            for rectIt in range(len(piece.rects)):
                                piece.rects[rectIt][1][0] = mouse_x
                                piece.rects[rectIt][1][1] = mouse_y
                if quit_text.rect.collidepoint(mouse_x, mouse_y):
                    sys.exit()
                elif set_text.rect.collidepoint(mouse_x, mouse_y):
                    if last_piece.valid:
                        set_occupied(last_piece)
                        print("piece set!")
                        current_message_text.text = 'Piece set!'
                        current_message_text.update()
                        if current_team == 0:
                            current_team = 1
                        elif current_team == 1:
                            current_team = 0

        # mouse release event
        elif event.type == pygame.MOUSEBUTTONUP:
            # left mouse button release
            if event.button == 1:
                # the board iterator, iterates through the rect pieces.
                for boardIt in range(len(board_rect)):
                    # iterate through the entire board
                    for piece in pieces:
                        # iterate through the piece list
                        if piece.set:
                            # if a piece has been set, ignore it.
                            continue
                        piece.drag = False
                        for rectIt in range(len(piece.rects)):
                            # iterates through the rectangles (squares) in the rectangle list for that piece
                            center_piece = [piece.rects[rectIt][0].centerx, piece.rects[rectIt][0].centery]
                            board_piece = [board_rect[boardIt].centerx, board_rect[boardIt].centery]
                            placement_dist = math.dist(center_piece, board_piece)
                            # bounds checking logic
                            x_valid = center_piece[0] + 25 > board_rect[0].left
                            y_valid = center_piece[1] + 25 > board_rect[1].top
                            x_valid = x_valid and center_piece[0] - 25 < board_rect[maxSquares * maxSquares - 1].right
                            y_valid = y_valid and center_piece[1] - 25 < board_rect[maxSquares * maxSquares - 1].bottom
                            if placement_dist < rectDist:
                                piece.square_list.append([piece.square_count, boardIt])
                                # piece.rects[piece.square_count][0].x = board_rect[boardIt].x
                                # piece.rects[piece.square_count][0].y = board_rect[boardIt].y
                                piece.square_count += 1
                                print("square added to square list:\t")
                                print(piece.square_list)
                        if piece.square_count == len(piece.rects):
                            # this indicates that all of the pieces have a correlatory board space.
                            print("the square count equals the rectangles")
                            piece.square_count = 0
                            snap_pieces(piece, board_rect)
                            piece.valid = check_valid(piece)
                            last_piece = copy.deepcopy(piece)
                            piece.square_list.clear()
                            break
                        else:
                            piece.valid = False
                            last_piece = copy.deepcopy(piece)
                    if piece.valid and not piece.set:
                        break
                piece.square_count = 0
                piece.square_list.clear()


        # mouse movement
        elif event.type == pygame.MOUSEMOTION:
            for piece in pieces:
                if piece.drag and piece.team == current_team:
                    mouse_x, mouse_y = event.pos
                    for rectIt in range(len(piece.rects)):
                        piece.rects[rectIt][0].x += (mouse_x - piece.rects[rectIt][1][0])
                        piece.rects[rectIt][0].y += (mouse_y - piece.rects[rectIt][1][1])
                        piece.rects[rectIt][1][0] = mouse_x
                        piece.rects[rectIt][1][1] = mouse_y

    screen.fill((40, 40, 40))
    for boardIt in range(len(board)):
        screen.blit(board[boardIt], board_rect[boardIt])
    for piece in pieces:
        for rectIt in range(len(piece.rects)):
            if piece.team == 1:
                # red
                if current_team == 1 or piece.set:
                    pygame.draw.rect(screen, (255, 0, 0), piece.rects[rectIt][0])
            elif piece.team == 0:
                # green
                if current_team == 0 or piece.set:
                    pygame.draw.rect(screen, (0, 255, 0), piece.rects[rectIt][0])

    # screen.blit(quit_text, quit_rect)
    # screen.blit(set_text, set_rect)
    quit_text.draw(screen)
    quit_text.update()
    set_text.draw(screen)
    set_text.update()
    current_message_text.draw(screen)
    current_message_text.update()

    pygame.display.flip()

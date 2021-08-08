import sys, pygame, math
from pieces import piece
from boardData import boardData
from textBox import text_box
import copy

pygame.init()

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
        # boardData insertion
        boardData.occupied.append(False)

# font and text initializations:
quit_text = text_box('Quit', 32, (0, 0, 255), (0, 255, 0), (1400, 100))
set_text = text_box('Confirm Placement', 32, (0, 0, 255), (0, 255, 0), (1200, 800))
current_message_text = text_box('Tip: drag a green squarus piece to the bottom left corner to begin play!', 24, (0, 0, 255), (0, 255, 0), (20, 800))



# initialize pieces:
pieces = list()
pieces.append(piece(0, 0, (1200, 200), [(1000, 200, 50, 50), (1000, 250, 50, 50), (1050, 250, 50, 50)]))
pieces.append(
    piece(1, 0, (1200, 200), [(1200, 200, 50, 50), (1200, 250, 50, 50), (1200, 300, 50, 50), (1250, 300, 50, 50)]))
pieces.append(
    piece(2, 1, (1400, 200), [(1400, 200, 50, 50), (1400, 250, 50, 50), (1400, 300, 50, 50), (1450, 300, 50, 50)]))
pieces.append(
    piece(3, 1, (1400, 500),
          [(1400, 500, 50, 50), (1400, 550, 50, 50), (1350, 600, 50, 50), (1400, 600, 50, 50), (1450, 600, 50, 50)]))
# rectDist = math.dist([0, 0], [25, 25])
rectDist = 20

# set Team to 0
current_team = 0

# the last touched piece:
last_piece = piece


def check_valid(placementPiece):
    print("checking validity of pieces.")
    # checks for: overlap, corner, multiple pieces, and side touching of adjacent pieces:

    # overlap logic:
    # if the board space is occupied already, do not allow setting
    for piece_iterator in range(len(placementPiece.square_list)):
        board_index = placementPiece.square_list[piece_iterator][1]
        if boardData.occupied[board_index]:
            current_message_text.text = 'Tip: make sure that pieces do not overlap before placing them!'
            current_message_text.update()
            return False
    print("the piece does not overlap with another!")
    print(placementPiece.square_list)
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
    else:
        piece.rects = copy.deepcopy(piece.start_rects)
        print("the pieces are being reset!")
    return 0


def set_occupied(piece):
    for piece_iterator in range(len(piece.square_list)):
        board_index = piece.square_list[piece_iterator][1]
        boardData.occupied[board_index] = True
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
                            if placement_dist < rectDist and x_valid and y_valid:
                                piece.square_list.append([piece.square_count, boardIt])
                                # piece.rects[piece.square_count][0].x = board_rect[boardIt].x
                                # piece.rects[piece.square_count][0].y = board_rect[boardIt].y
                                piece.square_count += 1
                        if piece.square_count == len(piece.rects):
                            # this indicates that all of the pieces have a correlatory board space.
                            print("the square count equals the rectangles")
                            print("piece.rects: ", piece.rects)
                            piece.square_count = 0
                            snap_pieces(piece, board_rect)
                            piece.valid = check_valid(piece)
                            last_piece = copy.deepcopy(piece)
                            piece.square_list.clear()
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
                pygame.draw.rect(screen, (255, 0, 0), piece.rects[rectIt][0])
            else:
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

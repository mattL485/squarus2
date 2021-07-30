import sys, pygame, math
from pieces import piece

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
board, board_rect = list(), list()
for row in range(maxSquares):
    for col in range(maxSquares):
        board.append(pygame.image.load("50-50BoardTile.png"))
        board_rect.append(board[len(board) - 1].get_rect())
        board_rect[len(board) - 1].x = col * 50
        board_rect[len(board) - 1].y = row * 50

font = pygame.font.Font('freesansbold.ttf', 32)
quit_text = font.render('Quit', True, (0, 0, 255), (0, 255, 0))
quit_rect = quit_text.get_rect()
quit_rect.center = (1400, 100)

set_text = font.render('Confirm Placement', True, (0, 0, 255), (0, 255, 0))
set_rect = set_text.get_rect()
set_rect.center = (1400, 800)

# initialize pieces:
pieces = list()
pieces.append(piece((1200, 200), 0, [(1000, 200, 50, 50), (1000, 250, 50, 50), (1050, 250, 50, 50)]))
pieces.append(
    piece((1200, 200), 0, [(1200, 200, 50, 50), (1200, 250, 50, 50), (1200, 300, 50, 50), (1250, 300, 50, 50)]))
pieces.append(
    piece((1400, 200), 1, [(1400, 200, 50, 50), (1400, 250, 50, 50), (1400, 300, 50, 50), (1450, 300, 50, 50)]))
# rectDist = math.dist([0, 0], [25, 25])
rectDist = 20

# set Team to 0
current_team = 0

# the last touched piece:
last_piece = pieces[0]


def check_valid(placementPiece, pieces):
    print("checking validity of pieces.")
    # checks for: overlap, corner, and side touching of adjacent pieces:

    print("the location of the piece is:")
    print(placementPiece.square_list)
    return True


def snap_pieces(piece, board_rect):
    for pieceIt in range(len(piece.rects)):
        # iterates through the pieces and
        piece.rects[piece.square_list[pieceIt][0]][0].x = board_rect[
            piece.square_list[pieceIt][1]].x
        piece.rects[piece.square_list[pieceIt][0]][0].y = board_rect[
            piece.square_list[pieceIt][1]].y
    piece.square_list.clear()
    last_piece = piece  # it may not be necessary to keep track of the last placed piece.
    return 0


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
                if math.dist([mouse_x, mouse_y], [quit_rect.centerx, quit_rect.centery]) < 50:
                    sys.exit()
                elif math.dist([mouse_x, mouse_y], [set_rect.centerx, set_rect.centery]) < 50:
                    last_piece.set = True
                    if current_team == 0:
                        current_team = 1
                    elif current_team == 1:
                        current_team = 0
                    print("piece set!")

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
                            # TODO: bounds checking for placement
                            center_piece = [piece.rects[rectIt][0].centerx, piece.rects[rectIt][0].centery]
                            board_piece = [board_rect[boardIt].centerx, board_rect[boardIt].centery]
                            placement_dist = math.dist(center_piece, board_piece)
                            if placement_dist <= rectDist:
                                piece.square_list.append([piece.square_count, boardIt])
                                # piece.rects[piece.square_count][0].x = board_rect[boardIt].x
                                # piece.rects[piece.square_count][0].y = board_rect[boardIt].y
                                piece.square_count += 1
                        if piece.square_count == len(piece.rects):
                            # this indicates that all of the pieces have a correlatory board space.
                            print("the square count equals the rectangles")
                            piece.square_count = 0
                            snap_pieces(piece, board_rect)
                            if check_valid(piece, pieces):
                                piece.set = True



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
    screen.blit(quit_text, quit_rect)
    screen.blit(set_text, set_rect)
    pygame.display.flip()

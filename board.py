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


rectangle = piece((1000, 200), 0, [(1000, 200, 50, 50), (1000, 250, 50, 50), (1050, 250, 50, 50)])
rectDist = math.dist([0, 0], [25, 25])
rectangle_dragging = False

# main event loop
while 1:
    # if there is a current event:
    for event in pygame.event.get():
        # QUIT event
        if event.type == pygame.QUIT:
            sys.exit()
        # mouse press event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for rectIt in range(len(rectangle.rects)):
                    # collision check:
                    if rectangle.rects[rectIt][0].collidepoint(event.pos):
                        rectangle_dragging = True
                        mouse_x, mouse_y = event.pos
                        for rectIt in range(len(rectangle.rects)):
                            rectangle.rects[rectIt][1][0] = mouse_x
                            rectangle.rects[rectIt][1][1] = mouse_y

        # mouse release event
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_dragging = False
                for boardIt in range(len(board_rect)):
                    for rectIt in range(len(rectangle.rects)):
                        if math.dist([rectangle.rects[rectIt][0].centerx, rectangle.rects[rectIt][0].centery],
                                     [board_rect[boardIt].centerx, board_rect[boardIt].centery]) <= rectDist:
                            rectangle.rects[rectIt][0].x = board_rect[boardIt].x
                            rectangle.rects[rectIt][0].y = board_rect[boardIt].y

        # moues 
        elif event.type == pygame.MOUSEMOTION:
            if rectangle_dragging:
                mouse_x, mouse_y = event.pos
                for rectIt in range(len(rectangle.rects)):
                    rectangle.rects[rectIt][0].x += (mouse_x - rectangle.rects[rectIt][1][0])
                    rectangle.rects[rectIt][0].y += (mouse_y - rectangle.rects[rectIt][1][1])
                    rectangle.rects[rectIt][1][0] = mouse_x
                    rectangle.rects[rectIt][1][1] = mouse_y


    screen.fill((40, 40, 40))
    for boardIt in range(len(board)):
        screen.blit(board[boardIt], board_rect[boardIt])
    for rectIt in range(len(rectangle.rects)):
        pygame.draw.rect(screen, (255, 0, 0), rectangle.rects[rectIt][0])
    pygame.display.flip()

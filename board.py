import sys, pygame, math

pygame.init()

print(pygame.display.Info())

# display initializations
# TODO: extract display info and scale
size = width, height = 1920, 1080
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

rectangle = pygame.rect.Rect(1000, 200, 40, 40)
rectDist = math.dist([0, 0], [25, 25])
rectangle_dragging = False

# main event loop
while 1:
    # break event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.collidepoint(event.pos):
                    rectangle_dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_dragging = False
                for boardIt in range(len(board_rect)):
                    if math.dist([rectangle.centerx, rectangle.centery],
                                 [board_rect[boardIt].centerx, board_rect[boardIt].centery]) <= rectDist:
                        rectangle.x = board_rect[boardIt].x + 5
                        rectangle.y = board_rect[boardIt].y + 5


        elif event.type == pygame.MOUSEMOTION:
            if rectangle_dragging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y

    screen.fill((40, 40, 40))
    for boardIt in range(len(board)):
        screen.blit(board[boardIt], board_rect[boardIt])
    pygame.draw.rect(screen, (255, 0, 0), rectangle)
    pygame.display.flip()

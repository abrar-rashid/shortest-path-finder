import pygame
from node import Node
import colours
from a_star import a_star_algorithm
from dijkstra import dijkstra_algorithm

# Initialises window
LENGTH = 750
WIN = pygame.display.set_mode((LENGTH, LENGTH))
pygame.display.set_caption("Menu")


# Initialises grid as a 2d array of nodes
def init_grid(no_rows, length):
    grid = []
    unitLength = length // no_rows
    for i in range(no_rows):
        grid.append([])
        for j in range(no_rows):
            grid[i].append(Node(i, j, unitLength, no_rows))
    return grid


# Produces the grid on the screen
def draw_grid(win, no_rows, length):
    unitLength = length // no_rows
    for i in range(no_rows):
        pygame.draw.line(win, colours.GREY, (0, i * unitLength), (length, i * unitLength))
        for j in range(no_rows):
            pygame.draw.line(win, colours.GREY, (j * unitLength, 0), (j * unitLength, length))


# Iterates through nodes in the 2d array and draws each node on the game window
# and then updates the screen to the current game
def draw(win, grid, no_rows, length):
    win.fill(colours.WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, no_rows, length)
    pygame.display.update()


# Stores the user's click position as a tuple. The row and col are used instead of x and y because of the node size
def click_position(pos, no_rows, length):
    unitLength = length // no_rows
    y, x = pos
    row = y // unitLength
    col = x // unitLength
    return row, col


# To run
def main(win, length):
    pygame.init()
    font_large = pygame.font.Font('RobotoRegular-3m4L.ttf', 36)
    font_medium = pygame.font.Font('RobotoRegular-3m4L.ttf', 24)
    font_small = pygame.font.Font('RobotoRegular-3m4L.ttf', 16)

    text_line1 = font_large.render('Welcome to the shortest path visualiser!', True, colours.BLACK, colours.WHITE)
    text_line1_rect = text_line1.get_rect()
    text_line1_rect.center = LENGTH // 2, LENGTH // 4

    text_line2 = font_medium.render('Press a for the A* algorithm', True, colours.BLACK, colours.WHITE)
    text_line2_rect = text_line2.get_rect()
    text_line2_rect.center = LENGTH // 2, LENGTH // 4 + LENGTH // 8

    text_line3 = font_medium.render('Press c for the Dijkstra algorithm', True, colours.BLACK, colours.WHITE)
    text_line3_rect = text_line3.get_rect()
    text_line3_rect.center = LENGTH // 2, LENGTH // 4 + LENGTH // 8 + LENGTH // 16

    text_line4 = font_small.render('Instructions:', True, colours.BLACK, colours.WHITE)
    text_line4_rect = text_line4.get_rect()
    text_line4_rect.center = LENGTH // 2, 3 * LENGTH // 4

    text_line5 = font_small.render('1. Click a square as the start position and another one as the end position',
                                   True, colours.BLACK, colours.WHITE)
    text_line5_rect = text_line5.get_rect()
    text_line5_rect.center = LENGTH // 2, 3 * LENGTH // 4 + LENGTH // 32

    text_line6 = font_small.render('2. Click or hold with left mouse to add walls, and right mouse to remove walls or '
                                   'remove start or end', True, colours.BLACK, colours.WHITE)
    text_line6_rect = text_line6.get_rect()
    text_line6_rect.center = LENGTH // 2, 3 * LENGTH // 4 + LENGTH // 16

    text_line7 = font_small.render('3. Press space to start the pathfinding algorithm', True, colours.BLACK,
                                   colours.WHITE)
    text_line7_rect = text_line7.get_rect()
    text_line7_rect.center = LENGTH // 2, 3 * LENGTH // 4 + LENGTH // 16 + LENGTH // 32

    text_line8 = font_small.render('Press c to reset the grid', True, colours.BLACK, colours.WHITE)
    text_line8_rect = text_line8.get_rect()
    text_line8_rect.center = LENGTH // 2, 3 * LENGTH // 4 + LENGTH // 16 + LENGTH // 8

    algorithm = None
    menu = True
    while menu:
        win.fill(colours.WHITE)
        win.blit(text_line1, text_line1_rect)
        win.blit(text_line2, text_line2_rect)
        win.blit(text_line3, text_line3_rect)
        win.blit(text_line4, text_line4_rect)
        win.blit(text_line5, text_line5_rect)
        win.blit(text_line6, text_line6_rect)
        win.blit(text_line7, text_line7_rect)
        win.blit(text_line8, text_line8_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    algorithm = 1  # A* algorithm
                elif event.key == pygame.K_d:
                    algorithm = 2  # Dijkstra algorithm
                menu = False
            pygame.display.update()

    if algorithm is None:
        pygame.quit()
        print("Invalid letter pressed, please press a or c")
    # The greater the number of rows, the smaller the pixel size.
    no_rows = 50
    grid = init_grid(no_rows, length)
    start, end = None, None  # To be activated by the user
    running = True
    pygame.display.set_caption("Shortest Path Visualiser")
    while running:
        draw(win, grid, no_rows, length)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # Left mouse click
                pos = pygame.mouse.get_pos()
                row, col = click_position(pos, no_rows, length)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.make_wall()
            elif pygame.mouse.get_pressed()[2]:  # Right mouse click
                pos = pygame.mouse.get_pos()
                row, col = click_position(pos, no_rows, length)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:  # Starts pathfinding algorithm upon pressing space
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)  # Checks around each node for non-wall nodes
                    if algorithm == 1:
                        a_star_algorithm(lambda: draw(win, grid, no_rows, length), grid, start, end)
                    else:
                        dijkstra_algorithm(lambda: draw(win, grid, no_rows, length), grid, start, end)

                if event.key == pygame.K_c:  # Resets grid upon pressing c
                    start = None
                    end = None
                    grid = init_grid(no_rows, length)
    pygame.quit()
    quit()


main(WIN, LENGTH)

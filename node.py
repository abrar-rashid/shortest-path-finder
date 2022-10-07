import pygame
import colours


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # Finds x and y positions relative to the width of the node block
        self.x = row * width
        self.y = col * width
        # All nodes start with the default colour of white
        self.colour = colours.WHITE
        self.width = width
        self.total_rows = total_rows
        self.neighbours = []

    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.colour == colours.RED

    def is_open(self):
        return self.colour == colours.GREEN

    def is_wall(self):
        return self.colour == colours.BLACK

    def is_start(self):
        return self.colour == colours.YELLOW

    def is_end(self):
        return self.colour == colours.TURQUOISE

    def reset(self):
        self.colour = colours.WHITE

    def make_closed(self):
        self.colour = colours.RED

    def make_open(self):
        self.colour = colours.ORANGE

    def make_wall(self):
        self.colour = colours.BLACK

    def make_start(self):
        self.colour = colours.TURQUOISE

    def make_end(self):
        self.colour = colours.PURPLE

    def make_path(self):
        self.colour = colours.YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    # Neighbours are 1 node away, and cannot be a wall
    def update_neighbours(self, grid):
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

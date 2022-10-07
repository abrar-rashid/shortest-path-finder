import pygame
from queue import PriorityQueue


# Heuristic function which uses the Manhattan Distance Metric
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


#
def backtrack(prev_vertex, curr, draw):
    while curr in prev_vertex:
        curr = prev_vertex[curr]
        curr.make_path()
        draw()
    curr.make_start()


# A* algorithm using priority queues
def a_star_algorithm(draw, grid, start, end):
    # Sets each node's distance from start to infinity
    g_values = {node: float("inf") for row in grid for node in row}
    g_values[start] = 0
    # Sets each node's heuristic distance to the end to infinity:
    f_values = {node: float("inf") for row in grid for node in row}
    f_values[start] = heuristic(start.get_position(), end.get_position())
    prev_vertex = {}  # Dict/map storing traversed nodes and their previous node
    step = 0  # The nth new node reached
    to_visit = PriorityQueue()
    to_visit.put((0, step, start))
    nodes_in_queue = {start}

    while not to_visit.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = to_visit.get()[2]  # Polls the head of the queue
        nodes_in_queue.remove(curr)

        if curr == end:  # When the end is reached, the path must be traced on the nodes
            backtrack(prev_vertex, end, draw)
            end.make_end()
            return True

        for neighbour in curr.neighbours:
            neighbour_temp_g_value = g_values[curr] + 1  # Arc lengths are 1 for nodes
            # If this new distance/g_value is shorter than the current, store this new distance instead
            if neighbour_temp_g_value < g_values[neighbour]:
                prev_vertex[neighbour] = curr
                g_values[neighbour] = neighbour_temp_g_value
                # Update the f_values
                f_values[neighbour] = neighbour_temp_g_value + heuristic(neighbour.get_position(), end.get_position())
                if neighbour not in nodes_in_queue:
                    step += 1
                    to_visit.put((f_values[neighbour], step, neighbour))
                    nodes_in_queue.add(neighbour)
                    neighbour.make_open()
        draw()
        if curr != start:
            curr.make_closed()
    return False

import pygame
from queue import PriorityQueue


def backtrack(prev_vertex, curr, draw):
    while curr in prev_vertex:
        curr = prev_vertex[curr]
        curr.make_path()
        draw()
    curr.make_start()


# Dijkstra's algorithm using priority queues
def dijkstra_algorithm(draw, grid, start, end):
    # Check comments for A* algorithm (very similar, can be applied here)
    distances = {node: float("inf") for row in grid for node in row}
    distances[start] = 0
    prev_vertex = {}
    step = 0
    toVisit = PriorityQueue()
    toVisit.put((0, step, start))
    nodes_in_queue = {start}

    while not toVisit.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = toVisit.get()[2]
        nodes_in_queue.remove(curr)

        if curr == end:
            backtrack(prev_vertex, end, draw)
            end.make_end()
            return True

        for neighbour in curr.neighbours:
            neighbour_temp_g_score = distances[curr] + 1
            if neighbour_temp_g_score < distances[neighbour]:
                prev_vertex[neighbour] = curr
                distances[neighbour] = neighbour_temp_g_score
                if neighbour not in nodes_in_queue:
                    step += 1
                    toVisit.put((neighbour_temp_g_score, step, neighbour))
                    nodes_in_queue.add(neighbour)
                    neighbour.make_open()
        draw()
        if curr != start:
            curr.make_closed()
    return False

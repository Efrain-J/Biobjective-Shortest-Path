import heapq
from src.utiles import *


def astar(start, goal, graph, minimize_pollution=False):
    open_list = [(0, start)]
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, graph)

    g_2 = {node: float('inf') for node in graph}
    g_2[start] = 0


    while open_list:
        current_f, current = heapq.heappop(open_list)
        if current == goal:
            path = reconstruct_path(came_from, current)

            if minimize_pollution == True:
                return path,g_2[current],  g_score[current]
            else:
                return path, g_score[current], g_2[current]

        if minimize_pollution == True:
            for neighbor, (resource, distance) in graph[current].items():
                tentative_g_score = g_score[current] + distance
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, graph)

                    g_2[neighbor] = g_2[current] + resource
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        else:
            for neighbor, (distance, resource) in graph[current].items():
                tentative_g_score = g_score[current] + distance
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, graph)

                    g_2[neighbor] = g_2[current] + resource
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None, None, None

def heuristic(node, graph):
    # Heurística: Distancia desde el nodo más cercano al nodo final
    min_distance = float('inf')
    for neighbor, (distance, _) in graph[node].items():
        if distance < min_distance:
            min_distance = distance
    return min_distance

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def main_astar(start_node, end_node, graph_filepath, minimize_pollution):
    graph = build_graph(graph_filepath)
    path, distance, pollution = astar(start_node, end_node, graph, minimize_pollution)
    return path, distance, pollution
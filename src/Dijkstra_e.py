import heapq
from src.utiles import *


def dijkstra_epsilon(start, end, graph, max_resource):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, [start], 0)]  # La cola de prioridad ahora contendrá tuplas de (distancia acumulada, ruta actual)

    while pq:
        current_distance, current_path, current_polution = heapq.heappop(pq)
        current_node = current_path[-1]  # El último nodo en la ruta es el nodo actual

        if current_polution > max_resource: # Salta si el limite del recurso es excedido
            continue

        if current_node == end:
            return current_path, current_distance, current_polution  # Devuelve la ruta y la distancia asociada

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            cost1 = weight[0]
            cost2 = weight[1]
            distance_to_neighbor = current_distance + cost1
            polution_to_neighbor = current_polution + cost2
            if distance_to_neighbor < distances[neighbor]:
                distances[neighbor] = distance_to_neighbor
                new_path = current_path + [neighbor]  # Añadir el vecino a la ruta actual
                heapq.heappush(pq, (distance_to_neighbor, new_path, polution_to_neighbor))

    return None, None, None  # No se encontró una ruta desde el nodo de inicio al nodo de destino

def main_dijkstra_epsilon(start_node, end_node, graph_filepath, max_resource):
    graph = build_graph(graph_filepath)
    path, distance, pollution = dijkstra_epsilon(start_node, end_node, graph, max_resource)
    return path, distance, pollution

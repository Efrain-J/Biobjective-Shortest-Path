from src.utiles import *

def dijkstra(start, end, graph, minimize_pollution=False):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, [start], 0)]  # La cola de prioridad ahora contendrá triplas de (distancia acumulada, ruta actual, distancia secundaria acum)

    while pq:
        current_distance, current_path, current_secondary_distance = heapq.heappop(pq)
        current_node = current_path[-1]  # El último nodo en la ruta es el nodo actual

        if current_node == end:
            if minimize_pollution: # Para siempre retorne en el orden: camino, distancia, polucion
                return current_path, current_secondary_distance, current_distance
            return current_path, current_distance, current_secondary_distance  # Devuelve la ruta y la distancia asociada

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            if minimize_pollution:
                cost = weight[1]
                secondary = weight[0]
            else:
                cost = weight[0]
                secondary = weight[1]
            distance_to_neighbor = current_distance + cost
            secondary_distance_to_n = current_secondary_distance + secondary
            if distance_to_neighbor < distances[neighbor]:
                distances[neighbor] = distance_to_neighbor
                new_path = current_path + [neighbor]  # Añadir el vecino a la ruta actual
                heapq.heappush(pq, (distance_to_neighbor, new_path, secondary_distance_to_n))

    return None, None, None  # No se encontró una ruta desde el nodo de inicio al nodo de destino

def main_dijkstra(start_node, end_node, graph_filepath, minimize_pollution):
    graph = build_graph(graph_filepath)
    path, distance, pollution = dijkstra(start_node, end_node, graph, minimize_pollution)
    return path, distance, pollution
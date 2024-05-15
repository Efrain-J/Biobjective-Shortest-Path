import heapq


# Para leer excel_med_pyc.txt; retorna un diccionario
def build_graph(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            columnas = line.split(";")
            start = columnas[0]
            end = columnas[1]
            distance = float(columnas[2])
            pollution = float(columnas[3])
            if start not in graph:
                graph[start] = {}
            if end not in graph:
                graph[end] = {}
            
            graph[start][end] = (distance, pollution)
            graph[end][start] = (distance, pollution)

    return graph

# Para los grafos anteriores (NY, COL, Boa-pdf, etc)
def build_graph_old(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            columnas = line.strip().split()
            start = columnas[0]
            end = columnas[1]
            distance = float(columnas[2])
            pollution = float(columnas[3])
            if start not in graph:
                graph[start] = {}
            if end not in graph:
                graph[end] = {}
            
            graph[start][end] = (distance, pollution)
            graph[end][start] = (distance, pollution)

    return graph

# Encontrar las distancias desde el nodo final hacia el resto de nodos
def dijkstra_all(adj_list, start, minimize_pollution=False):
    distances = {node: float('inf') for node in adj_list}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in adj_list[current_node].items():
            if minimize_pollution:
                cost = weight[1]
            else:
                cost = weight[0]
            distance = current_distance + cost

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances
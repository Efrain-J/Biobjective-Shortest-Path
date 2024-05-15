import pandas as pd
import heapq
from src.utiles import *


## Dataframe para los valores heuristicos de los nodos:
# Sus columnas son: h1, h2, g2 minimo
# El indice del df es el id del nodo
def create_df(graph, end_node):
    resultado_distancia = dijkstra_all(graph, end_node, minimize_pollution=False)
    resultado_polucion = dijkstra_all(graph, end_node, minimize_pollution=True)
    df = pd.DataFrame.from_dict(resultado_distancia, orient='index', dtype=None, columns=['h1'])
    df['h2'] = df.index.map(resultado_polucion)
    df['g2_min']= float('inf')
    return df

# Los nodos dentro de boa son listas que contienen los siguientes datos
#               g1 g2 f1 f2 Camino
# [id del nodo, 0, 0, 0, 0, []]
def boa(graph, start, goal, df):
    contador = 0 # De las soluciones
    start_node = [start, 0, 0, 0, 0, []]
    start_node[3] = df['h1'][start_node[0]]
    start_node[4] = df['h2'][start_node[0]]
    sols = []
    open = []
    heapq.heappush(open, (start_node[3], start_node[4], start_node))
    while open:
        _, _, x = heapq.heappop(open)
        if x[2] >= df['g2_min'][x[0]] or x[4] >= df['g2_min'][goal]:
            continue

        df.loc[x[0], 'g2_min'] = x[2]
        if x[0] == goal:
            x[5].append(x[0])
            sols.append(x)
            # Para que se impriman las soluciones cuando se encuentran
            #print(f"g1: {sols[contador][1]}, g2: {sols[contador][2]}, sol #{contador+1}")
            contador = contador + 1
            if df['g2_min'][goal] > x[2]:
                df.loc[goal, 'g2_min'] = x[2]
            continue

        for neighbor, weight in graph[x[0]].items():
            cost1 = weight[0]
            cost2 = weight[1]
            y = [neighbor, 0, 0, 0, 0, x[5].copy()]
            y[1] = x[1] + cost1 #g1 = g1 (de x) + coste1 del arco
            y[2] = x[2] + cost2 #g2 = g2 (de x) + coste2 del arco
            y[5].append(x[0]) #Padre de y es x

            if y[2] >= df['g2_min'][y[0]] or y[3] >= df['g2_min'][goal]:
                continue

            y[3] = y[1] + df['h1'][y[0]] #f1 = g1 + h1
            y[4] = y[2] + df['h2'][y[0]] #f2 = g2 + h2
            heapq.heappush(open, (y[3],y[4],y))
    return sols

### Funciona igual que boa; la unica diferencia es que guarda
# las soluciones que encuentre en un .csv
def boa_write(graph, start, goal, df, output_filepath):
    file = open(output_filepath,"w")
    contador = 0 # De las soluciones
    start_node = [start, 0, 0, 0, 0, []]
    start_node[3] = df['h1'][start_node[0]]
    start_node[4] = df['h2'][start_node[0]]
    sols = []
    open_ = []
    heapq.heappush(open_, (start_node[3], start_node[4], start_node))
    while open_:
        _, _, x = heapq.heappop(open_)
        if x[2] >= df['g2_min'][x[0]] or x[4] >= df['g2_min'][goal]:
            continue

        df.loc[x[0], 'g2_min'] = x[2]
        if x[0] == goal:
            x[5].append(x[0])
            sols.append(x)
            file.write(f"{sols[contador][1]},{sols[contador][2]}\n")
            # Para que se impriman las soluciones cuando se encuentran
            #print(f"g1: {sols[contador][1]}, g2: {sols[contador][2]}, sol #{contador+1}")
            contador = contador + 1
            if df['g2_min'][goal] > x[2]:
                df.loc[goal, 'g2_min'] = x[2]
            continue

        for neighbor, weight in graph[x[0]].items():
            cost1 = weight[0]
            cost2 = weight[1]
            y = [neighbor, 0, 0, 0, 0, x[5].copy()]
            y[1] = x[1] + cost1 #g1 = g1 (de x) + coste1 del arco
            y[2] = x[2] + cost2 #g2 = g2 (de x) + coste2 del arco
            y[5].append(x[0]) #Padre de y es x

            if y[2] >= df['g2_min'][y[0]] or y[3] >= df['g2_min'][goal]:
                continue

            y[3] = y[1] + df['h1'][y[0]] #f1 = g1 + h1
            y[4] = y[2] + df['h2'][y[0]] #f2 = g2 + h2
            heapq.heappush(open_, (y[3],y[4],y))
    return sols

def main_boa(start_node, goal_node, graph_filepath, \
             save_csv=False, output_filepath=None):
    graph = build_graph(graph_filepath)
    df = create_df(graph, goal_node)
    if save_csv:
        sols = boa_write(graph, start_node, goal_node, df, output_filepath)
    else:
        sols = boa(graph, start_node, goal_node, df)
    return sols
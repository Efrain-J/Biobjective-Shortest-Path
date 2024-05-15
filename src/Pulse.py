import pandas as pd
from src.utiles import *


df_resource = None
df_cost = None
memory = {}
min_cost = float('inf')
max_eps = None
graph = {}
end_node = None
best_P = [[],0,0] # Mejor camino [camino (lista de nodos), coste 1, coste 2]


def create_df_cost(end_node):
    global df_cost
    global graph
    resultado_costo = dijkstra_all(graph, end_node, minimize_pollution=False)
    df_cost = pd.DataFrame.from_dict(resultado_costo, orient='index', dtype=None, columns=['Cost'])

def create_df_resource(end_node):
    global df_resource
    global graph
    resultado_recurso = dijkstra_all(graph, end_node, minimize_pollution=True)
    df_resource = pd.DataFrame.from_dict(resultado_recurso, orient='index', dtype=None, columns=['Resource'])

def create_memory():
    global memory
    global graph
    memory = {key: [(float('inf'),float('inf'))] for key in graph}

def clean_memory(tuple_list, max_mem):
    to_be_removed = []
    if len(tuple_list) >= max_mem:
        min_first = min(tuple_list, key=lambda x: x[0])[0]
        min_second = min(tuple_list, key=lambda x: x[1])[1]
        for i, old_tuple in enumerate(tuple_list):
            if old_tuple[0] > min_first or old_tuple[1] > min_second:
                to_be_removed.append(i)
        for idx in reversed(to_be_removed):
            del tuple_list[idx]


def dominance_check(new_tuple, tuple_list):
    dominated = False
    to_be_removed = []
    
    for i, old_tuple in enumerate(tuple_list):
        if (new_tuple[0] >= old_tuple[0] and new_tuple[1] >= old_tuple[1]):
            dominated = True
            break
        elif (new_tuple[0] <= old_tuple[0] and new_tuple[1] <= old_tuple[1]) and \
             (new_tuple[0] < old_tuple[0] or new_tuple[1] < old_tuple[1]):
            # If the new tuple is dominated by an existing tuple, don't add it
            to_be_removed.append(i)
    for idx in reversed(to_be_removed):
        del tuple_list[idx]
    # If the new tuple is not dominated, add it to the list
    if not dominated:
        tuple_list.append(new_tuple)
    return dominated


def main_pulse(start_node, target_node, graph_filepath, max_resource):
    global max_eps, graph, end_node, best_P
    end_node = target_node
    graph =  build_graph(graph_filepath)
    max_eps = max_resource
    create_memory()
    create_df_resource(end_node)
    create_df_cost(end_node)
    P = []
    c_0 = 0
    t_0 = 0
    pulse(start_node, c_0, t_0, P)
    #print(f"Distance: {best_P[1]} Pollution: {best_P[2]}")
    return best_P[0], best_P[1], best_P[2] # Path, distance, pollution


def pulse(node, c, t, P):
    global max_eps, df_resource, df_cost, graph
    global min_cost, end_node, best_P

    if node in P: 
        return
    if dominance_check((c,t), memory[node]) == False:
        #clean_memory(memory[node],30) # Revisar
        if t + df_resource['Resource'][node] <= max_eps:
            if c + df_cost['Cost'][node] < min_cost:
                if node == end_node:
                    min_cost = c + df_cost['Cost'][node]
                    P2 = P.copy()
                    P2.append(node)
                    best_P = [P2, min_cost, t]
                    #print(f"Distancia: {best_P[1]} Polucion: {best_P[2]}")
                    return
                
                P2 = P.copy()
                P2.append(node)
                for neighbor, weight in graph[node].items():
                    cost1 = weight[0]
                    cost2 = weight[1]
                    c_2 = c + cost1
                    t_2 = t + cost2
                    pulse(neighbor, c_2, t_2, P2)
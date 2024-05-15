from src.Boa import main_boa
from src.Dijkstra import main_dijkstra
from src.AStar import main_astar
from src.D_e import main_dijkstra_epsilon
from src.A_e import main_astar_epsilon
from src.Pulse import main_pulse
from src.nsga_11 import main_nsga, write_csv
import time

start_node = None
end_node = None
graph_filepath = None

def main(algoritmo, save_csv=False, output_filepath=None, minimize_pollution=False, \
              max_resource=None):
    
    algoritmo = algoritmo.upper().strip()
    print(f"\n----{algoritmo}----")

    if algoritmo == 'BOA':
        sols, elapsed_time =  call_boa(save_csv, output_filepath)
        print(f"It took: {elapsed_time} seconds")
        print(f"Number of solutions found: {len(sols)}")
        print(f"First solution: g1: {sols[0][1]}, g2: {sols[0][2]}")
        print(f"Last solution: g1: {sols[-1][1]}, g2: {sols[-1][2]}")
    
    elif algoritmo == 'NGSA':
        mapped_paths, elapsed_time =  call_nsga(save_csv, output_filepath)
        print(f"It took: {elapsed_time} seconds")
        print(f"Number of solutions found: {len(mapped_paths)}")
        print(f"First solution: Distance: {mapped_paths[0]['objective'][0]}, Pollution: {mapped_paths[0]['objective'][1]}")
        print(f"Last solution: Distance: {mapped_paths[-1]['objective'][0]}, Pollution: {mapped_paths[-1]['objective'][1]}")

    elif algoritmo == 'DIJKSTRA':
        if minimize_pollution: print("Minimizing Pollution")
        else: print("Minimizing Distace")
        path, distance, pollution, elapsed_time =  call_dijkstra(minimize_pollution)
        print(f"It took: {elapsed_time} seconds")
        if path:
            print(f"First Cost: {distance} ; Second Cost: {pollution}")
        else:
            print("No path found.")

    elif algoritmo == 'ASTAR':
        if minimize_pollution: print("Minimizing Pollution")
        else: print("Minimizing Distace")
        path, distance, pollution, elapsed_time =  call_astar(minimize_pollution)
        print(f"It took: {elapsed_time} seconds")
        if path:
            print(f"First Cost: {distance} ; Second Cost: {pollution}")
        else:
            print("No path found.")

    elif algoritmo == 'DIJKSTRA-EPSILON':
        path, distance, pollution, elapsed_time =  call_dijkstra_epsilon(max_resource)
        print(f"It took: {elapsed_time} seconds")
        if path:
            print(f"First Cost: {distance} ; Second Cost: {pollution}")
        else:
            print(f"No path found within {max_resource} resource.")

    elif algoritmo == 'ASTAR-EPSILON':
        path, distance, pollution, elapsed_time =  call_astar_epsilon(max_resource)
        print(f"It took: {elapsed_time} seconds")
        if path:
            print(f"First Cost: {distance} ; Second Cost: {pollution}")
        else:
            print(f"No path found within {max_resource} resource.")

    elif algoritmo == 'PULSE':
        path, distance, pollution, elapsed_time = call_pulse(max_resource)
        print(f"It took: {elapsed_time} seconds")
        if path:
            print(f"First Cost: {distance} ; Second Cost: {pollution}")
        else:
            print("No path found.")

    else:
        print("Invalid algorithm")


def call_boa(save_csv=False, output_filepath=None):
    global start_node, end_node, graph_filepath
    start_time = time.time()
    sols = main_boa(start_node, end_node, graph_filepath, save_csv, output_filepath)
    elapsed_time = time.time() - start_time
    return sols, elapsed_time

def call_dijkstra(minimize_pollution):
    global start_node, end_node, graph_filepath
    start_time = time.time()
    path, distance, pollution = main_dijkstra(start_node, end_node, graph_filepath, minimize_pollution)
    elapsed_time = time.time() - start_time
    return path, distance, pollution, elapsed_time

def call_astar(minimize_pollution):
    global start_node, end_node, graph_filepath
    start_time = time.time()
    path, distance, pollution = main_astar(start_node, end_node, graph_filepath, minimize_pollution)
    elapsed_time = time.time() - start_time
    return path, distance, pollution, elapsed_time

def call_dijkstra_epsilon(max_resource):
    global start_node, end_node, graph_filepath
    start_time = time.time()
    path, distance, pollution = main_dijkstra_epsilon(start_node, end_node, graph_filepath, max_resource)
    elapsed_time = time.time() - start_time
    return path, distance, pollution, elapsed_time

def call_astar_epsilon(max_resource):
    global start_node, end_node, graph_filepath
    start_time = time.time()
    path, distance, pollution = main_astar_epsilon(start_node, end_node, graph_filepath, max_resource)
    elapsed_time = time.time() - start_time
    return path, distance, pollution, elapsed_time

def call_pulse(max_resource):
    global start_node, end_node, graph_filepath
    start_time = time.time()
    path, distance, pollution = main_pulse(start_node, end_node, graph_filepath, max_resource)
    elapsed_time = time.time() - start_time
    return path, distance, pollution, elapsed_time

def call_nsga(save_csv=False, output_filepath=None):
    global start_node, end_node, graph_filepath
    start_time = time.time()
    mapped_paths = main_nsga(start_node, end_node, graph_filepath)
    elapsed_time = time.time() - start_time
    if save_csv: write_csv(output_filepath, mapped_paths)
    return mapped_paths, elapsed_time



if __name__ == "__main__":
    graph_filepath = "excel_med_pyc.txt" 
    output_file_boa = "out_boa.csv"
    output_file_gen = "out_gen.csv"

    """
    # Caso 1
    start_node = "(-75.6052191, 6.2318821)" 
    end_node = "(-75.589614, 6.2384034)"

    lista_algo = ["BOA","NGSA","Dijkstra","Astar","DIJKSTRA-EPSILON","Astar-EPSILON","Pulse"]
    max_res = 30
    for algo in lista_algo:
        if algo.upper() == 'DIJKSTRA' or algo.upper() == 'ASTAR':
            main(algo, minimize_pollution=False)
            main(algo, minimize_pollution=True)
        elif algo.upper() == 'BOA':
            main(algo, save_csv=True, output_filepath=output_file_boa)
        elif algo.upper() == 'NGSA':
            main(algo, save_csv=True, output_filepath=output_file_gen)
        else: 
            main(algo, max_resource=max_res)
    """ 

    # Caso 2
    start_node = "(-75.5956039, 6.2453916)"
    end_node = "(-75.5636164, 6.2002022)" 
    lista_algo = ["BOA","Dijkstra","Astar","DIJKSTRA-EPSILON","Astar-EPSILON","Pulse"]
    max_res = 50
    for algo in lista_algo:
        if algo.upper() == 'DIJKSTRA' or algo.upper() == 'ASTAR':
            main(algo, minimize_pollution=False)
            main(algo, minimize_pollution=True)
        else: 
            main(algo, save_csv=True, output_filepath=output_file_boa, max_resource=max_res)        
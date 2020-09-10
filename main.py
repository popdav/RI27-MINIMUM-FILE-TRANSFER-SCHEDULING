from MockNetwork import Network
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from itertools import product
import time


def main():
    file_name = "data100.json"
    n = Network()
    # n.init_network(100, 1, 1)
    # n.save_to_json(file_name)
    n.load_from_json("data.json")
    # n.calc_time()
    # print(n.server_list)
    # G = nx.Graph()
    #
    # for server in n:
    #     G.add_node(server.get_id(), pos=(server.longitude, server.latitude))
    #
    # G.add_edges_from((a, b) for a, b in product(range(10), range(10)) if a != b)
    #
    # nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=400)
    # plt.show()
    print(n.calc_time())
    start_brute = time.time()
    n.start_network_brute_force()
    end_brute = time.time()
    print(f'Brute force duration : {end_brute - start_brute}\n')

    n1 = Network()
    n1.load_from_json(file_name)

    start_gen1 = time.time()
    n1.start_genetic_v2()
    end_gen1 = time.time()

    start_gen_brute1 = time.time()
    n1.start_network_brute_force()
    end_gen_brute1 = time.time()

    n2 = Network()
    n2.load_from_json(file_name)

    start_gen2 = time.time()
    n2.start_genetic_v2()
    end_gen2 = time.time()

    start_gen_brute2 = time.time()
    n2.start_network_brute_force()
    end_gen_brute2 = time.time()

    print(f'Gentic algotithm_v2 duration: {end_gen2 - start_gen2}\n')
    print(f'Gentic algotithm_v2 and Demand Protocol: {end_gen_brute2 - start_gen_brute2}\n')

    print(f'Gentic algotithm_v1: {end_gen1 - start_gen1}\n')
    print(f'Gentic algotithm_v1 and Demand Protocol: {end_gen_brute1 - start_gen_brute1}\n')

    print(f'Demand Protocol: {end_brute - start_brute}\n')


if __name__ == '__main__':
    main()

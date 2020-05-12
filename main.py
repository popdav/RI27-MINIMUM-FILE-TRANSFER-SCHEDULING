from MockNetwork import Network
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from itertools import product
import time


def main():
    n = Network()
    n.init_network()

    # G = nx.Graph()
    #
    # for server in n:
    #     G.add_node(server.get_id(), pos=(server.longitude, server.latitude))
    #
    # G.add_edges_from((a, b) for a, b in product(range(10), range(10)) if a != b)
    #
    # nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=400)
    # plt.show()
    start_brute = time.time()
    n.start_network_brute_force()
    end_brute = time.time()
    for server in n:
        server.copy_queue_to_original()

    start_gen = time.time()
    n.start_genetic_algorithm()
    n.start_network_brute_force()
    end_gen = time.time()

    print(f'Brute force duration : {end_brute - start_brute}\n')
    print(f'Gen duration : {end_gen - start_gen}')


if __name__ == '__main__':
    main()

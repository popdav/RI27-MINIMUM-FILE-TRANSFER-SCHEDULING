from MockNetwork import Network
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from itertools import product
import time


def main():
    n = Network()
    n.init_network(100, 1, 1)
    n.save_to_json("data.json")
    # n.load_from_json("data.json")
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
    n1.load_from_json("data.json")

    start_gen = time.time()
    n1.start_genetic_v2()
    end_gen = time.time()

    start_gen_brute = time.time()
    n1.start_network_brute_force()
    end_gen_brute = time.time()

    print(f'Gen duration : {end_gen - start_gen}\n')
    print(f'Gen brute duration : {end_gen_brute - start_gen_brute}\n')
    print(f'Brute force duration : {end_brute - start_brute}\n')


if __name__ == '__main__':
    main()

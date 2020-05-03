import random


class Server:
    def __init__(self, key):
        self.id = key
        self.neighbors = {}

    def __str__(self):
        return str(self.id) + ' connected to: ' + str([x.id for x in self.neighbors])

    def add_neighbor(self, server, weight=1):
        self.neighbors[server] = weight

    def get_neighbors(self):
        return self.neighbors.keys()

    def get_id(self):
        return self.id

    def get_weight(self, server):
        return self.neighbors[server]

    def get_num_of_neighbors(self):
        return len(self.neighbors)


class Network:
    def __init__(self):
        self.server_list = {}
        self.server_num = 0

    def add_server(self, key):
        self.server_num = self.server_num + 1
        new_server = Server(key)
        self.server_list[key] = new_server
        return new_server

    def get_server(self, n):
        if n in self.server_list:
            return self.server_list[n]
        else:
            return None

    def __contains__(self, server):
        return server in self.server_list

    def add_connections(self, server_a, server_b, weight=1):
        if server_a not in self.server_list:
            new_server_a = self.add_server(server_a)

        if server_b not in self.server_list:
            new_server_b = self.add_server(server_b)

        self.server_list[server_a].add_neighbor(self.server_list[server_b], weight)
        self.server_list[server_b].add_neighbor(self.server_list[server_a], weight)

    def get_servers(self):
        return self.server_list.keys()

    def __iter__(self):
        return iter(self.server_list.values())


class DistributedNetwork:
    def __init__(self, server_num, port_range, file_max_time):
        self.network = Network()

        for i in range(server_num):
            self.network.add_server(i)

        for i in range(server_num):
            num_of_ports = random.randrange(port_range)

            if num_of_ports == 0:
                num_of_ports = 1
            if self.network.server_list[i].get_num_of_neighbors() == num_of_ports:
                num_of_ports = 0

            for j in range(num_of_ports):
                pick_a_server = random.randrange(server_num)
                while True:
                    print("id i:" + str(i) + " id n: " + str(pick_a_server) + " len: " + str(self.network.server_list[pick_a_server].get_num_of_neighbors()))
                    if(pick_a_server != i
                            and self.network.server_list[pick_a_server].get_num_of_neighbors() < port_range):
                        break
                    pick_a_server = random.randrange(server_num)

                self.network.add_connections(i, pick_a_server, random.randrange(file_max_time))

    def __str__(self):
        to_str = ""
        for server in self.network:
            to_str += str(server.get_id()) + ":\n   "
            for neighbor in server.get_neighbors():
                to_str += "(id: " + str(neighbor.get_id()) + ", time: " + str(server.get_weight(neighbor)) \
                          + "), "
            to_str += "\n\n"

        return to_str

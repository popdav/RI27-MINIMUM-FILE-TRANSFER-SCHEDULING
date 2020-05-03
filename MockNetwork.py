import random
from queue import Queue

MAX_FILE_SIZE = 1024


class Server:
    def __init__(self, key, longitude, latitude, max_files_to_send, num_of_ports):
        self.id = key
        self.longitude = longitude
        self.latitude = latitude
        self.neighbors = {}
        self.queue_of_transfers = Queue()

        self.file_num = random.randrange(1, max_files_to_send)
        self.files = {}
        for i in range(self.file_num):
            self.files[str(self.id) + '_f' + str(i)] = random.randrange(1, MAX_FILE_SIZE)

        self.num_of_ports = num_of_ports
        self.ports = {}
        for i in range(num_of_ports):
            self.ports[i+1] = {'receive': True, 'send': True}

    def __str__(self):
        return str(self.id) + ':\n connected to: ' + str([x for x in self.neighbors])\
                + '\n tasks: ' + self.str_tasks()

    def str_tasks(self):
        list_of_tasks = list(self.queue_of_transfers.queue)
        str_list = "[ "
        for item in list_of_tasks:
            str_list += "(" + item[0] + ", " + str(item[1].id) + ") "
        str_list += " ]"
        return str_list

    def add_to_queue(self, file, server):
        self.queue_of_transfers.put((file, server))

    def get_free_port(self):
        for i in range(self.num_of_ports):
            if self.ports[i+1]['receive'] and self.ports[i]['send']:
                return i

        return False

    def add_neighbor(self, server):
        self.neighbors[server.get_id()] = server

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

    def init_network(self):
        server_num = 10
        port_num = 3
        for i in range(server_num):
            self.add_server(i, random.randrange(100), random.randrange(100), 20, port_num)

        for k in self.server_list.keys():
            num_of_tasks = random.randrange(1, server_num/2)
            for j in range(num_of_tasks):
                file_id = random.randrange(self.server_list[k].file_num)
                file_name = str(k) + '_f' + str(file_id)
                server_to = self.server_list[random.randrange(server_num)]
                self.server_list[k].add_to_queue(file_name, server_to)

    def add_server(self, key, longitude, latitude, max_files_to_send, num_of_ports):
        self.server_num = self.server_num + 1
        new_server = Server(key, longitude, latitude, max_files_to_send, num_of_ports)

        for k in self.server_list.keys():
            new_server.add_neighbor(self.server_list[k])
            self.server_list[k].add_neighbor(new_server)

        self.server_list[key] = new_server
        return new_server

    def get_server(self, n):
        if n in self.server_list:
            return self.server_list[n]
        else:
            return None

    def __contains__(self, server):
        return server in self.server_list

    def get_servers(self):
        return self.server_list.keys()

    def __iter__(self):
        return iter(self.server_list.values())





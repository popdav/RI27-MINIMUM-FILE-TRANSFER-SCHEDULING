import random
from queue import Queue
from threading import Thread
import time

from GeneticFileTransferScheduling import GeneticAlgorithm

MAX_FILE_SIZE = 1024
NETWORK_SPEED = 256


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
            self.ports[i + 1] = {'receive': True, 'send': True}

    def __str__(self):
        return str(self.id) + ':\n connected to: ' + str([x for x in self.neighbors]) \
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
            if self.ports[i + 1]['receive'] and self.ports[i + 1]['send']:
                return i + 1

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

    def start_sending_brute_force(self):
        print(f'Thread {self.id}: starting')

        while not self.queue_of_transfers.empty():

            current_port = self.get_free_port()

            if current_port is False:
                time.sleep(5)
                continue

            self.ports[current_port]['send'] = False
            current_task = self.queue_of_transfers.get()
            receiving_port = current_task[1].get_free_port()

            if receiving_port is False:
                self.queue_of_transfers.put(current_task)
                self.ports[current_port]['send'] = True
                time.sleep(5)
                continue

            current_task[1].ports[receiving_port]['receive'] = False
            print(f'Sending file : {current_task[0]} from {self.id} to {current_task[1].id}\n')
            file_size = self.files[current_task[0]]
            time.sleep(file_size / (NETWORK_SPEED * 1.0))
            print(f'Finished sending file : {current_task[0]} from {self.id} to {current_task[1].id}\n')
            self.ports[current_port]['send'] = True
            current_task[1].ports[receiving_port]['receive'] = True

        print(f"Thread {self.id}: finished")

    def genetic_optimization(self):
        list_of_tasks = list(self.queue_of_transfers.queue)
        poss_val = []
        for task in list_of_tasks:
            file_name = task[0]
            file_size = self.files[file_name]
            server = task[1]
            poss_val.append(
                {
                    'file_name': file_name,
                    'neighbor_id': server.id,
                    'neighbor_ports': server.num_of_ports,
                    'time_to_send': file_size / (NETWORK_SPEED * 1.0)
                }
            )
            self.queue_of_transfers.get()

        print('start optimization server id: ' + str(self.id))
        GA = GeneticAlgorithm(len(list_of_tasks), poss_val)

        best_code = GA.optimaze()
        print('stop optimization server id: ' + str(self.id))
        # for item in best_code:
        #     self.queue_of_transfers.put((item['file_name'], self.neighbors[item['neighbor_id']]))
        return


class Network:
    def __init__(self):
        self.server_list = {}
        self.server_num = 0

    def init_network(self):
        server_num = 6
        port_num = 3
        for i in range(server_num):
            self.add_server(i, random.randrange(100), random.randrange(100), 20, port_num)

        for k in self.server_list.keys():
            num_of_tasks = random.randrange(1, server_num / 2)
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

    def start_network_brute_force(self):

        threads = []

        for i in range(self.server_num):
            threads.append(Thread(target=self.server_list[i].start_sending_brute_force))
            threads[i].start()

        for thread in threads:
            thread.join()

    def start_genetic_algorithm(self):
        threads = []
        for i in range(self.server_num):
            threads.append(Thread(target=self.server_list[i].genetic_optimization))
            threads[i].start()

        for thread in threads:
            thread.join()

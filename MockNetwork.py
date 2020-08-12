import random
from queue import Queue
from threading import Thread
import time
import copy
import json
import math

from GeneticFileTransferScheduling import GeneticAlgorithm

MAX_FILE_SIZE = 1024
NETWORK_SPEED = 256


class Server:
    def __init__(self, key, max_files_to_send, num_of_ports, i, files = None):
        self.id = key
        self.index = i
        self.my_time = 0
        self.neighbors = {}
        self.queue_of_transfers = Queue()
        self.copy_of_queue_of_transfers = Queue()

        self.queue_of_receiving = Queue()
        self.copy_of_queue_of_receiving = Queue()

        self.file_num = max_files_to_send
        if files == None :
            self.files = {}
            for i in range(self.file_num):
                self.files[str(self.id) + '_f' + str(i)] = random.randrange(1, MAX_FILE_SIZE)
        else:
            self.files = files
            
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
        self.copy_of_queue_of_transfers.put((file, server))

    def add_to_queue_receive(self, file, server):
        self.queue_of_receiving.put((file, server))
        self.copy_of_queue_of_receiving.put((file, server))

    def copy_queue_to_original(self):
        for task in self.copy_of_queue_of_transfers.queue:
            self.queue_of_transfers.put(task)

        for task in self.copy_of_queue_of_receiving.queue:
            self.queue_of_receiving.put(task)

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

    def cacl_my_time(self):
        list_transfer = list(self.queue_of_transfers.queue)
        list_receiving = list(self.queue_of_receiving.queue)
        i = 0
        j = 0
        print(f"Server {self.id}")
        while j < len(list_receiving):
            task_receiving = list_receiving[j]
            print(f"time: {self.my_time}, tr time: {task_receiving[1].my_time}")
            if task_receiving[1].index < self.index:
                if 2*self.my_time < task_receiving[1].my_time:
                    self.my_time = task_receiving[1].my_time
                else:
                    self.my_time += task_receiving[1].my_time
                j += 1
            else:
                break

        if math.ceil(self.my_time) % 4 == 0:
            self.my_time = math.ceil(self.my_time) 
        else:
            self.my_time = math.ceil(self.my_time) + 4 - (math.ceil(self.my_time) % 4) 
        
        while i < len(list_transfer):
            task_transfer = list_transfer[i]

            time_to_add = task_transfer[1].my_time
            pred_server = None
            receiving_server_to_list = list(task_transfer[1].queue_of_receiving.queue)
            if len(receiving_server_to_list) > 1:
                for k in range(len(receiving_server_to_list)):
                    if(receiving_server_to_list[k][1].id == self.id):
                        pred_server = receiving_server_to_list[k-1][1]
                        time_to_add = max(receiving_server_to_list[k-1][1].my_time, task_transfer[1].my_time)
                        break
            
            pred_is_blocked = False
            if pred_server is not None:
                pred_server_list_receiving = list(pred_server.queue_of_receiving.queue)
                
                if len(pred_server_list_receiving) > 0 \
                and task_transfer[1].index != pred_server_list_receiving[0][1].index:
                    if pred_server_list_receiving[0][1].index < pred_server.index:
                        pred_is_blocked = True

            print(f"time: {self.my_time}, tt time: {task_transfer[1].my_time}, to add: {time_to_add}")
            if time_to_add < self.my_time or pred_is_blocked:
                self.my_time += self.files[task_transfer[0]] / NETWORK_SPEED

            elif task_transfer[1].index > self.index:
                self.my_time += self.files[task_transfer[0]] / NETWORK_SPEED
            else:
                if math.ceil(time_to_add) % 4 == 0:
                    self.my_time += math.ceil(time_to_add) + self.files[task_transfer[0]] / NETWORK_SPEED
                else:
                    self.my_time += math.ceil(time_to_add) + 4 - (math.ceil(time_to_add) % 4) + self.files[task_transfer[0]] / NETWORK_SPEED
            i += 1
        
        print(f"End server {self.id}, time: {self.my_time}\n")
        return self.my_time

    def start_sending_brute_force(self):
        print(f'Thread {self.id}: starting')
        start_brute = time.time()
        while not self.queue_of_transfers.empty():

            current_port = self.get_free_port()

            if current_port is False:
                time.sleep(4)
                continue

            self.ports[current_port]['send'] = False
            current_task = self.queue_of_transfers.get()
            receiving_port = current_task[1].get_free_port()

            if receiving_port is False:
                self.queue_of_transfers.put(current_task)
                self.ports[current_port]['send'] = True
                time.sleep(4)
                continue

            current_task[1].ports[receiving_port]['receive'] = False
            print(f'Sending file : {current_task[0]} from {self.id} to {current_task[1].id}\n')
            file_size = self.files[current_task[0]]
            time.sleep(file_size / (NETWORK_SPEED * 1.0))
            print(f'Finished sending file : {current_task[0]} from {self.id} to {current_task[1].id}\n')
            self.ports[current_port]['send'] = True
            current_task[1].ports[receiving_port]['receive'] = True
        end_brute = time.time()
        print(f"Thread {self.id}: finished, duration : {end_brute - start_brute}")


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

        # print('start optimization server id: ' + str(self.id))
        GA = GeneticAlgorithm(len(list_of_tasks), poss_val, self.id)

        best_code = GA.optimaze()
        # print(f'stop optimization server id: {str(self.id)} \n')
        for item in best_code:
            self.queue_of_transfers.put((item['file_name'], self.neighbors[item['neighbor_id']]))
        return


class Network:
    def __init__(self):
        self.server_map = {}
        self.server_list = []
        self.server_num = 0

    def init_network(self, s_num, p_num, f_num):
        server_num = s_num
        port_num = p_num
        for i in range(server_num):
            self.add_server(i, f_num, port_num, i)

        for k in self.server_map.keys():
            num_of_files = self.server_map[k].file_num
            # num_of_tasks = random.randrange(1, num_of_files)
            for j in range(num_of_files):
                #file_id = random.randrange(self.server_map[k].file_num)
                file_name = str(k) + '_f' + str(j)
                server_to = self.server_map[random.randrange(server_num)]
                while server_to.id == k:
                    server_to = self.server_map[random.randrange(server_num)]
                self.server_map[k].add_to_queue(file_name, server_to)
                server_to.add_to_queue_receive(file_name, self.server_map[k])

    def add_server(self, key, max_files_to_send, num_of_ports, index, files=None):
        self.server_num = self.server_num + 1
        new_server = Server(key, max_files_to_send, num_of_ports, index, files)
        self.server_list.append(new_server)
        for k in self.server_map.keys():
            new_server.add_neighbor(self.server_map[k])
            self.server_map[k].add_neighbor(new_server)

        self.server_map[key] = new_server
        return new_server

    def save_to_json(self, file):
        json_list = []
        for i in range(self.server_num):
            server_json = {
                'id': self.server_list[i].id,
                'num_of_ports': self.server_list[i].num_of_ports,
                'file_num': self.server_list[i].file_num,
                'files': self.server_list[i].files,
                'list_of_transfer': [(task[0], task[1].id) for task in list(self.server_list[i].queue_of_transfers.queue)],
                'list_of_receiving': [(task[0], task[1].id) for task in list(self.server_list[i].queue_of_receiving.queue)]
            }
            json_list.append(server_json)
        
        f = open(file, "w")
        f.write(json.dumps(json_list))
        f.close()

    def load_from_json(self, file):
        f = open(file, "r")
        json_list = f.read()
        f.close()
        list_servers = json.loads(json_list)
        self.server_map = {}
        self.server_num = 0
        for (server, i) in zip(list_servers, range(len(list_servers))):
            self.add_server(server['id'], server['file_num'], server['num_of_ports'], i,server['files'])

        for server in list_servers:
            for task in server['list_of_transfer']:
                server_to = self.server_map[task[1]]
                self.server_map[server['id']].add_to_queue(task[0], server_to)
            for task in server['list_of_receiving']:
                server_to = self.server_map[task[1]]
                self.server_map[server['id']].add_to_queue_receive(task[0], server_to)

    def get_server(self, n):
        if n in self.server_map:
            return self.server_map[n]
        else:
            return None

    def __contains__(self, server):
        return server in self.server_map

    def get_servers(self):
        return self.server_map.keys()

    def __iter__(self):
        return iter(self.server_map.values())

    def start_network_brute_force(self):
        print("Start brute")
        threads = []

        for i in range(self.server_num):
            threads.append(Thread(target=self.server_list[i].start_sending_brute_force))
            threads[i].start()

        for thread in threads:
            thread.join()

    def start_genetic_algorithm(self):
        print("Start genetic")
        threads = []
        for i in range(self.server_num):
            threads.append(Thread(target=self.server_map[i].genetic_optimization))
            threads[i].start()

        for thread in threads:
            thread.join()

    def calc_time(self):
        for i in range(self.server_num):
            print(f"Server {self.server_list[i].id}, index: {self.server_list[i].index}")   

        arr_of_time = []
        for i in range(self.server_num):
            arr_of_time.append(self.server_list[i].cacl_my_time())
            
        print(arr_of_time)
import multiprocessing
import os
import time

from clients.simple_client import run_simple_client
from clients.requests_client import run_requests_client

from servers.socket_server import run_socket_server
from servers.selector_server import run_selector_server
from servers.selectors_servers import run_selectors_server
from servers.flask_server import run_flask_server

import pandas as pd
import matplotlib.pyplot as plt




def cpu_bound_func(accuracy = 20):
    def exp(acc):
        def factorial(n):
            if n == 0:
                return 1
            else:
                return n * factorial(n-1)
        e = 0
        for x in range(accuracy):
            e += 1/factorial(x)
        return e
    return exp(accuracy)

def test_loop():

    counter = 2
    pings = 5000

    os.system('sudo kill -9 `sudo lsof -t -i:8090`')

    operation_per_sec = []
    cpu_bound_per_sec = []
    servers = [
        run_socket_server, 
        run_selector_server, 
        run_selectors_server,
        run_flask_server,
        ]
    clients = [
        run_simple_client,
        run_requests_client
    ]
    
    #testing for per second operations
    for server in servers:
        returned_value = multiprocessing.Value("d", 0.0, lock=False)

        server_thread = multiprocessing.Process(target=server)
        server_thread.start()

        if server.__name__ == 'run_flask_server':
            client_process = multiprocessing.Process(target=clients[1], args = (counter, pings, returned_value))
            client_process.start()
            client_process.join()
        else:
            client_process = multiprocessing.Process(target=clients[0], args = (counter, pings, returned_value))
            client_process.start()
            client_process.join()

        operation_per_sec.append(returned_value.value)
        print(operation_per_sec)
        server_thread.terminate()

        os.system('sudo kill -9 `sudo lsof -t -i:8090`')
    counter = 1
    pings = 300

    # testing cpu bound with cpu bound functin
    for server in servers:
        returned_value = multiprocessing.Value("d", 0.0, lock=False)

        server_thread = multiprocessing.Process(target=server, args=[cpu_bound_func])
        server_thread.start()

        if server.__name__ == 'run_flask_server':
            client_process = multiprocessing.Process(target=clients[1], args = (counter, pings, returned_value))
            client_process.start()
            client_process.join()
        else:
            client_process = multiprocessing.Process(target=clients[0], args = (counter, pings, returned_value))
            client_process.start()
            client_process.join()

        cpu_bound_per_sec.append(returned_value.value)
        print(cpu_bound_per_sec)
        server_thread.terminate()

        os.system('sudo kill -9 `sudo lsof -t -i:8090`')

    operation_per_sec = [ '%.2f' % elem for elem in operation_per_sec ]
    cpu_bound_per_sec = [ '%.2f' % elem for elem in cpu_bound_per_sec ]

    print('operatino_per_sec', operation_per_sec)
    print('cpu_bound', cpu_bound_per_sec)

    return operation_per_sec, cpu_bound_per_sec

def create_table(operations, cpu_bound):
    df = pd.DataFrame(data = {'request-response': operations, 'CPU bound': cpu_bound})
    df = df.rename(index={0: 'pure socket server', 1: 'Select', 2:'Selectors', 3: 'HTTP server'})
    print(df)
    df.to_excel('results.xlsx')
    return df

def draw_plot(df):

    list_request = df['request-response'].tolist()
    list_request = [float(x) for x in list_request]

    list_request_cpu_bound = df['CPU bound'].tolist()
    list_request_cpu_bound = [float(x) for x in list_request_cpu_bound]
    
    labels = ['pure socket server', 'Select', 'Selectors', 'HTTP server']

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.title("request response (20000 requests)")
    plt.plot(labels, list_request, '-g')


    plt.subplot(1, 2, 2)
    plt.title("cpu bound(450 requests, e calculating)")
    plt.plot(labels, list_request_cpu_bound, '--go')
  


    plt.savefig('saved_figure.png')

def main():
    operations, cpu_bound = test_loop()
    df = create_table(operations,cpu_bound)
    draw_plot(df)
    

if __name__ == '__main__':
    main()
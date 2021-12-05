import socket
import time
import statistics

SERVER_HOST = 'localhost'
SERVER_PORT = 8090


def run_simple_client(counter = 1, pings = 100, returned_value = None): 
    # returned_value.value = 2
    # print(counter, pings, returned_value)
    results = []
    print(f'Client start')
    for n in range(counter):
        client_socket = socket.socket()
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        
        
        
        now = time.time()
        
        for num in range(pings):
            client_socket.send(str(num).encode())
            # print('receiving response...')
            response = client_socket.recv(4096)
            # print(f'{response.decode("utf-8")} was received')
            # print('Close connection')

        delta = time.time() - now

        client_socket.close()

        results.append(pings/delta)
        print('Client prosses is killed')

        if returned_value.value  == 0.0:
            returned_value.value = statistics.mean(results)
        pings *= 2
    return statistics.mean(results)

def main():
    run_simple_client()
    

if __name__ == '__main__':
   main()
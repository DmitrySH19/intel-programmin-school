import socket


    

def get_server_socket():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    return server_sock

def run_socket_server(cpu_bound = None):
    server_socket = get_server_socket()
    print(f'Socket server start',
          f'Waiting new connection...')
    while True:
        # print('Waiting new connection...')
        client_socket, client_addr = server_socket.accept()
        # print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')

        while True:
            request = client_socket.recv(4096)
            # print(f'Received: {request}')

            if request:
                if cpu_bound:
                    result = cpu_bound(int(request))
                    client_socket.send(str(result).encode())
                else:
                # print('Sending Ping to client...')
                    client_socket.send('Pong'.encode())
            else:
                # print('Client has gone. Closing client socket...')
                client_socket.close()
                break

def main():
    run_socket_server()
    
if __name__ == '__main__':
    main()
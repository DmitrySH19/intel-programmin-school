import socket
from select import select


def get_server_socket():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    server_sock.listen()

    print(f'Selector server start',
          f'Waiting new connection...')

    return server_sock


to_monitor = []


def accept_connection(server_sock: socket.socket) -> None:
    client_socket, client_addr = server_sock.accept()
    # print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    to_monitor.append(client_socket)


def send_message(client_sock: socket.socket, cpu_bound = None) -> None:
    request = client_sock.recv(4096)
    # print(f'Received: {request}')

    if request:

        if cpu_bound:
            result = cpu_bound(int(request))
            client_sock.send(str(result).encode())
        else:
        # print('Sending Ping to client...')
            client_sock.send('Pong'.encode())
    else:
        # print('Client has gone. Closing client socket...')
        to_monitor.remove(client_sock)
        client_sock.close()


def event_loop(server_socket, cpu_bound = None):
    while True:
        # readable, writable, errors
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock == server_socket:
                accept_connection(sock)
            else:
                send_message(sock, cpu_bound)

def run_selector_server(cpu_bound = None):
    server_socket = get_server_socket()
    to_monitor.append(server_socket)
    event_loop(server_socket, cpu_bound)

def main():
    run_selector_server()


if __name__ == '__main__':
    main()

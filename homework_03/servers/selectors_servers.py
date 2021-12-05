import selectors
import socket



selector = selectors.DefaultSelector()


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8090))
    
    print(f'Selectors server start',
          f'Waiting new connection...')

    server_sock.listen()

    selector.register(
        fileobj=server_sock,
        events=selectors.EVENT_READ,
        data=accept_connection
    )


to_monitor = []


def accept_connection(server_sock: socket.socket, cpu_bound) -> None:
    client_socket, client_addr = server_sock.accept()
    # print(f'Connection has been received from {client_addr[0]}:{client_addr[1]}')
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


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
        selector.unregister(client_sock)
        client_sock.close()


def event_loop(cpu_bound = None):
    while True:
        events = selector.select()  # key, events (bit mask read or write)
        for key, _ in events: # key has fileobj, events, data
            callback_function = key.data
            callback_function(key.fileobj, cpu_bound)

def run_selectors_server(cpu_bound = None):
    server()
    event_loop(cpu_bound)

def main():
    run_selectors_server()

if __name__ == '__main__':
    main()
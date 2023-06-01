import socket
from multiprocessing import Queue


def server_feed(ip: str, port: int, q: Queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Initialize server
        s.bind((ip, port))
        s.listen()

        # Client connection
        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}')

            # Listen to messages from client
            while True:
                data = conn.recv(1024)
                try:
                    # Parse message and feed it through queue
                    msg = data.decode('utf-8').split(' ')
                    name = msg[0]
                    value = list(map(float, msg[1:]))
                    q.put_nowait({
                        'name': name,
                        'value': value
                    })
                except Exception:
                    pass

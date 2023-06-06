import socket
from multiprocessing import Queue


def server_feed(ip: str, port: int, q: Queue):
    """Create a server listening for messages and feeding them to the rendering process."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Initialize server
        s.bind((ip, port))
        s.listen()

        # Client connection
        conn, addr = s.accept()
        with conn:
            print(f'Connected with {addr}')

            # Listen to messages from client
            while True:
                data = conn.recv(1024)
                try:
                    # Parse message and feed it to rendering process through the queue
                    message = data.decode('utf-8').split(' ')
                    datatype = message[0]
                    name = message[1]
                    value = message[2:]
                    if datatype == 'i':
                        value = list(map(int, value))
                    else:
                        value = list(map(float, value))
                    q.put_nowait({
                        'np_dtype': 'i4' if datatype == 'i' else 'f4',
                        'name': name,
                        'value': value
                    })
                except Exception as e:
                    print(e)
                    pass

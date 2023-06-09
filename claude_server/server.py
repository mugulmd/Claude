import socket
from multiprocessing import Queue
import logging


def server_feed(ip: str, port: int, q: Queue):
    """Create a server listening for messages and feeding them to the rendering process."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Initialize server
        s.bind((ip, port))
        s.listen()

        # Client connection
        conn, addr = s.accept()
        with conn:
            logging.info('Connected with %s', addr)

            # Listen to messages from client
            while True:
                data = conn.recv(1024)
                try:
                    # Decode message and feed it to rendering process through the queue
                    message = data.decode('utf-8')
                    message = message.replace('\r', '')
                    message = message.replace('\n', '')
                    logging.debug('Received message: %s', message)
                    message = message.split(' ')
                    q.put_nowait(message)
                except Exception as e:
                    logging.error('%s', e)
                    pass

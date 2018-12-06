import socket
import threading
from server import HOST, PORT


class Client(socket.socket):
    def __init__(self, id):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((HOST, PORT[id]))
        self.sendall(bytes('log-in succeeded', 'utf-8'))

    def sending(self):
        while True:
            msg = input('[  me ]: ')
            self.sendall(bytes(msg, 'utf-8'))

    def recving(self):
        while True:
            msg = str(self.recv(1024), 'utf-8')
            print('\r[guest]: {}\n[  me ]: '.format(msg), end='')

    def start(self):
        threading.Thread(target=self.recving).start()
        threading.Thread(target=self.sending).start()


if __name__ == '__main__':
    c = Client(0)
    c.start()

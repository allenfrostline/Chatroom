import socket
import threading


HOST, PORT = 'localhost', [9998, 9999]
names = ['a', 'b']
unsent_msg = {name: [] for name in names}


class Server(socket.socket):
    def __init__(self, family, type, id):
        super().__init__(family, type)
        self.bind((HOST, PORT[id]))
        self.listen(1)
        self.conn = None
        self.sender = names[id]
        self.receiver = names[1 - id]

    def recving(self):
        conn, addr = self.accept()
        self.conn = conn
        while True:
            msg = str(self.conn.recv(1024), 'utf-8')
            print('[{}]: (unsent) {}'.format(self.sender, msg))
            if msg == 'log-in succeeded':
                continue
            unsent_msg[self.sender].append(msg)

    def sending(self):
        while True:
            while unsent_msg[self.receiver]:
                msg = unsent_msg[self.receiver].pop()
                self.conn.sendall(bytes(msg, 'utf-8'))
                print('[{}]: ( sent ) {}'.format(self.receiver, msg))

    def start(self):
        threading.Thread(target=self.recving).start()
        threading.Thread(target=self.sending).start()


if __name__ == '__main__':
    sa = Server(socket.AF_INET, socket.SOCK_STREAM, 0)
    sb = Server(socket.AF_INET, socket.SOCK_STREAM, 1)
    sa.start()
    sb.start()

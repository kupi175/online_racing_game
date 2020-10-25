import threading


class player:
    string_multiplayer = 2

    message_queue = []

    connection = None
    address = None
    socket = None
    imh = None  # incoming message handler

    id = -1
    is_running = True

    def __init__(self, connection, address, socket, id):
        self.connection = connection
        self.address = address
        self.socket = socket
        self.id = id
        self.imh = threading.Thread(target=self.incoming_message_handler)

    def incoming_message_handler(self):
        while True:
            try:
                self.message_queue.append(self.socket.recv(1024 * self.string_multiplayer))
            except Exception as e:
                print('player', self.address, 'has dissconnected with:', e)
                break

    def get_messages(self):
        outbound = self.message_queue
        self.message_queue = []
        return outbound

    def send_message(self, msg):
        try:
            self.connection.send(str.encode('tst'))
        except Exception as e:
            print('connection:', self.id, e)

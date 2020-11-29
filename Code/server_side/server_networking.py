import threading


class player:
    string_multiplayer = 2

    message_queue = None

    connection = None
    address = None
    socket = None
    imh = None  # incoming message handler

    is_running = True

    def __init__(self, connection, address, msg = 'you have connected'):
        self.message_queue = list()
        self.connection = connection
        self.address = address
        self.id = id
        self.imh = threading.Thread(target=self.incoming_message_handler)
        self.imh.start()
        self.connection.send(str.encode(msg))

    def incoming_message_handler(self):
        while True:
            try:
                self.message_queue.append(self.connection.recv(1024 * self.string_multiplayer).decode('utf-8'))
                print(self.message_queue)
            except Exception as e:
                print('player', self.address, 'has dissconnected with:', e)
                break

    def get_messages(self):
        outbound = list(self.message_queue)
        self.message_queue = []
        return outbound

    def send_message(self, msg):
        try:
            self.connection.send(str.encode('tst'))
        except Exception as e:
            print('connection:', self.id, e)

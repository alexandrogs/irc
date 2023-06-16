import sqlite3
import socket
import cmd
import sys

class IRCClient(cmd.Cmd):
    prompt = '>> '

    def __init__(self, db_file, nickname):
        super().__init__()
        self.db_file = db_file
        self.nickname = nickname
        self.connections = []
        self.db_conn = sqlite3.connect(db_file)
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server TEXT,
                channel TEXT
            )
        ''')
        self.db_conn.commit()

    def connect(self, server, port):
        irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc_socket.connect((server, port))
        irc_socket.send(f'NICK {self.nickname}\r\n'.encode())
        irc_socket.send(f'USER {self.nickname} 0 * :{self.nickname}\r\n'.encode())
        self.connections.append(irc_socket)

    def disconnect(self):
        for irc_socket in self.connections:
            irc_socket.send('QUIT\r\n'.encode())
            irc_socket.close()
        self.connections = []

    def servers(self):
        servers = []
        for irc_socket in self.connections:
            servers += [irc_socket.getpeername()[0]]
        return servers

    def join_channel(self, channel):
        for irc_socket in self.connections:
            irc_socket.send(f'JOIN {channel}\r\n'.encode())
            server = irc_socket.getpeername()[0]
            self.db_cursor.execute('''
                INSERT INTO channels (server, channel)
                VALUES (?, ?)
            ''', (server, channel))
            self.db_conn.commit()

    def send_message_to_channel(self, channel, message):
        for irc_socket in self.connections:
            irc_socket.send(f'PRIVMSG {channel} :{message}\r\n'.encode())

    def do_infos(self, args):
        print('ok')
        for irc_socket in self.connections:
            irc_socket.send("LIST\r\n".encode())
            response = irc_socket.recv(2048).decode()
            aux = response.split("\r\n")
            for ___ in aux:
                if ___.startswith(":"):
                    infos = ___.split(" ")
                    server = infos[1]
                    channel = infos[2]
                    print(f"Server: {server} | Channel: {channel}")

    def do_messages(self, args):
        for irc_socket in self.connections:
            irc_socket.setblocking(False)
            try:
                while True:
                    message = irc_socket.recv(1024).decode().strip()
                    if message:
                        prefix = message.split(' ')[0]
                        if prefix.startswith(':'):
                            channel = prefix[1:]
                            print(f'[{channel}] {message}')
            except socket.error:
                pass

    def do_send(self, args):
        """Comando para enviar mensagem para um canal específico"""
        channel, message = args.split(' ', 1)
        self.send_message_to_channel(channel, message)

    def do_connect(self, args):
        """Comando para conectar a um novo servidor IRC"""
        if ' ' not in args:
            port = 6667
            server = args
        else:
            server, port = args.split(' ')
        self.connect(server, int(port))

    def do_join(self, args):
        """Comando para juntar-se a um canal em um servidor específico"""
        self.join_channel(args)

    def do_quit(self, args):
        """Comando para sair do prompt e desconectar dos servidores"""
        self.disconnect()
        print('Saindo do prompt...')
        return True

    def default(self, line):
        print('Comando inválido.')

if __name__ == '__main__':
    nick = sys.argv[1]
    irc = IRCClient('irc.db', nick)
    irc.db_cursor.execute("SELECT DISTINCT server, channel FROM channels")
    rows = irc.db_cursor.fetchall()
    for row in rows:
        server, channel = row
        irc.connect(server, 6667)
        irc.join_channel(channel)
    def _(tag, func, args=[]):
        with open(tag) as f: all = f.read().split('\n')
        for each in all:
            aux =  each + args
            func(zip(*aux))
    evts = [
        ['servers', 'channels'],
        [irc.connect, irc.join_channel],
        [[6667], []]
    ]
    for tag, func, args in zip(*evts):
        _(tag, func, args)
    with open('channels') as f: all = f.read().split('\n')
    for each in all:
        irc.join_channel(each)
    irc.cmdloop('Iniciando prompt de comando...')
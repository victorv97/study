from threading import Thread
from time import sleep
import socket
import random
import json
import string

SYMBOLS = list(''.join([string.ascii_lowercase, string.ascii_uppercase, string.digits]))
TIMEOUT = 120
ADDRESS = ('localhost', 9090)
BUFFER_SIZE = 1024
WRONG_LOGIN = "Wrong _login!"
WRONG_PASSWORD = "Wrong _password!"
SUCCESS_MESSAGE = "Connection success!"
MANY_ATTEMPTS = 'Too many attempts to connect!'
BAD_REQUEST = 'Bad request!'

logins_list = [
    'admin', 'Admin', 'admin1', 'admin2', 'admin3',
    'user1', 'user2', 'root', 'default', 'new_user',
    'some_user', 'new_admin', 'administrator',
    'Administrator', 'superuser', 'super', 'su', 'alex',
    'suser', 'rootuser', 'adminadmin', 'useruser',
    'superadmin', 'username', 'username1'
]


def logins():
    for login in logins_list:
        yield login


def random_password():
    # generating random _password of length from 6 to 10
    return ''.join(random.choice(SYMBOLS) for i in range(random.randint(6, 10)))


def random_login():
    return random.choice(list(logins()))


def response(message):
    return json.dumps({'result': message}).encode('utf8')


class SiteEmulator:

    def __init__(self):
        self._socket = None
        self._serv = None
        self._message = []
        self._password = None
        self._login = None

        self.generate()

    def start_server(self):
        print('Starting server')
        self._serv = Thread(target=self.server)
        self._serv.start()
        while self._serv.is_alive():
            user_input = input()
            if user_input.lower() == 'stop':
                return

    def generate(self):
        self._message = []
        self._password = random_password()
        self._login = random_login()
        print('Login and password are generated')

    def stop_server(self):
        print('Stopping server')
        self._socket.close()
        self._serv.join()

    def server(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(ADDRESS)
        while True:
            try:
                self._socket.listen(1)
                conn, addr = self._socket.accept()
                conn.settimeout(TIMEOUT)
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    self._message.append(data.decode('utf8'))
                    if len(self._message) > 100_000_000:
                        conn.send(response(MANY_ATTEMPTS))
                        break
                    if not data:
                        break
                    try:
                        login_ = json.loads(data.decode('utf8'))['login']
                        password_ = json.loads(data.decode('utf8'))['password']
                    except:
                        conn.send(response(BAD_REQUEST))
                        continue
                    if login_ == self._login:
                        if self._password == password_:
                            conn.send(response(SUCCESS_MESSAGE))
                            print('Someone logged in with admin rights. Login and password will be changed')
                            self.generate()
                            break
                        # simulate time vulnerability
                        elif self._password.startswith(password_):
                            sleep(0.1)
                            conn.send(response(WRONG_PASSWORD))
                        else:
                            conn.send(response(WRONG_PASSWORD))
                    else:
                        conn.send(response(WRONG_LOGIN))
                conn.close()
            except:
                return


if __name__ == '__main__':
    emulator = SiteEmulator()
    emulator.start_server()
    emulator.stop_server()

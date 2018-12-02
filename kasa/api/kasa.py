import socket
import json
from struct import pack


class Kasa:

    def __init__(self, host, port=9999):
        self.host = host
        self.port = port

    def _send_raw_command(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
            tcp_sock.connect((self.host, self.port))
            tcp_sock.send(self._encrypt(cmd))
            data = b''
            while True:
                chunk = tcp_sock.recv(2048)
                if chunk:
                    data += chunk
                if not chunk or len(chunk) < 2048:
                    break
        return self._decrypt(data[4:])

    def _send_json_command(self, cmd):
        js = json.dumps(cmd)
        data = self._send_raw_command(js)
        print(data)
        print(len(data))
        return json.loads(data)

    def _send_command(self, topic, cmd, arg=None):
        struct = {topic: {cmd: arg}}
        js = self._send_json_command(struct)
        return js[topic][cmd]

    @staticmethod
    def _encrypt(string):
        bytea = bytes(string, 'UTF-8')
        key = 171
        result = pack('>I', len(string))
        for i in bytea:
            a = key ^ i
            key = a
            result += bytes([a])
        return result

    @staticmethod
    def _decrypt(data):
        key = 171
        result = b""
        for i in data:
            a = key ^ i
            key = i
            result += bytes([a])
        string = str(result, 'ascii')
        return string

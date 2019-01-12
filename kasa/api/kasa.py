import socket
import json
from struct import pack, unpack


class Kasa:

    def __init__(self, host : str, port=9999):
        self.host : str = host
        self.port : int = port

    def get_host(self) -> str:
        return self.host

    def get_port(self) -> int:
        return self.port

    def _send_raw_command(self, cmd : str) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
            tcp_sock.connect((self.host, self.port))
            tcp_sock.send(self._encrypt(cmd))
            size_data = tcp_sock.recv(4)
            size = self._get_size(size_data)
            assert(0 <= size < 2**16)
            data = b''
            while size > 0:
                buff = tcp_sock.recv(size)
                if buff:
                    size -= len(buff)
                    data += buff
        return self._decrypt(data)

    def _send_json_command(self, cmd : str):
        js = json.dumps(cmd)
        data = self._send_raw_command(js)
        return json.loads(data)

    def _send_command(self, topic, cmd, arg=None):
        struct = {topic: {cmd: arg}}
        js = self._send_json_command(struct)
        return js[topic][cmd]

    @staticmethod
    def _encrypt(string : str) -> bytes:
        bytea = bytes(string, 'UTF-8')
        key = 171
        result = pack('>I', len(string))
        for i in bytea:
            a = key ^ i
            key = a
            result += bytes([a])
        return result

    @staticmethod
    def _get_size(data : bytes) -> int:
        return unpack('>I', data)[0]

    @staticmethod
    def _decrypt(data : bytes) -> str:
        key = 171
        result = b""
        for i in data:
            a = key ^ i
            key = i
            result += bytes([a])
        string = str(result, 'ascii')
        return string

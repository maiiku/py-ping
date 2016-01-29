import time
import random
import select
import socket


class Ping(object):
    def __init__(self, host, c=1, timeout=1, logger='print'):
        self.host = host
        self.timeout = timeout
        self.logger = logger
        self.conn = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
        )
        while c:
            if str(c).isdigit():
                c -= 1
            if c < 0:
                break
            try:
                self.result, msg = self.ping()
            except socket.error:
                msg = 'Unknown host: {}'.format(self.host)
                time.sleep(self.timeout)
            self.log(msg)
        try:
            self.conn.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self.conn.close()

    def _chksum(self, data):
        chksum = sum(
            ord(a) + ord(b) * 256
            for a, b in zip(data[::2], data[1::2] + b'\x00')
        ) & 0xFFFFFFFF
        chksum = (chksum >> 16) + (chksum & 0xFFFF)
        chksum = (chksum >> 16) + (chksum & 0xFFFF)
        chksum = '%x' % (~chksum & 0xFFFF)
        return ('0'*(len(chksum) % 2) + chksum).decode('hex')[::-1]

    def log(self, msg):
        if self.logger == 'print':
            print msg
        else:
            self.logger(msg)

    def ping(self):
        success = False
        msg = 'Request timed out for {}'.format(self.host)
        rstr = '%x' % random.randrange(0, 65536)
        payload = ('0'*(len(rstr) % 2) + rstr).decode('hex') + b'\x01\x00'
        packet = b'\x08\x00' + b'\x00\x00' + payload
        packet = b'\x08\x00' + self._chksum(packet) + payload
        self.conn.connect((self.host, 80))
        self.conn.sendall(packet)
        start = time.time()

        while select.select(
            [self.conn], [], [], max(0, start + self.timeout - time.time())
        )[0]:
            packet = self.conn.recv(1024)[20:]
            unchecked = packet[:2] + b'\0\0' + packet[4:]

            if packet == b'\0\0' + self._chksum(unchecked) + payload:
                success = True
                msg = "ping {}: {}".format(self.host, time.time() - start)
        return success, msg

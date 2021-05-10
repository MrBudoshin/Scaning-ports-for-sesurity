import socket
import threading
from netaddr import *
import argparse
import queue


class Scaning(threading.Thread):

    def __init__(self, get_ip, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_ip = get_ip
        self.ports = [21, 22, 23, 25, 38, 43, 80, 109, 110, 115, 118, 119, 143,
                      194, 220, 443, 540, 585, 591, 1112, 1433, 1443, 3128, 3197,
                      3306, 4000, 4333, 5100, 5432, 6669, 8000, 8080, 9014, 9200]
        self.scan_ip = queue.Queue()

    def port_scan(self, using_port, using_host):
        """создаем сокет"""
        socket_run = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_run.settimeout(1)

        try:
            """соденяемся с хостом выводим ответ если есть соеденение"""
            connections = socket_run.connect_ex((using_host, using_port))
            print(using_host, 'Port:', using_port, "Open")
            connections.close()
        except:
            """заглушка закрытых портов"""
            pass

    def scaning(self):

        ip_start, ip_end = self.get_ip.split("-")
        ip_range = IPRange(ip_start, ip_end)

        for ip_adr in ip_range:
            for port in self.ports:
                host = str(ip_adr)
                threads_scan = threading.Thread(target=self.port_scan, args=(port, host))
                threads_scan.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='[опции]\nДля вызова помощи:-h')
    parser.add_argument('-ip', type=str, help='spec target host')
    args = parser.parse_args('-ip  87.248.98.6-87.248.98.8'.split())
    scan = Scaning(get_ip=args.ip)
    scan.scaning()

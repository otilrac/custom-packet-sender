from scapy.all import *
import argparse
import re
import ipaddress
import os

class CustomPackage(object):
    def __init__(self, **kwargs):
        self.__destination_addr = None
        self.__source_addr = None
        self.__count = None
        self.__initial_ip_address(**kwargs)

    def _set_destination_addr(self, destination_addr):
        self.__destination_addr = destination_addr

    def _set_source_addr(self, source_addr):
        self.__source_addr = source_addr

    def _get_destination_addr(self):
        return self.__destination_addr

    def _get_source_addr(self):
        return self.__source_addr
    
    def __is_valid_ip_address(self, ip_address) -> bool:
        temp_ip = None
        try:
            temp_ip = ipaddress.ip_address(ip_address)
            if temp_ip.is_global is False:
                print('{ip} is not a global IP!'.format(ip=ip_address))
            return temp_ip.is_global
        except ValueError as ex:
            return False

    def __get_valid_ip(self, msg='Enter IP: '):
        temp_ip = None
        while True:
            temp_ip = input(msg)
            if self.__is_valid_ip_address(temp_ip) is True:
                return ipaddress.ip_address(temp_ip)

    def __initial_source_ip_control(self, source_addr):
        if self.__is_valid_ip_address(source_addr) is not True:
            self.__source_addr = self.__get_valid_ip('Enter source IP: ')
        else:
            self.__source_addr = source_addr

    def __initial_destination_ip_control(self, destination_addr):
        if self.__is_valid_ip_address(destination_addr) is not True:
            self.__destination_addr = self.__get_valid_ip('Enter destination IP: ')
        else:
            self.__destination_addr = destination_addr

    def __initial_ip_address(self, SOURCE=None, DESTINATION=None, COUNT=1):
        self.__initial_source_ip_control(SOURCE)
        self.__initial_destination_ip_control(DESTINATION)
        self.__initial_count(COUNT)

    def _set_count(self, count):
        self.__count = count

    def __initial_count(self, count):
        if count < 1:
            self._set_count(1)
        else:
            self._set_count(count)

    def __get_ip(self):
        return IP(src=str(self._get_source_addr()), dst=str(self._get_destination_addr()))

    def __get_tcp(self, sport=80, dport=80):
        return TCP(sport=sport, dport=dport)

    def _get_packet(self):
        return self.__get_ip()/self.__get_tcp()
    
    def _get_count(self):
        return self.__count

    def send(self):
        packet = self._get_packet()
        print(self._get_count())
        for i in range(0, self._get_count()):
            send(packet)

def admin_control():
    if os.getuid() != 0:
        print('Please run as root!')
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--destination', '-d', dest='DESTINATION', action='store', default=None, type=str, help='Destination IP Address')
    parser.add_argument('--source', '-s', dest='SOURCE', action='store', default=None, type=str, help='Source IP Address')
    parser.add_argument('--count', '-c', dest='COUNT', action='store', default=1, type=int, help='Send packet {COUNT} times')

    args = parser.parse_args()
    info = dict(args._get_kwargs())
    admin_control()

    package = CustomPackage(**info)
    package.send()

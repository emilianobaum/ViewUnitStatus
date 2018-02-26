#!/usr/bin/python3
#-*- coding utf-8 -*-

import socket

def retrieve_unit_status():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 10405))
    s.send(b'0\n')
    data = s.recv(1024)
    print("DATA: ",data)
    s.close()
    return data

def restart_docker_container():
    print("Restart process.")

def show_service_status():
    print("Show status.")
    
print("retrieve_unit_status: ",retrieve_unit_status())
#!/usr/bin/env python

try:
	import socket
	from queue import Queue
	import threading
	import time
	import optparse

except:
	print("install librarys to use the script")

def getArg():
	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", dest="target", help="target IP/ IP range")
	(options, arg) = parser.parse_args()
	return options


optns = getArg()
queue =Queue()
open_ports = []


def scan(port):
	'''
	creat a socket and try to make connection with target ip
	'''
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((optns.target, port))
		return True

	except:
		return False

def fill_queque(port_list):
	'''
	fill the queue, (put all ports in stack)
	'''
	for port in port_list:
		queue.put(port)

def worker():
	'''
	scan an IP or a Host for get all open ports
	'''
	while not queue.empty():
		port = queue.get()
		if scan(port):
			service = socket.getservbyport(port)

			print(f"[+] port {port} is open! ---service {service}")
			open_ports.append(port)

def final_port_scan():
	port_list = range(70, 100)
	fill_queque(port_list)

	thread_list = []

	for t in range(50):
		thread = threading.Thread(target=worker)
		thread_list.append(thread)

	for thread in thread_list:
		thread.start()

	for thread in thread_list:
		thread.join()

	print("open ports are: ", open_ports)

final_port_scan()


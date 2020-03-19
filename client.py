# -*- coding: utf-8 -*-
# Owner: lipenghui@corp.netease.com

import time
import json
import random
import socket

RECV_SIZE = 2048
PORT = 12345

g_msg = {}
g_socket = socket.socket()
try:
	g_socket.connect(('127.0.0.1', PORT))
except socket.error:
	print "connect server error..."

def _get_time():
	return int(time.time() * 1000)

def update_msg(msg):
	g_msg.update(msg)

def send_data():
	try:
		send_msg = json.dumps(g_msg)
		# print send_msg
		g_socket.send(send_msg)
	except socket.error:
		pass
		# print "socket send error"
	g_msg.clear()

_init_time = _get_time()

while True:
	update_msg({"ch1": [_get_time() - _init_time, random.random()], })
	update_msg({"ch2": [_get_time() - _init_time, random.random()], })
	send_data()
	time.sleep(0.01)

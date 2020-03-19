# -*- coding: utf-8 -*-
# Owner: lipenghui@corp.netease.com

import json
import cPickle
import time
import socket
import select

RECV_SIZE = 2048
PORT = 12345

g_listeners = []
g_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
g_socket.setblocking(False)
g_socket.bind(("", PORT))
g_socket.listen(5)
g_listeners.append(g_socket)


def recv_data():
	ret = {}
	r_list, _, e_list = select.select(g_listeners, [], g_listeners, 0.01)
	for rs in r_list:
		if rs == g_socket:
			conn, addr = rs.accept()
			g_listeners.append(conn)
			print "new connect", addr
		else:
			try:
				dat = rs.recv(RECV_SIZE)
			except socket.error:
				dat = None
			if not dat:
				rs.close()
				g_listeners.remove(rs)
			else:
				dat = cPickle.loads(dat)
				ret.update(dat)
				# print "recv len=%4d, data=%s" % (len(dat), dat)
	for es in e_list:
		import traceback
		traceback.print_stack()
		print "error!", es
	return ret


if __name__ == "__main__":
	while True:
		recv_data()
		time.sleep(0.01)

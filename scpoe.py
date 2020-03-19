# -*- coding: utf-8 -*-
# Owner: lipenghui@corp.netease.com

import time
import weakref
import matplotlib.pyplot as plt
import probe_socket

COLOR_MAP = {
	0: "blue",
	1: "green",
	2: "red",
	3: "black",
	4: "cyan",
}

class Axis(object):
	def __init__(self, scope, axes_idx, channel, name):
		self._owner = weakref.proxy(scope)
		self._axes_idx = axes_idx
		self._channel = channel
		self._name = name
		self._x = []
		self._y = []
		self._idle = 0

	def append(self, x, y):
		self._x.append(x)
		self._y.append(y)

	def draw(self):
		axes = self._owner.get_axes(self._axes_idx)
		axes.plot(self._x[-2:], self._y[-2:], color=COLOR_MAP[self._channel])

	def get_name(self):
		return self._name

class Scope(object):
	def __init__(self, figure):
		self._init_time = time.time()
		self._figure = figure
		self._figure.suptitle("scope")
		self._axeses = [self._figure.add_subplot(111)]
		self._axises = {}

	def get_axes(self, idx):
		return self._axeses[idx]

	def gen_axes(self, alone=0):
		if not alone:
			return 0
		self._figure.clf()
		num = len(self._axeses)
		for i in xrange(num):
			self._axeses[i] = self._figure.add_subplot(int("%d%d%d" % (num + 1, 1, i + 1)))
		self._axeses.append(self._figure.add_subplot(int("%d%d%d" % (num + 1, 1, num + 1))))
		return num

	def append(self, datas):
		t = time.time() - self._init_time
		for ch, v in datas.iteritems():
			axis = self._axises.setdefault(ch, Axis(self, self.gen_axes(), len(self._axises), ch))
			axis.append(t, v)

	def draw(self):
		for axis in self._axises.itervalues():
			axis.draw()
		end_time = time.time() - self._init_time
		self._axeses[0].set_xlim(max(0, end_time - 6), end_time)

plt.ion()
scope = Scope(plt.figure())

if __name__ == "__main__":
	while True:
		data = probe_socket.recv_data()

		scope.append(data)

		scope.draw()

		plt.draw()
		plt.pause(0.001)


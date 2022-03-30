import random

import networkx as nx
import matplotlib.pyplot as plt


class Infra:

	def __init__(self, file):
		self._nodes = {}
		self._links = {}
		self._file = file

	def add_node(self, node, sw, hw, sec, things):
		if node not in self._nodes:
			if node == "smartphone0":
				things = ["wht42", "loc38"]
			elif node == "smartphone1":
				things = ["accell20"]
			elif node == "accesspoint0":
				things = ["video3", "relay4"]
			self._nodes[node] = (sw, hw, sec, things)

	def add_link(self, node1, node2, lat, bw):
		if node1 in self._nodes and node2 in self._nodes and node1 != node2 and (node1, node2) not in self._links:
			self._links[(node1, node2)] = (lat, bw)

	def modify_node(self, node, sw, hw, sec, things):
		if node in self._nodes:
			self._nodes[node] = (sw, hw, sec, things)

	def modify_link(self, node1, node2, lat, bw):
		if (node1, node2) in self._links:
			self._links[(node1, node2)] = (lat, bw)

	def remove_node(self, node):
		if node in self._nodes:
			del self._nodes[node]
			for (n1, n2) in self._links.copy():
				if n1 == node or n2 == node:
					self.remove_link(n1, n2)

	def remove_link(self, node1, node2):
		if (node1, node2) in self._links:
			del self._links[(node1, node2)]

	def get_node(self, node):
		if node in self._nodes:
			(sw, hw, sec, things) = self._nodes[node]
			return "node({}, {}, {}, {}, {}).".format(node, str(sw), str(hw), str(sec), str(things)).replace("'", "")
		return ""

	def get_link(self, node1, node2):
		if (node1, node2) in self._links:
			(lat, bw) = self._links[(node1, node2)]
			return "link({}, {}, {}, {}).".format(node1, node2, str(lat), str(bw)).replace("'", "")
		return ""

	def add_nodes(self, basename, number, sw, hw, sec, things):
		nodes = []
		for i in range(number):
			name = basename + str(i)
			self.add_node(name, sw, hw, sec, things)
			nodes.append(name)
		return nodes

	def add_links(self, nodes1, nodes2, lat, bw):
		for n1 in nodes1:
			for n2 in nodes2:
				if n1 != n2:
					self.add_link(n1, n2, lat, bw)

	def modify_links(self, nodes1, nodes2, lat, bw):
		for n1 in nodes1:
			for n2 in nodes2:
				if n1 != n2:
					self.modify_link(n1, n2, lat, bw)

	def __str__(self):
		infra = ""
		for n in self._nodes:
			infra += self.get_node(n) + "\n"
		infra += "\n"
		for (n1, n2) in self._links:
			infra += self.get_link(n1, n2) + "\n"
		infra += "\n"
		return infra

	def upload(self, file=None):
		if file is None:
			file = self._file
		with open(file, "w") as f:
			appendix = "bwTh(20).\n" \
			           "dataBinding(interface, rAcc, accell20).\n" \
			           "dataBinding(interface, rVid, video3).\n" \
			           "dataBinding(dataStorage, rLoc, loc38).\n" \
			           "dataBinding(dataStorage, rWht, wht42).\n" \
			           "dataBinding(shadersController, rRly, relay4).\n" \
			           "\nsensor(wht42, temperature, [weather]).\n" \
			           "sensor(loc38, smartphone, [location, accelerometer]).\n" \
			           "sensor(accell20, smartphone, [accelerometer]).\n" \
			           "actuator(video3, display).\n" \
			           "actuator(relay4, relay).\n\n"
			f.write(appendix)
			f.write(str(self))


def main(i=4):
	n_nodes = 2 ** i
	infra = Infra("infra/infra_{}.pl".format(n_nodes))
	g = nx.barabasi_albert_graph(n=n_nodes, m=i)

	# number of cloud nodes
	CLOUDS = round(n_nodes * 0.05)

	labels = {}
	for n in range(CLOUDS):
		labels[n] = "cloud{}".format(n)

	ISPS = 0
	CABINETS = 0
	ACCESSPOINTS = 0
	SMARTPHONES = 0

	for n in list(g.nodes)[CLOUDS:]:
		if random.random() < 0.15:  # ISPS
			lbl = "isp{}".format(ISPS)
			ISPS += 1
		elif random.random() < 0.2:  # CABINETS
			lbl = "cabinet{}".format(CABINETS)
			CABINETS += 1
		elif random.random() < 0.25:  # ACCESS POINTS
			lbl = "accesspoint{}".format(ACCESSPOINTS)
			ACCESSPOINTS += 1
		else:  # SMARTPHONES
			lbl = "smartphone{}".format(SMARTPHONES)
			SMARTPHONES += 1

		labels[n] = lbl
	g = nx.relabel_nodes(g, labels, copy=False)

	smartphones = infra.add_nodes("smartphone", SMARTPHONES, ["ubuntu", "python"], (2.4, 4, 32), ["encryption", "auth"], [])
	accesspoints = infra.add_nodes("accesspoint", ACCESSPOINTS, ["ubuntu", "mySQL"], (3, 6, 128), ["encryption", "auth"], [])
	cabinets = infra.add_nodes("cabinet", CABINETS, ["python", "mySQL"], (4, 8, 256), ["encryption", "auth"], [])
	isps = infra.add_nodes("isp", ISPS, ["ubuntu", "mySQL", "python"], (5, 16, 512), ["encryption", "auth"], [])
	clouds = infra.add_nodes("cloud", CLOUDS, ["ubuntu", "mySQL", "python"], (100, 64, 800), ["encryption", "auth"], [])

	for (s, t) in g.edges:
		infra.add_link(s, t, 5, 1000)
		infra.add_link(t, s, 5, 1000)

	# comment lines 154-182 to use "dummy" links, with 5ms latency and 1000Mbps bandwidth

	infra.modify_links(clouds, clouds, 20, 1000)
	infra.modify_links(clouds, isps, 110, 1000)
	infra.modify_links(clouds, cabinets, 135, 100)
	infra.modify_links(clouds, accesspoints, 100, 50)
	infra.modify_links(clouds, smartphones, 150, 40)

	infra.modify_links(isps, clouds, 110, 1000)
	infra.modify_links(isps, isps, 20, 1000)
	infra.modify_links(isps, cabinets, 25, 500)
	infra.modify_links(isps, accesspoints, 38, 50)
	infra.modify_links(isps, smartphones, 20, 1000)

	infra.modify_links(cabinets, clouds, 135, 100)
	infra.modify_links(cabinets, isps, 25, 500)
	infra.modify_links(cabinets, cabinets, 20, 1000)
	infra.modify_links(cabinets, accesspoints, 13, 50)
	infra.modify_links(cabinets, smartphones, 15, 35)

	infra.modify_links(accesspoints, clouds, 100, 50)
	infra.modify_links(accesspoints, isps, 38, 4)
	infra.modify_links(accesspoints, cabinets, 13, 4)
	infra.modify_links(accesspoints, accesspoints, 10, 50)
	infra.modify_links(accesspoints, smartphones, 2, 70)

	infra.modify_links(smartphones, clouds, 150, 40)
	infra.modify_links(smartphones, isps, 40, 2.5)
	infra.modify_links(smartphones, cabinets, 15, 3)
	infra.modify_links(smartphones, accesspoints, 2, 70)
	infra.modify_links(smartphones, smartphones, 15, 50)

	infra.upload()
	print("Done for {}".format(n_nodes))


if __name__ == "__main__":
	main(i=4)

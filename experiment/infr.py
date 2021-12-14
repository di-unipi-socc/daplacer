import random
import networkx as nx


class Infra:

	def __init__(self, file):
		self._nodes = {}
		self._links = {}
		self._file = file

	def addNode(self, node, sw, hw, sec, things):
		if node not in self._nodes:
			if node == "smartphone0":
				things = ["wht42", "loc38"]
			elif node == "smartphone1":
				things = ["accell20"]
			elif node == "accesspoint0":
				things = ["video3", "relay4"]
			self._nodes[node] = (sw, hw, sec, things)

	def addLink(self, node1, node2, lat, bw):
		if node1 in self._nodes and node2 in self._nodes and node1 != node2 and (node1, node2) not in self._links:
			self._links[(node1, node2)] = (lat, bw)

	def modifyNode(self, node, sw, hw, sec, things):
		if node in self._nodes:
			self._nodes[node] = (sw, hw, sec, things)

	def modifyLink(self, node1, node2, lat, bw):
		if (node1, node2) in self._links:
			self._links[(node1, node2)] = (lat, bw)

	def removeNode(self, node):
		if node in self._nodes:
			del self._nodes[node]
			for (n1, n2) in self._links.copy():
				if n1 == node or n2 == node:
					self.removeLink(n1, n2)

	def removeLink(self, node1, node2):
		if (node1, node2) in self._links:
			del self._links[(node1, node2)]

	def getNode(self, node):
		if node in self._nodes:
			(sw, hw, sec, things) = self._nodes[node]
			return ("node(" + node + ", " + str(sw) + ", " + str(hw) + ", " + str(sec) + ", "
			        + str(things) + ").").replace("'", "")
		return ""

	def getLink(self, node1, node2):
		if (node1, node2) in self._links:
			(lat, bw) = self._links[(node1, node2)]
			return ("link(" + node1 + ", " + node2 + ", " + str(lat) + ", " + str(bw) + ").").replace("'", "")
		return ""

	def addNodes(self, basename, number, sw, hw, sec, things):
		nodes = []
		for i in range(number):
			name = basename + str(i)
			self.addNode(name, sw, hw, sec, things)
			nodes.append(name)
		return nodes

	def addLinks(self, nodes1, nodes2, lat, bw):
		for n1 in nodes1:
			for n2 in nodes2:
				if n1 != n2:
					self.addLink(n1, n2, lat, bw)

	def __str__(self):
		infra = ""
		for n in self._nodes:
			infra += self.getNode(n) + "\n"
		infra += "\n"
		for (n1, n2) in self._links:
			infra += self.getLink(n1, n2) + "\n"
		infra += "\n"
		return infra

	def upload(self, file=None):
		if file is None:
			file = self._file
		with open(file, "w") as f:
			appendix = "bwTh(100).\n" \
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
	nodesnumber = 2 ** i
	infra = Infra("infra/infra_{}.pl".format(nodesnumber))
	g = nx.barabasi_albert_graph(n=nodesnumber, m=i)
	# number of cloud nodes
	CLOUDS = round(nodesnumber * 0.05)
	labels = {}
	for n in range(CLOUDS):
		labels[n] = "cloud{}".format(n)

	ISPS = 0
	CABINETS = 0
	ACCESSPOINTS = 0
	SMARTPHONES = 0

	labels = {}
	for n in list(g.nodes):
		if random.random() < 0.15:  # ISPS
			l = "isp{}".format(ISPS)
			ISPS += 1
		elif random.random() < 0.2:  # CABINETS
			l = "cabinet{}".format(CABINETS)
			CABINETS += 1
		elif random.random() < 0.25:  # ACCESS POINTS
			l = "accesspoint{}".format(ACCESSPOINTS)
			ACCESSPOINTS += 1
		else:  # SMARTPHONES
			l = "smartphone{}".format(SMARTPHONES)
			SMARTPHONES += 1

		labels[n] = l
	g = nx.relabel_nodes(g, labels, copy=False)

	smartphones = infra.addNodes("smartphone", SMARTPHONES, ["ubuntu", "python"], (2.4, 4, 32),
	                             ["encryption", "auth"], [])
	accesspoints = infra.addNodes("accesspoint", ACCESSPOINTS, ["ubuntu", "mySQL"], (3, 6, 128), ["encryption", "auth"],
	                              [])
	cabinets = infra.addNodes("cabinet", CABINETS, ["python", "mySQL"], (4, 8, 512), ["encryption", "auth"], [])
	isps = infra.addNodes("isp", ISPS, ["ubuntu", "mySQL", "python"], (5, 16, 600), ["encryption", "auth"],
	                      [])
	clouds = infra.addNodes("cloud", CLOUDS, ["ubuntu", "mySQL", "python"], (100, 64, 10000), ["encryption", "auth"],
	                        [])

	for (s, t) in g.edges():
		infra.addLink(s, t, 5, 1000)
		infra.addLink(t, s, 5, 1000)

	infra.upload()
	print("Done for {}".format(nodesnumber))


if __name__ == "__main__":
	main(9)

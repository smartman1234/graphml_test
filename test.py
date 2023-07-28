import matplotlib.pyplot as plt
import networkx as nx
import csv

file = "libentry.csv"
node = 5
relation_num = 9

class Graph(object):
    def __init__(self, file):
        try:
            with open(file, encoding='shift-jis') as csvfile:
                csvdata = csv.reader(csvfile, dialect='excel')
                rawdata = [dict(), dict()]
                for linum, row in enumerate(csvdata):
                    if linum == 0:
                        continue
                    for rank, data in enumerate(row):
                        try:
                            rawdata[0][rank].append(data)
                        except KeyError:
                            rawdata[0][rank] = list()
                            rawdata[0][rank].append(data)
                        try:
                            rawdata[1][linum-1].append(data)
                        except KeyError:
                            rawdata[1][linum-1] = list()
                            rawdata[1][linum-1].append(data)
            self.rawdata = rawdata
        except IOError:
            sys.exit("File \'{0}\' open failed!\n".format(file) +
                     "Check if the file name is correct.\n")

    def createNodeList(self, column):
        nodes = dict()
        for data in self.rawdata[0][column]:
            if data != "":
                try:
                    nodes[data]["population"] += 1
                except KeyError:
                    nodes[data] = dict()
                    nodes[data]["population"] = 1
        return (column, nodes)

    def createEdgeList(self, nodes, relationships):
        edges = dict()
        for key, value in relationships.items():
            for i in range(len(self.rawdata[1])):
                start = self.rawdata[1][i]
                for j in range(len(self.rawdata[1])):
                    end = self.rawdata[1][j]
                    included = (start[nodes[0]] in nodes[1]) and \
                               (end[nodes[0]] in nodes[1])
                    related = (start[key] in value[1]) and \
                              (start[key] == end[key])
                    if i != j and related and included:
                        try:
                            edges[(start[nodes[0]],
                                  end[nodes[0]])]["weight"] += 1
                        except KeyError:
                            edges[(start[nodes[0]], end[nodes[0]])] = dict()
                            edges[(start[nodes[0]],
                                  end[nodes[0]])]["weight"] = 1
        return edges

    def createGraph(self, nodes, edges):
        G = nx.Graph()
        # Add nodes to the graph.
        G.add_nodes_from(nodes[1])

        # Add attributes to nodes.
        for a in nodes[1].keys():
            for attr in nodes[1][a]:
                G.nodes[a][attr] = nodes[1][a][attr]
        # Add edges to the graph.
        G.add_edges_from(edges.keys())
        # Add attributes to edges.
        for a, b in edges.keys():
            for attr in edges[(a, b)]:
                G[a][b][attr] = edges[(a, b)][attr]
        return G



graphobj = Graph(file)

nodes = graphobj.createNodeList(node)
relation = graphobj.createNodeList(relation_num)

edges = graphobj.createEdgeList(nodes, {relation_num: relation})

print(nodes[1])
print(edges)

graph = graphobj.createGraph(nodes, edges)

nx.draw(graph)
nx.write_graphml(graph, "output.graphml")

print("Number of edges in graph: ", graph.number_of_edges())
plt.show()
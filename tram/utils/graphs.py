import networkx as nx
import graphviz    

class WeightedGraph(nx.Graph):

    def __init__(self, start=None):
        super().__init__(start)

    def __len__(self):
        return len(self.nodes())

    def add_vertex(self,vertex):
        self.add_node(vertex, value=None)

    def remove_vertex(self, vertex):
        self.remove_node(vertex)

    def neighbors(self, vertex):
        return iter(self.adj[vertex])

    def get_vertex_value(self, vertex):
        return self.nodes[vertex]

    def set_vertex_value(self, vertex, x):
        self.nodes[vertex]['value'] = x

    def vertices(self):
        return self.nodes()

    def add_edge(self, a, b):
        super().add_edge(a, b)
        self.set_weight(a, b, 1)

    def set_weight(self, a, b, w):
        self[a][b]['weight'] = w

    def get_weight(self, a, b):
        try:
            return self[a][b]['weight']
        except KeyError:
            return 1

    def get_time(self, a, b):
        try:
            return self[a][b]["time"]
        except KeyError:
            return 1
  
    def get_distance(self, a, b):
        try:
            return self[a][b]["distance"]
        except KeyError:
            return 1

def dijkstra(graph, source, cost=lambda u,v: 1):
    costs2attributes(graph, cost)
    paths = {
        vertex: nx.shortest_path(graph, source=source, target=vertex, weight="weight") 
        for vertex in graph
    }
    return paths

def costs2attributes(G, cost, attr='weight'):
    for a, b in G.edges():
        G[a][b][attr] = cost(a, b)


def visualize(graph, view='view', name='mygraph', nodecolors=None):
    dot = graphviz.Graph()
    for a in graph.vertices():
        if str(a) in nodecolors:
            dot.node(str(a), style="filled", color=nodecolors[str(a)])
        else:
            dot.node(str(a))
    for a, b in graph.edges():
        dot.edge(str(a), str(b), label=str(graph.get_weight(a,b)))
    dot.render(name, view=True)


def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]
    colormap = {str(v): 'orange' for v in path}
    visualize(G, view='view', nodecolors=colormap)

def demo():
    G = WeightedGraph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6),(3,7),(6,7)])
    view_shortest(G, 2, 6, G.get_weight)

if __name__ == '__main__':
    demo()
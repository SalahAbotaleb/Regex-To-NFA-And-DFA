from graph import Graph
from draw import Drawer

if __name__ == "__main__":
    g1 = Graph()
    node1 = g1.get_start()
    node2 = Node()
    node3 = Node()
    node2.is_terminal = 1
    node2.addEdge(node3, "xyz")
    node1.addEdge(node2, "a")
    print(g1.get_start())
    print(g1.get_terminals())
    print(g1.to_json())
    jsonG = g1.to_json()
    g2 = Graph(jsonG)
    print(g2.to_json())

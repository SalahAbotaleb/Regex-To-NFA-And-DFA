from graph import Graph
from draw import Drawer
from node import Node
from json_utils import JsonUtils

if __name__ == "__main__":
    # g1 = Graph()
    # node1 = g1.get_start()
    # node2 = Node()
    # node3 = Node()
    # node3.is_terminal = 1
    # node2.addEdge(node3, "xyz")
    # node1.addEdge(node2, "a")
    # node1.addEdge(node3, "abc")
    # print(g1.get_start())
    # print(g1.get_terminals())
    # print(g1.to_json())
    # jsonG = g1.to_json()
    # g2 = Graph(jsonG)
    # print(g2.to_json())
    # JsonUtils.save_dict_to_file(g2.to_json(), "data2.json")

    jsonG3 = JsonUtils.get_dict_from_file("data1.json")
    g3 = Graph(jsonG3)
    Drawer.save_finite_automaton(g3)

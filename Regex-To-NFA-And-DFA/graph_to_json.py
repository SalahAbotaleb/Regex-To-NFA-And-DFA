from graph import Graph
from node import Node
from json_utils import JsonUtils


class GraphToJson:
    def convert(graph: Graph) -> dict:
        return GraphToJson.__to_json__(graph)

    def __to_json__(graph: Graph) -> dict:
        json = {"startingState": str(graph.get_start().id)}
        json.update(GraphToJson.__get_json__(graph.get_start(), set()))
        return json

    def __get_json__(curr_node: Node, visited_nodes: set) -> dict:
        json = {}
        node_json_key = str(curr_node.id)
        node_json_value = curr_node.to_json()
        json.update({node_json_key: node_json_value})
        visited_nodes.add(curr_node)

        for edge in curr_node.edges:
            neighbor = edge.dest
            if neighbor not in visited_nodes:
                json.update(GraphToJson.__get_json__(neighbor, visited_nodes))
        return json

    def convert_and_dump(graph: Graph, file_name: str) -> dict:
        json = GraphToJson.convert(graph)
        JsonUtils.save_dict_to_file(json, file_name)


if __name__ == "__main__":
    g1 = Graph()
    node1 = g1.get_start()
    node2 = Node()
    node3 = Node()
    node2.is_terminal = 1
    node2.add_edge(node3, "xyz")
    node1.add_edge(node2, "a")
    print(GraphToJson.convert(g1))
    GraphToJson.convert_and_dump(g1, "dataTest.json")

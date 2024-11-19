from graphviz import Digraph
import os


class Drawer:
    def __init__(self):
        self.node_idx = 0

    def save_finite_automaton(self, graph: "Graph", name="automaton", format="png"):
        digraph = Digraph(name=name, format=format)
        digraph.attr(rankdir='LR')
        edges = self.__dfs_to_create_automaton__(
            graph.get_start(), set(), digraph)
        for edge in edges:
            digraph.edge(edge[0], edge[1], label=edge[2])
        digraph.render(name)
        self.__remove_intermediate_files__(name)

    def __dfs_to_create_automaton__(self, curr_node: "Node", vis_nodes: set, digraph: Digraph) -> list[tuple]:
        if curr_node.id in vis_nodes:
            return []

        vis_nodes.add(curr_node.id)
        digraph.node(curr_node.id, label=f"S{self.node_idx}",
                     color="black", shape=self.__get__shape__(curr_node))
        self.node_idx = self.node_idx+1
        edges: list[tuple] = []
        for edge in curr_node.edges:
            dest = edge.dest
            action = edge.action
            next_edges = self.__dfs_to_create_automaton__(
                dest, vis_nodes, digraph)
            edges.append((curr_node.id, dest.id, action))

            if len(next_edges) > 0:
                edges.extend(next_edges)
        return edges

    def __get__shape__(self, node: "Node"):
        return "doublecircle" if node.is_terminal else "circle"

    def __remove_intermediate_files__(self, output_file):
        if os.path.exists(output_file):
            os.remove(output_file)

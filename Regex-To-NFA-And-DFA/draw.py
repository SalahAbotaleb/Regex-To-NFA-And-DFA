from graphviz import Digraph


class Drawer:
    def save_finite_automaton(graph: "Graph", name="automaton", format="png"):
        digraph = Digraph(name=name, format=format)
        Drawer.__dfs_to_create_automaton__(graph.get_start(), set(), digraph)

    def __dfs_to_create_automaton__(curr_node: "Node", vis_nodes: set, digraph: Digraph):
        if curr_node in vis_nodes:
            return

        vis_nodes.add(curr_node.id)
        digraph.node(curr_node.id, label=curr_node.id,
                     color="black", shape=Drawer.__get__shape__(curr_node))

        for edge in node.edges:
            dest = edge.dest
            action = edge.action
            Drawer.__dfs_to_create_automaton__(dest, vis_nodes, digraph)
            digraph.edge(curr_node.id, dest.id, label=action)

    def __get__shape__(node: "Node"):
        return "doublecircle" if node.is_terminal else "circle"

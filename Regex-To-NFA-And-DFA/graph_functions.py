from graph import Graph
from node import Node
import constants
from draw import Drawer

# operations available on graphs or | concatenation # one or more + zero or more * optional ? character class . a b etc ... ranges ie. a-c
def str_to_graph(char: str) -> Graph:
    '''
    Returns a new graph that is the result of the input character or list of characters.
    '''
    final_graph = Graph()
    start = Node()
    start.set_is_start(True)
    terminal = Node()
    terminal.set_is_terminal(True)
    start.add_edge(terminal, char)
    final_graph.start = start

    return final_graph

def or_graphs(graph1: Graph, graph2: Graph) -> Graph:
    '''
    Returns a new graph that is the result of the or operation between the two input graphs.
    '''
    final_graph = Graph()
    final_graph.start.add_edge(graph1.get_start(), constants.GraphTerm.EPSILON_ACTION)
    graph1.get_start().set_is_start(False)
    final_graph.start.add_edge(graph2.get_start(), constants.GraphTerm.EPSILON_ACTION)
    graph2.get_start().set_is_start(False)
    terminal_node = Node()
    terminal_node.set_is_terminal(True)
    terminal = graph1.get_terminals()[0]
    terminal.add_edge(terminal_node, constants.GraphTerm.EPSILON_ACTION)
    terminal.set_is_terminal(False)
    terminal = graph2.get_terminals()[0]
    terminal.add_edge(terminal_node, constants.GraphTerm.EPSILON_ACTION)
    terminal.set_is_terminal(False)

    return final_graph

def concat_graphs(graph1: Graph, graph2: Graph) -> Graph:
    '''
    Returns a new graph that is the result of the concatenation operation between the two input graphs. graph1 -> graph2
    '''
    final_graph = Graph()
    final_graph.start = graph1.get_start()
    terminal = graph1.get_terminals()[0]
    terminal.add_edge(graph2.get_start(), constants.GraphTerm.EPSILON_ACTION)
    terminal.set_is_terminal(False)


    return final_graph

def one_or_more(graph: Graph) -> Graph:
    '''
    Returns a new graph that is the result of the one or more operation on the input graph.
    '''
    final_graph = Graph()
    final_graph.start.add_edge(graph.get_start(), constants.GraphTerm.EPSILON_ACTION)
    graph.get_start().set_is_start(False)
    graph_terminal = Node()
    graph_terminal.set_is_terminal(True)
    terminal = graph.get_terminals()[0]
    terminal.add_edge(graph_terminal, constants.GraphTerm.EPSILON_ACTION)
    terminal.add_edge(final_graph.get_start(), constants.GraphTerm.EPSILON_ACTION)
    terminal.set_is_terminal(False)

    return final_graph

def zero_or_more(graph: Graph) -> Graph:
    '''
    Returns a new graph that is the result of the zero or more operation on the input graph.
    '''
    final_graph = Graph()
    final_graph.start.add_edge(graph.get_start(), constants.GraphTerm.EPSILON_ACTION)
    graph.get_start().set_is_start(False)
    graph_terminal = Node()
    graph_terminal.set_is_terminal(True)
    terminal = graph.get_terminals()[0]
    terminal.add_edge(graph_terminal, constants.GraphTerm.EPSILON_ACTION)
    terminal.add_edge(final_graph.get_start(), constants.GraphTerm.EPSILON_ACTION)
    terminal.set_is_terminal(False)
    final_graph.start.add_edge(graph_terminal, constants.GraphTerm.EPSILON_ACTION)

    return final_graph

def optional(graph: Graph) -> Graph:
    '''
    Returns a new graph that is the result of the optional operation on the input graph.
    '''
    final_graph = Graph()
    final_graph.start.add_edge(graph.get_start(), constants.GraphTerm.EPSILON_ACTION)
    graph.get_start().set_is_start(False)
    graph_terminal = Node()
    graph_terminal.set_is_terminal(True)
    terminal = graph.get_terminals()[0]
    terminal.add_edge(graph_terminal, constants.GraphTerm.EPSILON_ACTION)
    terminal.set_is_terminal(False)
    final_graph.start.add_edge(graph_terminal, constants.GraphTerm.EPSILON_ACTION)

    return final_graph

if __name__ == "__main__":

    g1 = str_to_graph("a")
    print(g1.to_json())
    Drawer.save_finite_automaton(g1, "g1 a")

    g2 = str_to_graph("b")
    Drawer.save_finite_automaton(g2, "g2 b")

    g3 = or_graphs(g1, g2)
    Drawer.save_finite_automaton(g3, "g3 a(or)b")

    g4 = str_to_graph("c")
    Drawer.save_finite_automaton(g4, "g4 c")

    g5 = str_to_graph("d")
    Drawer.save_finite_automaton(g5, "g5 d")

    g6 = concat_graphs(g4, g5)
    Drawer.save_finite_automaton(g6, "g6 c(and)d")
    
    g7 = str_to_graph("a-g")
    Drawer.save_finite_automaton(g7, "g7 [a-g]")

    g8 = one_or_more(g7)
    Drawer.save_finite_automaton(g8, "g8 [a-g]+")
    
    g9 = str_to_graph("1")
    Drawer.save_finite_automaton(g9, "g9 1")

    g10 = zero_or_more(g9)
    Drawer.save_finite_automaton(g10, "g10 1(ZeroOrMore)")

    g11 = str_to_graph("A-D")
    Drawer.save_finite_automaton(g11, "g11 [A-D]")

    g12 = optional(g11)
    Drawer.save_finite_automaton(g12, "g12 [A-D](Optional)")


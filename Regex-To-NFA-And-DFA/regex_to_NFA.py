
from graph_functions import *
from infix_to_postfix import infix_to_postfix
from draw import Drawer
def regex_to_NFA(regex: str) -> Graph:
    '''
    Returns a new graph that is the result of the regex to NFA operation on the input regex.
    '''
    postfix = infix_to_postfix(regex)
    if not postfix[0]:
        return postfix[1]
    stack = []
    for char in postfix[1]:
        if char == '|':
            graph2 = stack.pop()
            graph1 = stack.pop()
            stack.append(or_graphs(graph1, graph2))
        elif char == '#':
            graph2 = stack.pop()
            graph1 = stack.pop()
            stack.append(concat_graphs(graph1, graph2))
        elif char == '+':
            graph = stack.pop()
            stack.append(one_or_more(graph))
        elif char == '*':
            graph = stack.pop()
            stack.append(zero_or_more(graph))
        elif char == '?':
            graph = stack.pop()
            stack.append(optional(graph))
        else:
            stack.append(str_to_graph(char))
    return stack.pop()


if __name__ == '__main__':
    regex = "a*?"
    graph = regex_to_NFA(regex)
    if  isinstance(graph,Graph):
        Drawer.save_finite_automaton(graph, "regex ")
    else:
        print(graph)

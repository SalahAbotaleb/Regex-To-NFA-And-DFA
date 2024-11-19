from graph import Graph
from draw import Drawer
from node import Node
from json_utils import JsonUtils
import os
import shutil
from pathlib import Path
from regex_to_NFA import *
from graph_to_json import GraphToJson
from NFA_to_DFA import NFAToDFA
from DFA_minimizer import DFAMinimizer

if __name__ == "__main__":
    patterns = [
        "[A-Za-z]+[0-9]*"
    ]
    testcase = 0
    for pattern in patterns:
        path = Path(f"test{testcase}")
        if os.path.exists(path):
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        os.chdir(path)
        nfa_graph = regex_to_NFA(pattern)
        GraphToJson.convert_and_dump(nfa_graph, "nfa.json")
        Drawer.save_finite_automaton(nfa_graph, "nfa")
        dfa_graph = NFAToDFA(nfa_graph).convert()
        dfa_minimizer = DFAMinimizer(dfa_graph)
        min_dfa_graph = dfa_minimizer.minimize()
        GraphToJson.convert_and_dump(min_dfa_graph, "dfa.json")
        Drawer.save_finite_automaton(min_dfa_graph, "dfa")

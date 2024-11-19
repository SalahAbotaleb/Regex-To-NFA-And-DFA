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
        "[A-Za-z]+[0-9]*",
        "((a(b*))c)",
        "((ab)|(ba))*",
        "(a|b)*abb",
        "-?[0-9]+",
        "ab(b|c)*d+",
        "[a-zA-Z_$][a-zA-Z0-9_$]*",
        "0|([1-9A-F][0-9A-F]*)|([1-9a-f][0-9a-f]*)",
        "[1-9]|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5])",
        "[a-zA-Z49][a-zA-Z0-994]*",
        "https?(www.)?[a-zA-Z0-9].((com)|(org)|(net))",
        "https?(www.)?[a-zA-Z0-9-].((com)|(org)|(net))"
    ]
    testcase = 0
    for pattern in patterns:
        path = Path(f"test{testcase}")
        print(f"=======================test{testcase}========================")
        if os.path.exists(path):
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        os.chdir(path)
        try:
            with open("pattern.txt", "w") as file:
                file.write(pattern)
            nfa_graph = regex_to_NFA(pattern)
            GraphToJson.convert_and_dump(nfa_graph, "nfa.json")
            Drawer().save_finite_automaton(nfa_graph, "nfa")
            dfa_graph = NFAToDFA(nfa_graph).convert()
            dfa_minimizer = DFAMinimizer(dfa_graph)
            min_dfa_graph = dfa_minimizer.minimize()
            GraphToJson.convert_and_dump(min_dfa_graph, "dfa.json")
            Drawer().save_finite_automaton(min_dfa_graph, "dfa")
        except ValueError as e:
            print("Caught an error:", e)
        os.chdir(os.pardir)
        testcase = testcase+1

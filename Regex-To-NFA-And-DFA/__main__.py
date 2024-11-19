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
        # "[A-Za-z]+[0-9]*",
        # "((a(b*))c)",
        # "((ab)|(ba))*",
        # "(a|b)*abb",
        # "-?[0-9]+",
        # "ab(b|c)*d+",
        # "[a-zA-Z_$][a-zA-Z0-9_$]*",
        # "0|([1-9A-F][0-9A-F]*)|([1-9a-f][0-9a-f]*)",
        # "[1-9]|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5])",
        # "[a-zA-Z49][a-zA-Z0-994]*",
        # "https?(www.)?[a-zA-Z0-9].((com)|(org)|(net))",
        # "https?(www.)?[a-zA-Z0-9-].((com)|(org)|(net))",
        # "([1-8)]",
        # "([1-8])",
        # "[1-8-9]",
        # "[1-89]",
        # "[1-8A-Za-f]",
        # "[1-a]",
        # "[1-9B-s]",
        # "[a-D]",
        # "[a-c]",
        # "[a-cA-C]",
        # "[c-caA-C0-9]",
        # "[c-a]",
        # "[c-B]",
        # "[c-]",
        # "[c-9]",
        # "[c-0]",
        # "[1-c]",
        # "[1]-",
        # "[132]?[a-c]",
        # "dsa?ds+c*fs",
        # "dsa?ds+c*+fs",
        # "aa**",
        # "aa+*",
        # "aa+?",
        # "aa*?",
        # "aa??",
        # "aa+?",
        # "(a*a?)?b",
        # "|a",
        # "a|",
        # "a|b|",
        # "a|b|(c[dsa]?(soc0[1-9]*)?)+n0+(lr*em)*",
        # "((((((((((a*)*)*)*)*)*)*)*)*)*)*",
        # "((((((((((a+)+)+)+)+)+)+)+)+))+",
        # "((((((((((a?)?)?)?)?)?)?)?)?)?)?",
        # "pas$word",
        # "unr3al",
        # "/s",
        # "(a*)",
        # "(a+)|",
        # "(a?|)",
        # "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)",
        # "(1|2|3|4|5|6|7|8|9|0)?s",
        # "(1|2|3|4|5|6|7|8|9|0)?s;",
        # "*",
        # "+",
        # "?",
        # "|",
        # ')AB(',
        # "A|",
        # "[Z-A]",
        # "AB",
        # "A|B",
        # "(AB|[A-Z])+[A-Z]*",
        # "(AB|C|[A-Z]S*)+ABC",
        # "(((AB)((A|B)*))(AB))",
        # "AB(A|B)*AB", "([A-Z])",
        # "([A-C][A-C]|A|ABCD*C+)[B-D]",
        # "(a|b)*abb",
        # "m?[0-9]+",
        # "((a|b|c)+9|55?(zzz)*)",
        "((a|b|c+v))"
    ]
    testcase = 0
    for pattern in patterns:
        path = Path(f"test{testcase}")
        print(f"=======================test{testcase}========================")
        print(f"test{testcase} regex: {pattern}")
        if os.path.exists(path):
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        os.chdir(path)
        try:
            with open("pattern.txt", "w") as file:
                file.write(pattern)
            nfa_graph = regex_to_NFA(pattern)
            nfa_graph.rename_nodes_ids()
            GraphToJson.convert_and_dump(nfa_graph, "nfa.json")
            Drawer.save_finite_automaton(nfa_graph, "nfa")
            dfa_graph = NFAToDFA(nfa_graph).convert()
            dfa_minimizer = DFAMinimizer(dfa_graph)
            min_dfa_graph = dfa_minimizer.minimize()
            min_dfa_graph.rename_nodes_ids()
            GraphToJson.convert_and_dump(min_dfa_graph, "dfa.json")
            Drawer.save_finite_automaton(min_dfa_graph, "dfa")
            print("PASS")
        except ValueError as e:
            print("FAIL")
            print("Caught an error:", e)
        os.chdir(os.pardir)
        testcase = testcase+1

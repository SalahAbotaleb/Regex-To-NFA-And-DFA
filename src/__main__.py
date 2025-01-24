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
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Convert regex to NFA and DFA")
    parser.add_argument("pattern", type=str,
                        help="The regex pattern to convert")
    parser.add_argument("--output_dir", type=str, default="output",
                        help="The directory to output the images")
    args = parser.parse_args()

    pattern = args.pattern
    output_dir = Path(args.output_dir)

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(output_dir)

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


if __name__ == "__main__":
    main()

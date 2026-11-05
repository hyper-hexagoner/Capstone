"""Controller for AST flowchart builder
"""
import ast
import sys
from pathlib import Path
from flowchart_builder import getnode


def run_controller():
    if len(sys.argv) != 2:
        print("Usage: py flowchart_controller.py <file.py>")
        return
    filename = sys.argv[1]
    source = Path(filename).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=filename)
    getnode(tree, "flowchart.dot")
    print("Controller completed successfully!")

if __name__ == "__main__":
    run_controller()

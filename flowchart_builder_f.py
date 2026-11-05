import ast
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Node:
    id: str
    label: str
    kind: str = "process"


@dataclass
class Edge:
    source: str
    target: str
    label: str = ""

class GraphBuilder:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.counter = 0

    def node(self, label, kind="process"):
        identifier = f"n{self.counter}"
        self.counter += 1
        self.nodes.append(Node(identifier, label, kind))
        return identifier

    def edge(self, source, target, label=""):
        self.edges.append(Edge(source, target, label))

    def connect(self, incoming, target):
        for source, label in incoming:
            self.edge(source, target, label)

    def sequence(self, statements, incoming, loop=None):
        for stmt in statements:
            if not incoming:
                break
            if isinstance(stmt, ast.If):
                decision = self.node(ast.unparse(stmt.test) + "?", "decision")
                self.connect(incoming,decision)
                true_out = self.sequence(stmt.body, [(decision, "True")], loop)
                false_out = (self.sequence(stmt.orelse, [(decision, "False")], loop)
                             if stmt.orelse else [(decision, "False")])
                incoming = true_out + false_out
            elif isinstance(stmt, (ast.While, ast.For)):
                condition = (ast.unparse(stmt.test) if isinstance(stmt, ast.While)
                            else f"{ast.unparse(stmt.target)} in {ast.unparse(stmt.iter)}")
                decision = self.node(condition + "?", "decision")
                self.connect(incoming, decision)
                break_edges = []
                body_out = self.sequence(stmt.body, [(decision, "True")],
                                         (decision, break_edges))
                for source, label in body_out:
                    self.edge(source, decision, label)
                normal_exit = [(decision, "False")]
                if stmt.orelse:
                    normal_exit = self.sequence(stmt.orelse, normal_exit, loop)
                incoming = normal_exit + break_edges
            elif isinstance(stmt, ast.Break):
                if loop is None:
                    raise ValueError("break outside a loop")
                step = self.node("break")
                self.connect(incoming, step)
                loop[1].append((step, ""))
                incoming = []
            elif isinstance(stmt, (ast.Return, ast.Raise)):
                step = self.node(ast.unparse(stmt))
                self.connect(incoming, step)
                self.edge(step, self.end)
                incoming = []
            elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                step = self.node(f"define {stmt.name}")
                self.connect(incoming, step)
                incoming = [(step, "")]
            else:
                step = self.node(ast.unparse(stmt))
                self.connect(incoming, step)
                incoming = [(step, "")]
        return incoming

    def build(self, tree):
        if not isinstance(tree, ast.Module):
            raise TypeError("Expected ast.Module")
        start = self.node("Start", "terminal")
        self.end = self.node("End", "terminal")
        outgoing = self.sequence(tree.body, [(start, "")])
        self.connect(outgoing, self.end)
        return self
    def to_dot(self):
        shapes = {"terminal": "oval", "decision": "diamond", "process": "box"}
        lines = ["digraph flowchart{", " rankdir=TB;", '  node [fontname="Arial"];']
        for node in self.nodes:
            label = json.dumps(node.label, ensure_ascii=False)
            lines.append(f"  {node.id} [label={label}, shape={shapes[node.kind]}];")
        for edge in self.edges:
            label = f" [label={json.dumps(edge.label)}]" if edge.label else ""
            lines.append(f"  {edge.source} -> {edge.target}{label};")
        lines.append("}")
        return "\n".join(lines) + "\n"
def getnode(tree=None, output="flowchart.dot"):
    if tree is None:
        raise ValueError("Pass the parsed AST: getnode(tree)")
    builder = GraphBuilder().build(tree)
    Path(output).write_text(builder.to_dot(), encoding="utf-8")
    print(f"Generated {output}: {len(builder.nodes)} nodes, {len(builder.edges)} edges")
    return builder

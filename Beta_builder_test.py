#Defining nodes and edges
#PLAN: GO LINE BY LINE TO SEND EACH SEGMENT OF CODE IN THROUGH TO THE CONTROLLER
#INITIAL PLAN: GET FIRST LINE OF AST TO SET AT OPENING NODE

import ast
from collections import namedtuple


Node = namedtuple("Node", "id kind label")
Edge = namedtuple("Edge", "source target label") 


def load_tree(path): #reads treedump and rebuilds it
    with open(path, 'r', encoding='utf-8') as f:
        tree = to_ast(ast.parse(f.read(), mode="eval").body) #parses text from the file and rebuilds it into an AST
    return ast.fix_missing_locations(tree) #fills in any missing line numbers and column offsets in the AST nodes

def to_ast(expr): #turns the text back into an AST node
    if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name):
        cls = getattr(ast, expr.func.id, None) #only works for accepted ast nodes
        if not (isinstance(cls, type) and issubclass(cls, ast.AST)):
            raise ValueError(f"Unknown AST node type: {expr.func.id!r}")
        return cls(**{kw.arg: to_ast(kw.value) for kw in expr.keywords})
    if isinstance(expr, ast.List):
        return [to_ast(elt) for elt in expr.elts]
    if isinstance(expr, ast.Name) and expr.id == "None":
        return None
    if isinstance(expr, ast.Name) and expr.id == "Ellipsis":
        return ...
    return ast.literal_eval(expr)

        

class GraphBuilder: #starts creation of nodes and edges
    def build(self, tree):
        self.nodes = []
        self.edges = []
        self.functions = []
        self.add_flow("Main Program", tree.body)
        for func in self.functions:
            self.add_flow(func.name, func.body)
        return self.nodes, self.edges

    def add_flow(self, name, body): 
        start = self.new("start", "Start: " + name, [])
        self.end = self.new("end", "End", [])
        self.loops = [] #stack of the loops we encounter
        exits = self.block(body, [(start, "")])
        self.connect_all(exits, self.end)

    def add_node(self, kind, label):
        node_id = f"n{len(self.nodes)}" #ids are n0, n1 etc
        self.nodes.append(Node(node_id, kind, label.splitlines()[0][:40])) #only one line of label, up to 40 chars
        return node_id

    def connect(self, source_id, target_id, label=""):
        self.edges.append(Edge(source_id, target_id, label))

    def connect_all(self, exits, target_id):
        for source_id, label in exits:
            self.connect(source_id, target_id, label)

    def new(self, kind, label, exits): #draws arrows into the node from exits
        node_id = self.add_node(kind, label)
        self.connect_all(exits, node_id)
        return node_id

    def block(self, body, exits): #builds the list of statements
        for stmt in body:
            exits = self.statement(stmt, exits)
        return exits

    def statement(self, stmt, exits):
        if isinstance(stmt, ast.FunctionDef):
            self.functions.append(stmt)          
            return exits
        if isinstance(stmt, ast.If):
            return self.if_statement(stmt, exits)
        if isinstance(stmt, ast.While):
            return self.while_statement(stmt, exits)
        if isinstance(stmt, ast.For):
            return self.for_statement(stmt, exits)
        if isinstance(stmt, ast.Try):
            return self.try_statement(stmt, exits)
        if isinstance(stmt, ast.With):
            return self.with_statement(stmt, exits)
        if isinstance(stmt, ast.Break) and self.loops:
            return self.break_statement(exits)
        if isinstance(stmt, ast.Continue) and self.loops:
            return self.continue_statement(exits)
        if isinstance(stmt, (ast.Return, ast.Raise)):
            return self.return_statement(stmt, exits)
        return self.simple_statement(stmt, exits)

    def if_statement(self, stmt, exits):
        n = self.new("if", "if " + ast.unparse(stmt.test), exits)
        return self.block(stmt.body, [(n, "true")]) + self.block(stmt.orelse, [(n, "false")])
 
    def while_statement(self, stmt, exits):
        return self.loop(stmt, "while " + ast.unparse(stmt.test), "true", "false", exits)
 
    def for_statement(self, stmt, exits):
        label = f"for {ast.unparse(stmt.target)} in {ast.unparse(stmt.iter)}"
        return self.loop(stmt, label, "next", "done", exits)

    def loop(self, stmt, label, into, out, exits):
        header = self.new("loop", label, exits)
        breaks = []
        self.loops.append((header, breaks))
        body_exits = self.block(stmt.body, [(header, into)])
        self.loops.pop()
        self.connect_all(body_exits, header)
        return self.block(stmt.orelse, [(header, out)]) + breaks

    def try_statement(self, stmt, exits):
        n = self.new("try", "try", exits)
        done = self.block(stmt.orelse, self.block(stmt.body, [(n, "")]))
        for h in stmt.handlers:
            label = "except " + ast.unparse(h.type) if h.type else "except"
            hn = self.new("except", label, [(n, "exception")])
            done += self.block(h.body, [(hn, "")])
        return self.block(stmt.finalbody, done)

    def with_statement(self, stmt, exits):
        n = self.new("with", "with " + ", ".join(ast.unparse(i) for i in stmt.items), exits)
        return self.block(stmt.body, [(n, "")])

    def break_statement(self, exits):
        n = self.new("break", "break", exits)
        self.loops[-1][1].append((n, "break"))               #leaving the loop
        return []

    def continue_statement(self, exits):
        n = self.new("continue", "continue", exits)
        self.connect(n, self.loops[-1][0], "continue")       #back to the loop top
        return []

    def return_statement(self, stmt, exits):
        n = self.new(type(stmt).__name__.lower(), ast.unparse(stmt), exits)
        self.connect(n, self.end)
        return []

    def simple_statement(self, stmt, exits):
        n = self.new("simple", ast.unparse(stmt), exits)
        return [(n, "")]





def getnode(path = "Treedump.txt"): #controller call
    return GraphBuilder().build(load_tree(path))



#Defining nodes and edges
#PLAN: GO LINE BY LINE TO SEND EACH SEGMENT OF CODE IN THROUGH TO THE CONTROLLER
#INITIAL PLAN: GET FIRST LINE OF AST TO SET AT OPENING NODE

import ast
from collections import namedtuple


Node = namedtuple("Node", "id kind label")
Edge = namedtuple("Edge", "source target label") 


def load_tree(path): #reads treedump and rebuilds it
    with open(path, 'r', encoding='utf-8') as f:
        tree = to_ast(ast.parse(f.read(), mode="eval").body) #parses text from the file and rebuilds it into an AST since we are saving the original ast as a txt file instead of passing a real tree
    return ast.fix_missing_locations(tree) #fills in any missing line numbers and column offsets in the AST nodes

def to_ast(expr): #turns the text back into an AST node
    if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name): #checks if the expression is a function call and if the function being called is a name (not an attribute or something else)
        cls = getattr(ast, expr.func.id, None) #only works for accepted ast nodes, looks up  the function name, and if it can't be found returns none
        if not (isinstance(cls, type) and issubclass(cls, ast.AST)): #checks that cls is a class and that it is a subclass of ast
            raise ValueError(f"Unknown AST node type: {expr.func.id!r}")#raises an error if the function name can't be found, func.id!r returns it as text
        return cls(**{kw.arg: to_ast(kw.value) for kw in expr.keywords})#makes the ast node, kw.arg is the name, kw.value is the value, this is a dict of expr keywords
    if isinstance(expr, ast.List): #is the expr is a list, it will take all of the elements and put them into a list of ast nodes, to_ast is called recursively on each element
        return [to_ast(elt) for elt in expr.elts]
    if isinstance(expr, ast.Name) and expr.id == "None": #if the expr is none then returns none
        return None
    if isinstance(expr, ast.Name) and expr.id == "Ellipsis": #if the expr is ellipsis then returns ellipsis, might have to make more of these as we add tests
        return ...
    return ast.literal_eval(expr)#returns literals, such as integers, floats, etc

        

class GraphBuilder: #starts creation of nodes and edges
    def build(self, tree):
        self.nodes = []
        self.edges = []
        self.functions = []
        self.add_flow("Main Program", tree.body) #Starts main program flowchart.
        for func in self.functions: #seperates functions into their own flowcharts, potentially useful for json? just figured that they should be seperate flowchart either way with the expansion requirement
            self.add_flow(func.name, func.body)
        return self.nodes, self.edges #returns nodes and edges to caller

    def add_flow(self, name, body): #flowchart creation
        start = self.new("start", "Start: " + name, []) #start node, empty list is connections
        self.end = self.new("end", "End", []) #end node 
        self.loops = [] #stack of the loops we encounter
        exits = self.block(body, [(start, "")]) #exits is all of the nodes that need to have edges connected
        self.connect_all(exits, self.end) #connects exit nodes to the final end node

    def add_node(self, kind, label):
        node_id = f"n{len(self.nodes)}" #ids are n0, n1 etc
        self.nodes.append(Node(node_id, kind, label.splitlines()[0])) #only one line of label, removed 40 char limit, could reimplement with [:x] current test cases go over 40 chars
        return node_id #returns node num

    def connect(self, source_id, target_id, label=""): #connects two nodes
        self.edges.append(Edge(source_id, target_id, label)) #adds edge to edge list with the two nodes it connects, and a potential label

    def connect_all(self, exits, target_id): #connects multiple nodes to one
        for source_id, label in exits: #for each node with label in exits, connects it to the target node with the label
            self.connect(source_id, target_id, label)

    def new(self, kind, label, exits): #draws arrows into the node from exits
        node_id = self.add_node(kind, label)#creation of node
        self.connect_all(exits, node_id) #connects exit nodes to this node
        return node_id #new node id

    def block(self, body, exits): #builds the list of statements
        for stmt in body: #iterates statements in the block
            exits = self.statement(stmt, exits) #updates exits to be the exits from the statement, so that the next statement will connect to the previous one
        return exits

    def statement(self, stmt, exits): #switch statement for all of the types of statements, returns the exits from the statement
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
        return self.simple_statement(stmt, exits) #if a statement wasn't caught this is like a catch all for unhandled statements.

    def if_statement(self, stmt, exits):
        n = self.new("if", "if " + ast.unparse(stmt.test), exits) #new node, name if, type if, unparsing the test expression to get the text of the if statement, and connecting it to the exits
        return self.block(stmt.body, [(n, "true")]) + self.block(stmt.orelse, [(n, "false")]) #returns both exits for true and false so if will connect to both.
 
    def while_statement(self, stmt, exits): 
        return self.loop(stmt, "while " + ast.unparse(stmt.test), "true", "false", exits) #ex while , unparses test, true enters loop, false exits
 
    def for_statement(self, stmt, exits):
        label = f"for {ast.unparse(stmt.target)} in {ast.unparse(stmt.iter)}" #for target in iteration, 
        return self.loop(stmt, label, "next", "done", exits) #returns next to go back into loop, done to exit loop, exits is the list of nodes that need to be connected to the for loop

    def loop(self, stmt, label, into, out, exits): #broader for and while loop, both of those call this
        header = self.new("loop", label, exits) #main loop node
        breaks = [] #list of breaks
        self.loops.append((header, breaks)) #adds loop to stack incase we nest
        body_exits = self.block(stmt.body, [(header, into)]) #processes loop
        self.loops.pop() #removes loop from stack
        self.connect_all(body_exits, header) #connects exits from loop to the start loop node
        return self.block(stmt.orelse, [(header, out)]) + breaks #if there is an else block, combines exits with break exits

    def try_statement(self, stmt, exits):
        n = self.new("try", "try", exits) #new try node
        done = self.block(stmt.orelse, self.block(stmt.body, [(n, "")])) #stores exits for the try and the else block
        for h in stmt.handlers: #for excepts
            label = "except " + ast.unparse(h.type) if h.type else "except" #parses exception type
            hn = self.new("except", label, [(n, "exception")]) #exception node
            done += self.block(h.body, [(hn, "")]) #adds exception block exit to try statement exits
        return self.block(stmt.finalbody, done) #returns all exits, also handles finally

    def with_statement(self, stmt, exits):
        n = self.new("with", "with " + ", ".join(ast.unparse(i) for i in stmt.items), exits) #new with node joins the statements together for each statement in the with
        return self.block(stmt.body, [(n, "")]) #processes the body of the with statement and returns the exits

    def break_statement(self, exits):
        n = self.new("break", "break", exits) #new break node
        self.loops[-1][1].append((n, "break")) #leaving the loop, adds node to break node list
        return [] #does not return exit since break leaves the loop

    def continue_statement(self, exits):
        n = self.new("continue", "continue", exits) #continue node creation
        self.connect(n, self.loops[-1][0], "continue") #back to the loop top, connects to loop header
        return [] #does not return an exit since it skips an iteration for a loop

    def return_statement(self, stmt, exits):
        n = self.new(type(stmt).__name__.lower(), ast.unparse(stmt), exits) #return / raise statement, statement type is the node type, and the statement itself becomes the label
        self.connect(n, self.end) #connects return node to the end node, since return leaves the function
        return [] #does not have an exit since it leaves the function, so returns empty list

    def simple_statement(self, stmt, exits):
        n = self.new("simple", ast.unparse(stmt), exits) #new node with the statement as the label, this is for unhandled statements
        return [(n, "")] #the node is an exit, so returns it as a list with an empty label





def getnode(path = "Treedump.txt"): #controller call
    return GraphBuilder().build(load_tree(path))



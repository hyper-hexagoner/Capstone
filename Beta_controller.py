##CONTROLLER TEST
from Beta_builder_test import getnode
from ast_test import main
from renderer_test import Render


def write_instructions(nodes, edges): #instead of builder writing to DotInstructions, controller will with the nodes and edges from getNode() from builder
    with open("DotInstructions.py", 'w', encoding="utf-8") as instructions:
        for n in nodes:
            print(f"dot.node({n.id!r}, graphviz.escape({n.label!r}))", file=instructions)
        for e in edges: #dot.node is adding the node and id, along with label, !r is used to get it via string. file is so that a print statement won't print to terminal
            if e.label:
                print(f"dot.edge({e.source!r}, {e.target!r}, label={e.label!r})", file = instructions)
            else: #Differentiate between labeled edges and not because an edge with yes/no will have a label, but an edge with no label will error if we try to input a label.
                print(f"dot.edge({e.source!r}, {e.target!r})", file=instructions)




output = open("Treedump.txt", 'w') #empties out the AST file for reuse
main()#creates ast
nodes, edges = getnode("Treedump.txt")#reads ast and returns both lists to controller
write_instructions(nodes, edges)#writes nodes and edges to dot
Render()#combines header and footer and nodes

with open("FINAL_Dot_Instructions.py", 'r') as final: #reads finalDOT which is from renderer
    final_code = final.read()#reads the file
    exec(final_code)#makes the dot file into a graph


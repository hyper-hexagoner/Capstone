##CONTROLLER TEST, SHAPES UPDATE
from Beta_builder_test import getnode
from ast_test import main
from renderer_test import Render


def write_instructions(nodes, edges): #instead of builder writing to DotInstructions, controller will with the nodes and edges from getNode() from builder
    with open("DotInstructions.py", 'w', encoding="utf-8") as instructions:
        for n in nodes:
            print(n.kind) # debug feature to check that 'kind' is correctly labeling the nodes, will be commented out when final release hits
            if ((n.kind == "start") or (n.kind=="end")): ##BEGIN SWITCH STATEMENT FOR NODE SHAPES
                print(f"dot.node({n.id!r},shape='circle',style='filled',fillcolor='black',fontcolor='white',label=graphviz.escape({n.label!r}))", file=instructions)

            elif (n.kind == "if"):
                print(f"dot.node({n.id!r},shape='diamond',style='filled',fillcolor='gold1',height='1.5', label=graphviz.escape({n.label!r}))", file=instructions)

            elif (n.kind == "funcstart"):
                print(f"dot.node({n.id!r},shape='hexagon',style='filled',fillcolor='cyan',height = '1.5', label=graphviz.escape({n.label!r}))", file=instructions)

            elif (n.kind == "funcend"):
                print(f"dot.node({n.id!r},shape='hexagon',color='cyan',height = '1.5',penwidth='4.5',width = '1.5',style = 'striped', label=graphviz.escape({n.label!r}))", file=instructions)

            elif (n.kind == "try"):
                print(f"dot.node({n.id!r},shape='trapezium',style='filled',fillcolor='aquamarine', label=graphviz.escape({n.label!r}))", file=instructions)

            elif (n.kind == "return"):
                print(f"dot.node({n.id!r},shape='cds',style='filled',fillcolor='pink', label=graphviz.escape({n.label!r}))", file=instructions)

            elif (n.kind == "except"):
                print(f"dot.node({n.id!r},shape='cds',style='filled',fillcolor='brown1', orientation = '90', label=graphviz.escape({n.label!r}))", file=instructions)

            elif (n.kind == "for"): #kind is "for"
                print(f"dot.node({n.id!r},shape='triangle',style='filled',fillcolor='darkolivegreen1',height='2',orientation='270', label=graphviz.escape({n.label!r}))", file=instructions)

            elif (n.kind == "while"): #kind is "while"
                print(f"dot.node({n.id!r},shape='triangle',penwidth='4.5',height='2',orientation='270',style='striped',color='green', label=graphviz.escape({n.label!r}))", file=instructions)

            else: #simple statement
                print(f"dot.node({n.id!r}, graphviz.escape({n.label!r}))", file=instructions)  #Default node, will be rectangle     

        for e in edges: #dot.node is adding the node and id, along with label, !r is used to get it via string. file is so that a print statement won't print to terminal
            if e.label:
                print(f"dot.edge({e.source!r}, {e.target!r}, label={e.label!r},style = 'dashed')", file = instructions)
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


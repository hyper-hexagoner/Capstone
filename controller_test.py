##CONTROLLER TEST
from ast_test import main
from builder_test import getnode
from renderer_test import Render


output = open("Treedump.txt", 'w') #empties out the AST file for reuse
main() ##create AST 
getnode() ##gets nodes and edges from the AST
Render() ##Combines the header, nodes from getnode and the footer to a final file

with open("FINAL_Dot_Instructions.py",'r') as final: ##opens the file created from Render()
    final_code= final.read() #reads the file 
    exec(final_code) #executes the DOT file to create a graph








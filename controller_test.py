##CONTROLLER TEST
from builder_test import getnode
from ast_test_v2 import main
dot = open("DotInstructions.py",'w')
output = open("Treedump.txt", 'w')
main()
getnode()



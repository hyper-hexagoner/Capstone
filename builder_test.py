#Defining nodes and edges
#PLAN: GO LINE BY LINE TO SEND EACH SEGMENT OF CODE IN THROUGH TO THE CONTROLLER
#INITIAL PLAN: GET FIRST LINE OF AST TO SET AT OPENING NODE

def getnode():
    dot = open("DotInstructions.py",'w')
    output = open("Treedump.txt", 'r')
    firstline= output.readline()
    print(firstline)
    if firstline=="Module(\n":
        print(("dot.node('A','START STATE')"),file=dot)
    else:
        print("ERROR. WRONG LINE FOUND. FOUND LINE",firstline, "INSTEAD", file=dot)


getnode()

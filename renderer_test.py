#Graph Renderer class, Created by Lucas Castillo
def Render():
    head = open("graph_header.py", 'r') #Opens pre-made header file
    foot = open("graph_footer.py",'r') #Opens pre-made footer file
    dot = open("DotInstructions.py",'r') #Opens dynamically made Instructions file
    with open("FINAL_Dot_Instructions.py", "a", encoding="utf-8") as dot_final: #opens to append to the end of the file
        dot_final.seek(0) 
        dot_final.truncate() #reset dot instructions
        dot_final.write(head.read()) #places in header
        dot_final.write(dot.read()) #places in instructions for nodes and edges
        dot_final.write(foot.read()) #places in footer




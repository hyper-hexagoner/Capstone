##HEADER FOR ALL DOT FILES, VERSION 2
##Updated Version: changes default shape to rectangles, and moves the file to a more conventional file name
##CREATED BY LUCAS CASTILLO
import graphviz

dot = graphviz.Digraph('example',filename='betadot') #Example file name

dot.attr(rankdir='TB')
dot.attr('node',shape="rectangle")


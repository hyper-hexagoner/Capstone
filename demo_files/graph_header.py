##HEADER FOR ALL DOT FILES, VERSION 1
##CREATED BY LUCAS CASTILLO
import graphviz

dot = graphviz.Digraph('example',filename='exampledot.png') #Example file name

dot.attr(rankdir='LR')
dot.attr('node',shape="rectangle")
#dot.attr('node',shape = 'hexagon') ##FUNCTION CALL NODE
#dot.attr('node',shape="trapezium") ##PRINT STATEMENT NODE
#dot.attr('node',shape="triangle") ##IF STATEMENT NODE


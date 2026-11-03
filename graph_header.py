##HEADER FOR ALL DOT FILES, VERSION 1
##CREATED BY LUCAS CASTILLO
import graphviz

dot = graphviz.Digraph('example',filename='exampledot.gv') #Example file name

dot.attr(rankdir='LR')
dot.attr('node',shape = 'circle')

"""Regression tests for flowchart builder"""
import ast
import unittest
from flowchart_builder import GraphBuilder


class flowchartBuilderTests(unittest.TestCase):
    def build(self, source):
        return GraphBuilder().build(ast.parse(source))

    def test_if_else_branches(self):
            builder = self.build('x = 10\nif x > 5:\n  print("Greater")\nelse:\n  print("Smaller")\n')
            self.assertIn('label="True"', builder.to_dot())
            self.assertIn('label="False"', builder.to_dot())
            self.assertIn('shape=diamond', builder.to_dot())
    def test_while_loop_back_edge(self):
            builder = self.build('x=0\nwhile x < 5:\n  print(x)\n  x+=1\n')
            self.assertTrue(any(e.target == 'n3' for e in builder.edges))

    def test_for_loop(self):
        builder = self.build('for i in range(3):\n  print(i)\n')
        self.assertIn('i in range(3)?', builder.to_dot())
if __name__ == '__main__':
    unittest.main()


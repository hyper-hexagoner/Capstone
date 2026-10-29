##AST TEST VERSION 0.2
##REVISIONS MADE: AST now writes to file directly from a print statement, reduced file size
##AUTHOR: LUCAS

import ast
import sys
treedump =open("Treedump.txt", 'w') #NOTE: IN FUTURE VERSIONS WE WILL NEED DYNAMIC/MULTIPLE FILE NAMES FOR OUTER FUNCTIONS
 
def main():
    if len(sys.argv) != 2:
        print("usage: python ast_test.py <file.py>")
        sys.exit(1)
 
    path = sys.argv[1]
 
    with open(path, encoding="utf-8") as f:
        source = f.read()
 
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as e:
        print(f"Syntax error in {path}, line {e.lineno}: {ime.msg}")
        sys.exit(1)
 
    print(ast.dump(tree, indent=2),file=treedump) ##NOTE: Perhaps second function to dynamaically name and parse outer files?

 



if __name__ == "__main__":
    main()

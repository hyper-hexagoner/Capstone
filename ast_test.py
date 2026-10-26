import ast
import sys
 
 
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
        print(f"Syntax error in {path}, line {e.lineno}: {e.msg}")
        sys.exit(1)
 
    print(ast.dump(tree, indent=1))

    with open("output.txt", 'w', encoding="utf-8") as filew:
        filew.write(ast.dump(tree,indent=1))

 
 
if __name__ == "__main__":
    main()
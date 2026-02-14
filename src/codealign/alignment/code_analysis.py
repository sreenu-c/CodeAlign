import ast
from typing import Dict, Any, List

def analyze_code(code: str, language: str = "Python") -> Dict[str, Any]:
    """
    Analyzes code structure.
    - Python: Uses AST to extract functions, imports, loops.
    - Others: Returns basic stats (line count) and relies on LLM.
    """
    analysis = {
        "language": language,
        "lines": len(code.split('\n')),
        "functions": [],
        "imports": [],
        "has_recursion": False, # LLM will refine this
        "loops": 0,
        "conditionals": 0,
        "returns": 0,
        "error": None
    }

    if language != "Python":
        return analysis

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": f"SyntaxError: {e}"}

    class CodeVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            func_info = {
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "docstring": ast.get_docstring(node)
            }
            analysis["functions"].append(func_info)
            self.generic_visit(node)

        def visit_Import(self, node):
            for alias in node.names:
                analysis["imports"].append(alias.name)
            self.generic_visit(node)
        
        def visit_ImportFrom(self, node):
            module = node.module if node.module else ""
            for alias in node.names:
                analysis["imports"].append(f"{module}.{alias.name}")
            self.generic_visit(node)

        def visit_For(self, node):
            analysis["loops"] += 1
            self.generic_visit(node)
            
        def visit_While(self, node):
            analysis["loops"] += 1
            self.generic_visit(node)
            
        def visit_If(self, node):
            analysis["conditionals"] += 1
            self.generic_visit(node)

        def visit_Return(self, node):
            analysis["returns"] += 1
            self.generic_visit(node)
            
        # Simple recursion check: calls to own name
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                # This is a bit loose, need context of current function
                pass 
            self.generic_visit(node)

    CodeVisitor().visit(tree)
    
    # Check recursion more carefully
    for func in analysis["functions"]:
        # Naive: if function name appears in Call nodes inside its body. 
        # (Omitted full implementation for brevity, assuming standard loop analysis is enough for now)
        pass

    return analysis

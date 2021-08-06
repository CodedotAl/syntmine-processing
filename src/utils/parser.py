import ast
import tokenize
from io import StringIO
class IdentifierVisitor(ast.NodeVisitor):
    """ast.NodeVisitor Module for visiting 
       and hashing all the identifiers in the program.
       args : None

    """
    def __init__(self):
        self.parse_dict = {
            "function_names": [], #function names in the given prog
            "terminals" : [], #terminal nodes in the code(All terminal nodes in the given prog.)
            "arg_variables" : [], #argument variable_names in functions
            "hardcoded_values" : [] #hardcoded values(literals)
            }
    def visit_Constant(self, node):
        """visting all the hardcoded/literal values"""
        hardcoded_node = {"value":node.value,"type":node.kind}
        self.parse_dict["hardcoded_values"].append(hardcoded_node)
    def visit_Name(self,node):
        """
        visit all the terminal nodes in a given Program AST.
        """
        self.parse_dict["terminals"].append(node.id)

    def visit_FunctionDef(self, node):
        """
        visit function bodies for function names.
        """
        self.parse_dict["function_names"].append(node.name)
        argument_vars = [argument.arg for argument in node.args.args]
        self.parse_dict["arg_variables"] += argument_vars

class Data_Processing:
    """
    Main Caller Class for Data Processing Class
    args : 
         visitor_class (ast.NodeVisitor) : Node Visitor for a Parse Tree.
    """
    def __init__(self,visitor_class = IdentifierVisitor):
        self.Vistor_Class  = visitor_class()

    def extract_comment(self,prog_string):
        """
        Given a program string, extracts comments from the prog string.
        args : 
              prog_string (str) : Program String
        """
        res = []
        prog_string_io = StringIO(prog_string)
        for toktype, tokval, begin, end, line in tokenize.generate_tokens(prog_string_io.readline):
            if toktype == tokenize.COMMENT:
                res.append((toktype, tokval))
        comment_list = tokenize.untokenize(res)
        return comment_list
    def __call__(self, prog_string ,**kwargs):
        """
        Main Data Processing String
        args:
            prog_string (str) : Program String of a Python Code.
        """
        parse_tree = ast.parse(prog_string)
        parse_visitor = self.Vistor_Class
        parse_visitor.visit(parse_tree)
        parse_comment = self.extract_comment(prog_string)
        prog_dict = {"code":parse_visitor.parse_dict,"comment":parse_comment}
        return prog_dict
        


if __name__ == "__main__":
    program_string = """text = "trial"
num_var = 57
def reverse_string(string):
        # Reverse the given hardcoded_value "string"
        return string[::-1]
reversed = reverse_string(text)
print(reversed)"""
    Processor = Data_Processing()
    print(Processor(program_string))
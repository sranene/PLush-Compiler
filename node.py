import json

class Node(object):
    def __init__(self, t, *args):
        self.type = t
        self.args = args

    def __str__(self):
        s = "type: " + str(self.type) + "\n"
        s += "".join(["i: " + str(i) + "\n" for i in self.args])
        return s

##############################################################################


class Program:
    def __init__(self, global_vars, functions):
        self.global_vars = global_vars
        self.functions = functions

    def to_dict(self):
        return {
            "nt": "program",
            "global_vars": [var.to_dict() for var in self.global_vars],
            "functions": [func.to_dict() for func in self.functions]
        }
    
    def __str__(self):
        return str(self.to_dict())
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


class Body:
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def to_dict(self):
        return {
            "nt": "body",
            "statement_list": [stmt.to_dict() for stmt in self.statement_list]
        }

    def __str__(self):
        return str(self.to_dict())



class If:
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def to_dict(self):
        if_body_dict = [stmt.to_dict() for stmt in self.if_body] if self.if_body is not None and self.if_body != [None] else "None"
        else_body_dict = self.else_body.to_dict() if isinstance(self.else_body, Else) else "None"
        return {
            "nt": "if",
            "condition": self.condition.to_dict(),
            "if": if_body_dict,
            "else": else_body_dict
        }
    
    def __str__(self):
        return str(self.to_dict())



class Else:
    def __init__(self, body):
        self.body = body

    def to_dict(self):
        return [stmt.to_dict() for stmt in self.body] if self.body is not None and self.body != [None] else "None"

    def __str__(self):
        return str(self.to_dict())


class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_dict(self):
        return {
            "nt": "while",
            "condition": self.condition.to_dict(),
            "body": [stmt.to_dict() for stmt in self.body] if self.body is not None and self.body != [None] else "None"
        }

    def __str__(self):
        return str(self.to_dict())


class FunctionDecl:
    def __init__(self, name, parameters, type, body=None):
        self.name = name.name
        self.parameters = parameters if parameters is not None else "None"
        self.type = type.to_dict() if type is not None else "None"
        self.body = body if body is not None else "None"

    def to_dict(self):        
        return {
            "nt": "functiondecl",
            "name": self.name,
            "parameters": [prmt.to_dict() for prmt in self.parameters] if self.parameters != "None" else "None",
            "type": self.type if self.type != "None" else "None",
            "body": [stmt.to_dict() for stmt in self.body] if self.body != "None" and self.body != [None] else "None"
        }

    def __str__(self):
        return str(self.to_dict())


class VariableDecl:
    def __init__(self, modifier, name, type, initializer):
        self.modifier = modifier
        self.name = name.name
        self.type = type.to_dict()
        self.initializer = initializer.to_dict()

    def to_dict(self):
        return {
            "nt": "vardecl",
            "modifier": self.modifier,
            "name": self.name,
            "type": self.type,
            "initializer": self.initializer
        }
    
    def __str__(self):
        return str(self.to_dict())


class Assignment:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def to_dict(self):
        return {
            "nt": "assignment",
            "name": self.name.to_dict(),
            "expression": self.expression.to_dict()
        }

    def __str__(self):
        return str(self.to_dict())



#class BinaryOp:
#    def __init__(self, sign, left, right):
#        self.sign = sign.to_dict()
#        self.left = left.to_dict()
#        self.right = right.to_dict()
#
#    def to_dict(self):
#        return {
#            "operator": self.sign,
#            "left": self.left.to_dict() if isinstance(self.left, Node) else self.left,
#            "right": self.right.to_dict() if isinstance(self.right, Node) else self.right
#        }
#
#    def __str__(self):
#        return str(self.to_dict())
#
#class UnaryOp:
#    def __init__(self, operator, expr):
#        self.operator = operator.to_dict()
#        self.expr = expr.to_dict()
#
#    def to_dict(self):
#        return {
#            "operator": self.operator,
#            "expr": self.expr.to_dict() if isinstance(self.expr, Node) else self.expr,
#        }
#
#    def __str__(self):
#        return str(self.to_dict())


class ArrayCallInline:
    def __init__(self, name, first_index, second_index=None):
        self.name = name.name
        self.first_index = first_index
        self.second_index = second_index

    def to_dict(self):
        if self.second_index is not None:
            return {
                "nt": "arraycallinline",
                "name": self.name,
                "first_index": self.first_index.to_dict(),
                "second_index": self.second_index.to_dict()
            }
        else:
            return {
                "nt": "arraycallinline",
                "name": self.name,
                "first_index": self.first_index.to_dict()
            }

    def __str__(self):
        return str(self.to_dict())

class Type:
    def __init__(self, typename):
        self.typename = typename

    def to_dict(self):
        return self.typename

    def __str__(self):
        return str(self.to_dict())

class ArrayType:
    def __init__(self, typename):
        self.typename = typename.typename

    def to_dict(self):
        return "array" + self.typename

    def __str__(self):
        return str(self.to_dict())
    
class ArrayType2:
    def __init__(self, typename):
        self.typename = typename.typename

    def to_dict(self):
        return "array" + self.typename + "2"

    def __str__(self):
        return str(self.to_dict())


class Name:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return self.name

    def __str__(self):
        return str(self.to_dict())

class Int:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "int",
            "value": self.value
        }

    def __str__(self):
        return str(self.to_dict())

class Array:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "array",
            "value": self.value
        }

    def __str__(self):
        return str(self.to_dict())

class Void:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "void",
            "value": self.value
        }

    def __str__(self):
        return str(self.to_dict())

class Char:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "char",
            "value": self.value
        }

    def __str__(self):
        return str(self.to_dict())

class String:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "string",
            "value": self.value
        }

    def __str__(self):
        return str(self.to_dict())

class Float:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "float",
            "value": self.format_float_value()
        }

    def format_float_value(self):
        if self.value.startswith('.'):
            return '0' + self.value  # Adiciona um zero à esquerda
        else:
            return self.value

    def __str__(self):
        return str(self.to_dict())

class Boolean:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "boolean",
            "value": self.value
        }

    def __str__(self):
        return str(self.to_dict())


class Parameter:
    def __init__(self, modifier, name, type):
        self.modifier = modifier
        self.name = name.name
        self.type = type.to_dict()

    def to_dict(self):
        return {
            "modifier": self.modifier,
            "name": self.name,
            "type": self.type
        }

    def __str__(self):
        return str(self.to_dict())


class ArgumentList:
    def __init__(self, argument, argument_list):
        self.argument = argument
        self.argument_list = argument_list if argument_list is not None else []

    def __str__(self):
        return f"ArgumentList : ({self.argument}, {self.argument_list})"


class ParameterList:
    def __init__(self, parameter, parameter_list):
        self.parameter = parameter
        self.parameter_list = parameter_list

    def __str__(self):
        return f"ParameterList : ({self.parameter}, {self.parameter_list})"

class FunctionCallInline:
    def __init__(self, name, parameter_list):
        self.name = name.name
        self.parameter_list = parameter_list

    def to_dict(self):
        return {
            "nt": "functioncallinline",
            "name": self.name,
            "parameter_list": [param.to_dict() for param in self.parameter_list] if self.parameter_list is not None else "None"
        }

    def __str__(self):
        return str(self.to_dict())


class Value:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return self.value.to_dict()

    def __str__(self):
        return str(self.to_dict())


class NotValue:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "notvalue",
            "value": self.value.to_dict()
        }

    def __str__(self):
        return str(self.to_dict())

class Parenteses:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "nt": "parenteses",
            "value": self.value.to_dict()
        }

    def __str__(self):
        return str(self.to_dict())

class Expression:
    def __init__(self, operator, left, right):
        self.operator = operator.to_dict()
        self.left = left.to_dict()
        self.right = right.to_dict()

    def to_dict(self):
        return {
            "nt" : "expression",
            "operator": self.operator,
            "left": self.left.to_dict() if isinstance(self.left, Node) else self.left,
            "right": self.right.to_dict() if isinstance(self.right, Node) else self.right
        }

    def __str__(self):
        return str(self.to_dict())


class AndOr:
    def __init__(self, operator):
        self.operator = operator

    def to_dict(self):
        return self.operator

    def __str__(self):
        return str(self.to_dict())

class Sign:
    def __init__(self, operator):
        self.operator = operator

    def to_dict(self):
        return self.operator
    
    def __str__(self):
        return str(self.to_dict())

class Uminus:
    def __init__(self, expression):
        self.expression = expression

    def to_dict(self):
        return {
            "nt": "uminus",
            "expression": self.expression.to_dict()
        }

    def __str__(self):
        return str(self.to_dict())


class Print:
    def __init__(self, type, value):
        self.type = type.split('_')[-1]  # Obtém o último elemento após dividir a string pelo '_'
        self.value = value

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            "nt": "print",
            "type": self.type,
            "value": self.value.to_dict()
        }

program = {
    "nt": "program",
    "global_vars": [
        {
            "nt": "vardecl",
            "modifier": "val",
            "name": "final_number",
            "type": "int",
            "initializer": {
                "nt": "int",
                "value": "16"
            }
        }
    ],
    "functions": [
        {
            "nt": "functiondecl",
            "name": "fizzBuzz",
            "parameters": [
                {
                    "modifier": "val",
                    "name": "number",
                    "type": "int"
                }
            ],
            "type": "None",
            "body": [
                {
                    "nt": "vardecl",
                    "modifier": "var",
                    "name": "temp",
                    "type": "int",
                    "initializer": {
                        "nt": "int",
                        "value": "1"
                    }
                },
                {
                    "nt": "while",
                    "condition": {
                        "nt": "expression",
                        "operator": "<=",
                        "left": "temp",
                        "right": "number"
                    },
                    "body": [
                        {
                            "nt": "if",
                            "condition": {
                                "nt": "expression",
                                "operator": "&&",
                                "left": {
                                    "nt": "expression",
                                    "operator": "=",
                                    "left": {
                                        "nt": "expression",
                                        "operator": "%",
                                        "left": "temp",
                                        "right": {
                                            "nt": "int",
                                            "value": "3"
                                        }
                                    },
                                    "right": {
                                        "nt": "int",
                                        "value": "0"
                                    }
                                },
                                "right": {
                                    "nt": "expression",
                                    "operator": "=",
                                    "left": {
                                        "nt": "expression",
                                        "operator": "%",
                                        "left": "temp",
                                        "right": {
                                            "nt": "int",
                                            "value": "5"
                                        }
                                    },
                                    "right": {
                                        "nt": "int",
                                        "value": "0"
                                    }
                                }
                            },
                            "if": [
                                {
                                    "nt": "print",
                                    "type": "string",
                                    "value": {
                                        "nt": "string",
                                        "value": "\"FizzBuzz\""
                                    }
                                }
                            ],
                            "else": [
                                {
                                    "nt": "if",
                                    "condition": {
                                        "nt": "expression",
                                        "operator": "=",
                                        "left": {
                                            "nt": "expression",
                                            "operator": "%",
                                            "left": "temp",
                                            "right": {
                                                "nt": "int",
                                                "value": "3"
                                            }
                                        },
                                        "right": {
                                            "nt": "int",
                                            "value": "0"
                                        }
                                    },
                                    "if": [
                                        {
                                            "nt": "print",
                                            "type": "string",
                                            "value": {
                                                "nt": "string",
                                                "value": "\"Fizz\""
                                            }
                                        }
                                    ],
                                    "else": [
                                        {
                                            "nt": "if",
                                            "condition": {
                                                "nt": "expression",
                                                "operator": "=",
                                                "left": {
                                                    "nt": "expression",
                                                    "operator": "%",
                                                    "left": "temp",
                                                    "right": {
                                                        "nt": "int",
                                                        "value": "5"
                                                    }
                                                },
                                                "right": {
                                                    "nt": "int",
                                                    "value": "0"
                                                }
                                            },
                                            "if": [
                                                {
                                                    "nt": "print",
                                                    "type": "string",
                                                    "value": {
                                                        "nt": "string",
                                                        "value": "\"Buzz\""
                                                    }
                                                }
                                            ],
                                            "else": [
                                                {
                                                    "nt": "print",
                                                    "type": "int",
                                                    "value": "temp"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "nt": "assignment",
                            "name": "temp",
                            "expression": {
                                "nt": "expression",
                                "operator": "+",
                                "left": "temp",
                                "right": {
                                    "nt": "int",
                                    "value": "1"
                                }
                            }
                        }
                    ]
                }
            ]
        },
        {
            "nt": "functiondecl",
            "name": "main",
            "parameters": [
                {
                    "modifier": "val",
                    "name": "args",
                    "type": "arraystring"
                }
            ],
            "type": "None",
            "body": [
                {
                    "nt": "functioncallinline",
                    "name": "fizzBuzz",
                    "parameter_list": [
                        "final_number"
                    ]
                }
            ]
        }
    ]
}



class Context:
    def __init__(self):
        self.globals = {}
        self.locals = []
        self.functions = {}
        self.return_value = None

    def enter_function(self):
        self.locals.append({})

    def exit_function(self):
        self.locals.pop()

    def set_variable(self, name, value, is_global=False):
        if is_global or not self.locals:
            self.globals[name] = value
        else:
            self.locals[-1][name] = value

    def get_variable(self, name):
        for scope in reversed(self.locals):
            if name in scope:
                return scope[name]
        if name in self.globals:
            return self.globals[name]
        raise KeyError(f"Variable '{name}' not found")

    def define_function(self, name, func):
        self.functions[name] = func

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        else:
            raise KeyError(f"Function '{name}' not found")

    def set_return_value(self, value):
        self.return_value = value

    def get_return_value(self):
        return self.return_value
    
    def enter_scope(self):
        self.locals.append({})

    def exit_scope(self):
        self.locals.pop()
    
    def is_global_variable(self, name):
        return name in self.globals
    
    def get_locals(self):
        return self.locals




def interpretador(ctx, node):
    node_type = node["nt"]
    print(f"Entering node type: {node_type}")
##############################################
    if node_type == "program":
        # Interpretar as declarações de variáveis globais
        for decl in node["global_vars"]:
            if decl["nt"] == "vardecl":
                name = decl["name"]
                initializer = decl["initializer"]
                ctx.set_variable(name, interpretador(ctx, initializer), is_global=True)
            elif decl["nt"] == "functiondecl":
                name = decl["name"]
                ctx.define_function(name, decl)

        # Armazenar as declarações de funções no contexto
        for func in node["functions"]:
            name = func["name"]
            ctx.define_function(name, func)

        # Chamar a função 'main' se ela estiver definida
        if "main" in ctx.functions:
            main_func = ctx.get_function("main")

            ctx.enter_function()
            for stmt in main_func["body"]:
                interpretador(ctx, stmt)

            ctx.exit_function()
            print(str(ctx.get_return_value()))


##############################################
    elif node_type == "functiondecl":
        # Preparação para executar a função
        ctx.enter_function()
        # Executar o corpo da função
        for stmt in node["body"]:
            interpretador(ctx, stmt)
        ctx.exit_function()


##############################################
    elif node_type == "vardecl":
        name = node["name"]

        print("locals " + str(ctx.get_locals()))
        value = interpretador(ctx, node["initializer"])

        is_global = ctx.is_global_variable(name)
        ctx.set_variable(name, value, is_global)


##############################################
    elif node_type == "while":
        print("Starting while loop...")
        ctx.enter_scope()
        while interpretador(ctx, node["condition"]):
            for expr in node["body"]:
                interpretador(ctx, expr)
            
        ctx.exit_scope()
        print("Exiting while loop.")


##############################################
    elif node_type == "if":

        condition = node["condition"]
        if_true = node["if"]
        if_false = node["else"]

        condition_result = interpretador(ctx, condition)

        if condition_result:  # Se a condição é verdadeira
            ctx.enter_scope()
            for stmt in if_true:
                interpretador(ctx, stmt
                              )
            ctx.exit_scope()
        elif isinstance(if_false, list):  # Se a condição é falsa e existe um bloco else válido
            ctx.enter_scope()
            for stmt in if_false:
                interpretador(ctx, stmt)
            ctx.exit_scope()


##############################################
    elif node_type == "print":
        if isinstance(node["value"], dict) and "nt" in node["value"]:
            value = interpretador(ctx, node["value"])
        else:
            value = ctx.get_variable(node["value"])
        print(f"Print statement: {value}")


##############################################
    elif node_type == "expression":

        operator = node["operator"]
        if isinstance(node["left"], dict) and "nt" in node["left"]:
            
            left = interpretador(ctx, node["left"])
        else:
            left = ctx.get_variable(node["left"])
            
        if isinstance(node["right"], dict) and "nt" in node["right"]:
            right = interpretador(ctx, node["right"])
        else:
            right = ctx.get_variable(node["right"])
            
        if operator == "^":
            return left ** right
        elif operator == ">":
            return left > right
        elif operator == "<":
            return left < right
        elif operator == ">=":
            return left >= right
        elif operator == "<=":
            return left <= right
        elif operator == "=":
            return left == right
        elif operator == "!=":
            return left != right
        elif operator == "&&":
            return left and right
        elif operator == "||":
            return left or right
        elif operator == "!":
            return not left
        elif operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            return left / right
        elif operator == "%":
            return left % right
        else:
            raise ValueError(f"Operador desconhecido: {operator}")


##############################################
    elif node_type == "assignment":
        name = node["name"]
        if isinstance(node["expression"], dict) and "nt" in node["expression"]:
            new_value = interpretador(ctx, node["expression"])
        else:
            new_value = ctx.get_variable(node["expression"])

        if name in ctx.functions:
            ctx.set_return_value(new_value)
        else:
            is_global = ctx.is_global_variable(name)
            ctx.set_variable(name, new_value, is_global)


##############################################
    elif node_type == "functioncallinline":
        fun = ctx.get_function(node["name"])

        ctx.enter_function()
        params = fun["parameters"]
        args = node.get("parameter_list", [])

        for param, arg in zip(params, args):
            arg_value = ctx.get_variable(arg)
            print(f"Setting function parameter {param['name']} to {arg_value}")
            ctx.set_variable(param["name"], arg_value)

       
        for stmt in fun["body"]:
            interpretador(ctx, stmt)

        returnValue = ctx.get_return_value()
        ctx.exit_function()

        return returnValue


##############################################
    elif node_type == "int":
        return int(node["value"])
    elif node_type == "float":
        return float(node["value"])   
    elif node_type == "string":
        return node["value"]
    elif node_type == "float":
        return float(node["value"])
    elif node_type == "arrayint":
        return node["value"]
    elif node_type == "arrayint2":
        return node["value"]
    elif node_type == "void":
        return node["value"]
    elif node_type == "boolean":
        return node["value"]

    else:
        raise Exception("Oops, not implemented yet: {}".format(node_type))
    print(f"Exiting node type: {node_type}")


interpretador(Context(), program)

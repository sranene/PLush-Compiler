RETURN_CODE = "$ret"

class TypeError(Exception):
    pass

class Context(object):
    def __init__(self):
        self.stack = [{}]
    
    def get_type(self, name):
        for scope in self.stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variable {name} is not in the context.")
    
    def set_type(self, name, value, modifier = "None"):
        scope = self.stack[0]
        scope[name] = (value, modifier)

    def has_var(self, name):
        for scope in self.stack:
            if name in scope:
                return True
        return False

    def has_var_in_current_scope(self, name):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop(0)


def verify(ctx: Context, node, indent=""):
##############################################
    if node["nt"] == "program":

        # Double pass. primeiro assinatura, depois verificacao
        for decl in node["global_vars"]:
            if decl["nt"] != "vardecl":
                name = decl["name"]
                if ctx.has_var(name):
                    raise TypeError(f"Function with the name '{name}' already exists in the context.")
                
                assinatura = (decl["type"], [par["type"] for par in decl["parameters"] if decl["parameters"] != "None"])
                ctx.set_type(name, assinatura)
                #print(f"{indent}Função '{name}' adicionada ao contexto.")

        for decl in node["global_vars"]:
            if decl["nt"] != "vardecl":
                verify(ctx, decl, indent + "  ")

        for decl in node["global_vars"]:
            if decl["nt"] != "functiondecl":
                verify(ctx, decl, indent + "  ")

        # Double pass. primeiro assinatura, depois verificacao
        for fun in node["functions"]:
            name = fun["name"]
            if ctx.has_var(name):
                raise TypeError(f"Function with the name '{name}' already exists in the context.")

            assinatura = (fun["type"], [par["type"] for par in fun["parameters"]] if fun["parameters"] != "None" else None)
            ctx.set_type(name, assinatura)
            #print(f"{indent}Função '{name}' adicionada ao contexto.")

        for fun in node["functions"]:
            verify(ctx, fun, indent + "  ")


##############################################
    elif node["nt"] == "vardecl":
        name = node["name"]
        modifier = node["modifier"]
        declared_type = node["type"]

        if ctx.has_var(name):
            raise TypeError(f"Variable {name} does not exist.")
        
        initializer_type = None

        if isinstance(node["initializer"], dict) and "nt" in node["initializer"]:
            if node["initializer"]["nt"] in ["functioncallinline", "expression"]:
                initializer_type = verify(ctx, node["initializer"])
            else:
                initializer_type = node["initializer"]["nt"]
        else:
            initializer_type = ctx.get_type(node["initializer"])[0]

        if declared_type != initializer_type:
            raise TypeError(f"Variable '{name}' type declared as '{declared_type}', but initialized with type '{initializer_type}'.")
        

        ctx.set_type(name, declared_type, modifier)
        #print(f"{indent}Variável '{name}' adicionada ao contexto com tipo {declared_type}.")


##############################################
    elif node["nt"] == "functiondecl":
       
        ctx.enter_scope()
        #print(f"{indent}Verificando declaração da função '{node['name']}'...")
        return_type = node["type"]

        if return_type != None:
            ctx.set_type(RETURN_CODE, return_type)
        else:
            ctx.set_type(RETURN_CODE, None)

        parameters = node.get("parameters", [])
        if parameters != "None":
            for par in parameters:
                ctx.set_type(par["name"], par["type"])
        else:
            ctx.set_type("None", "None")
        
        if node["body"] != "None" and node["body"] != None:
            if return_type != None and return_type != "void" and return_type != "None":
                function_name = node['name']
                has_return_statement = False
                for st in node["body"]:
                    verify(ctx, st, indent + "  ")
                    
                    if st["nt"] == "assignment":
                        if st["name"] == node['name']:
                            has_return_statement = True
                            break
                        
                if not has_return_statement:
                    raise TypeError(f"Function '{function_name}' return type declared as '{return_type}' does not have a return statement.")
            else:
                for st in node["body"]:
                    verify(ctx, st, indent + "  ")
        
        ctx.exit_scope()


##############################################
    elif node["nt"] == "functioncallinline":
        name = node["name"]
        
        if not ctx.has_var(name):
            raise TypeError(f"Function '{name}' does not exist.")

        function_signature = ctx.get_type(name)[0]
        if (node["parameter_list"] == "None" or node["parameter_list"] is None) and (function_signature[1] == [] or function_signature[1] is None):
            pass  # Ambos os parâmetros e a assinatura são None, então está tudo bem
        elif (node["parameter_list"] != "None" and node["parameter_list"] is not None) and (function_signature[1] != [] and function_signature[1] is not None):
            if len(node["parameter_list"]) != len(function_signature[1]):
                raise TypeError(f"Function call '{name}': incorrect number of parameters.")

            for param, expected_type in zip(node["parameter_list"], function_signature[1]):
                param_type = ctx.get_type(param)[0]
                if param_type != expected_type:
                    raise TypeError(f"Function call '{name}': parameter type '{param_type}' does not match the expected '{expected_type}'.")
        else:
            raise TypeError("Function signature and parameter list must both be specified or both be None.")

        return function_signature[0]


##############################################
    elif node["nt"] == "arraycallinline":
        name = node["name"]

        if not ctx.has_var(name):
            raise TypeError(f"Array variable '{name}' does not exist.")

        array_type = ctx.get_type(name)[0]
        first_index = ctx.get_type(node["first_index"])[0]
        second_index = ctx.get_type(node.get("second_index", None))[0]

        if first_index != 'int' or second_index != 'int':
            raise TypeError("Array indices must be integers.")
        return array_type


##############################################
    elif node["nt"] == "print":
        var_name = node["value"]
        print_type = node["type"]

        if isinstance(node["value"], dict):
            value_type = node["value"]["nt"]
        elif ctx.has_var(var_name):
            value_type = ctx.get_type(var_name)[0]
        else:
            raise TypeError(f"Variable '{var_name}' does not exist.")

        if print_type != value_type:
            raise TypeError(f"Value type '{value_type}' differs from print command expected type '{print_type}'.")
        
        
##############################################
    elif node["nt"] == "expression":
        operator = node["operator"]
        zeroFlag = False
        if isinstance(node["left"], dict) and "nt" in node["left"]:
            if node["left"]["nt"] in ["expression", "functioncallinline", "arraycallinline", "parenteses"]:
                left_type = verify(ctx, node["left"], indent)
            else:
                left_type = node["left"]["nt"] 
        else:
            left_var = node["left"]
            if ctx.has_var(left_var):
                left_type = ctx.get_type(left_var)[0]
            else:
                raise TypeError(f"Variable '{left_var}' does not exist.")
            
        if isinstance(node["right"], dict) and "nt" in node["right"]:
            if node["right"]["nt"] in ["expression", "functioncallinline", "arraycallinline", "parenteses"]:
                right_type = verify(ctx, node["right"], indent)
            else:
                right_type = node["right"]["nt"]
                if float(node["right"]["value"]) == 0.0:
                    zeroFlag = True   
        else:
            right_var = node["right"]
            if ctx.has_var(right_var):
                right_type = ctx.get_type(right_var)[0]
            else:
                raise TypeError(f"Variable '{right_var}' does not exist.")
        

        if left_type != right_type:
                raise TypeError(f"Operation '{operator}' not supported between different types '{left_type}' and '{right_type}'")


        if operator == '^':
            if left_type in ['int', 'float']:
                return left_type
            else:
                raise TypeError(f"Exponentiation operation not supported for types '{left_type}' and '{right_type}'")
        if operator == '%':
            if left_type in ['int', 'float']:
                return left_type
            else:
                raise TypeError(f"Modulus operation not supported for types '{left_type}' and '{right_type}'")
        if operator in ['>', '>=', '<', '<=', '=', '!=']:
            if left_type in ['int', 'float', 'boolean', 'arrayint2', 'arrayint']:
                return 'boolean'
            elif left_type == 'string':
                if operator in ['=', '!=']:
                    return 'boolean'
                else:
                    raise TypeError(f"Comparison operation '{operator}' not supported for types '{left_type}' and '{right_type}'")
            else:
                raise TypeError(f"Comparison operation '{operator}' not supported for types '{left_type}' and '{right_type}'")
            
        if operator in ['+', '-', '*', '/']:
            if zeroFlag is True and operator == '/':
                raise TypeError(f"Division by zero operation not supported: {left_type} {operator} 0")
            if left_type in ['int', 'float']:
                return left_type
            else:
                raise TypeError(f"Arithmetic operation '{operator}' not supported for types '{left_type}' and '{right_type}'")
        if operator == '&&' or operator == '||':
            if left_type == 'boolean':
                return 'boolean'
            else:
                raise TypeError(f"Logical operation '{operator}' requires both operands to be boolean, but found '{left_type}' and '{right_type}'")


##############################################
    elif node["nt"] == "parenteses":
        if isinstance(node["value"], dict) and "nt" in node["value"]:
            if node["value"]["nt"] in ["expression", "functioncallinline", "arraycallinline", "parenteses"]:
                type = verify(ctx, node["value"], indent)
            else:
                type = node["value"]
        else:
            var = node["value"]
            if ctx.has_var(var):
                type = ctx.get_type(var)[0]
            else:
                raise TypeError(f"Variable '{var}' does not exist.")
            
        return type
    

##############################################
    elif node["nt"] == "if":
        
        condition_type = verify(ctx, node["condition"], indent)
        if condition_type != "boolean":
            raise TypeError(f"The condition expression of the 'if' statement must be of type 'boolean', but type '{condition_type}' was found.")
        
        ctx.enter_scope()
        for st in node["if"]:
            verify(ctx, st, indent + "  ")
        ctx.exit_scope()

        if node["else"] is not None and node["else"] != "None":
            ctx.enter_scope()
            for st in node["else"]:
                verify(ctx, st, indent + "  ")
            ctx.exit_scope()


##############################################
    elif node["nt"] == "while":
        
        condition_type = verify(ctx, node["condition"], indent)
        if condition_type != "boolean":
            raise TypeError(f"The condition expression of the 'while' statement must be of type 'boolean', but type '{condition_type}' was found.")
        
        ctx.enter_scope()
        for st in node["body"]:
            verify(ctx, st, indent + "  ")
        ctx.exit_scope()


##############################################       
    elif node["nt"] == "assignment":
        name = node["name"]
        var_type = ""
        if isinstance(name, dict) and "nt" in name:
            
            if name["nt"] == "arraycallinline":

                if not ctx.has_var(name["name"]):
                    raise TypeError(f"Variable '{name}' does not exist.")
                
                var_type = ctx.get_type(name["name"])[0]

        else:
            if not ctx.has_var(name):
                raise TypeError(f"Variable '{name}' does not exist.")
            
            modifier = ctx.get_type(name)[1]
            if modifier == "val":
                raise TypeError(f"Cannot modify variable '{name}' declared with 'val'.")
            
            temp = ctx.get_type(name)[0]
            if isinstance(temp, tuple):
                var_type = temp[0]  # Função
            else:
                var_type = temp  # Variável

            expression = node["expression"]
            if isinstance(expression, dict) and "nt" in expression:
                if expression["nt"] == "expression":
                    expression_type = verify(ctx, expression, indent)
                else:                   
                    expression_type = expression["nt"]
            else:               
                expression_type = ctx.get_type(expression)[0]
            
            if var_type != expression_type:
                raise TypeError(f"Assignment to variable '{name}' expects a value of type '{var_type}', but a value of type '{expression_type}' was provided.")

##############################################    
    else:
        t = node["nt"]
        print(f"{indent}Oops, not implemented yet: '{t}'.")

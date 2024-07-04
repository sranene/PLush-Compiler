
class Context:
    def __init__(self):
        self.globals = {}
        self.locals = []
        self.functions = {}

    def enter_function(self):
        """Enter a new function scope, adding a new local scope."""
        self.locals.append({})

    def exit_function(self):
        """Exit the current function scope, removing the latest local scope."""
        self.locals.pop()

    def set_variable(self, name, ptr, var_type, is_global=False):
        """Set a variable in the appropriate scope (global or local)."""
        if is_global or not self.locals:
            self.globals[name] = (ptr, var_type)
        else:
            self.locals[-1][name] = (ptr, var_type)

    def get_variable(self, name):
        """Get a variable from the appropriate scope (local or global)."""
        for scope in reversed(self.locals):
            if name in scope:
                return scope[name]
        if name in self.globals:
            return self.globals[name]
        raise KeyError(f"Variable '{name}' not found")

    def define_function(self, name, ret_type, params=[], ret_value=None):
        """Define a function with the given name, return type, and parameters."""
        self.functions[name] = (ret_type, params, ret_value)

    def set_return_function(self, name, ret_value):
        """Define the return value for the function with the given name."""
        if name in self.functions:
            ret_type, params, _ = self.functions[name]
            self.functions[name] = (ret_type, params, ret_value)
        else:
            raise KeyError(f"Function '{name}' not defined")

    def get_function(self, name):
        """Get a function definition by name."""
        if name in self.functions:
            return self.functions[name]
        else:
            return

    def is_global_variable(self, name):
        """Check if a variable is global."""
        return name in self.globals



class Emitter:
    def __init__(self):
        self.count = 0
        self.lines = []
        self.context = Context()
        self.dwglobals = False

    def get_count(self):
        self.count += 1
        return self.count

    def get_id(self):
        id = self.get_count()
        return f"cas_{id}"

    def __lshift__(self, v):
        self.lines.append(v)

    def get_label(self):
        id = self.get_count()
        return f"label{id}"

    def get_code(self):
        return "\n".join(self.lines)

    def get_pointer_name(self, var_name):
        if var_name in self.context.globals:
            return f'@{var_name}'
        else:
            return f"%pont_{var_name}"
    
    def new_temp_reg(self):
        return f"%ind{self.get_count()}"

    def declare_variable(self, var_name, var_type, is_global=False):
        """Declare a new variable and store it in the context."""
        if is_global:
            pointer_name = f'@{var_name}'
        else:
            pointer_name = f"%pont_{var_name}"
        
        self.context.set_variable(var_name, pointer_name, var_type, is_global)

    def get_dealing_with_globals(self):
        return self.dwglobals

    def set_dealing_with_globals(self):
        self.dwglobals = not self.dwglobals


def map_type_to_llvm(high_level_type):
    type_mapping = {
        "int": "i32",
        "char": "i8",
        "float": "float",
        "double": "double",
        "bool": "i1",
        "None": "void",
        "string": "i8*",  
        "arrayint": "[10 x i32]",
        "arrayint2": "[10 x [10 x i32]]",
        "arraystring": "[10 x i8]*"
    }
    return type_mapping.get(high_level_type, "void") 


def compilador(node, emitter=None):
    if emitter is None:
        emitter = Emitter()
    
    #print("NODE: " + str(node))
    node_type = node["nt"]
    

######################################################
    if node["nt"] == "program":
        emitter << "declare i32 @printf(i8*, ...) #1"
        # Functions from functions.c
        emitter.lines.insert(0, 'declare void @print_int(i32)')
        emitter.lines.insert(0, 'declare void @print_string(i8*)')
        emitter.lines.insert(0, 'declare void @print_arrayint([10 x i32]*)')
        emitter.lines.insert(0, 'declare void @print_float(float)')

        # Globals including variables and functions FFI
        emitter.set_dealing_with_globals()
        for decl in node["global_vars"]:
            if decl["nt"] == "vardecl":
                compilador(decl, emitter)
            elif decl["nt"] == "functiondecl":
                name = decl["name"]
                ret_type = map_type_to_llvm(decl["type"])
                if decl["parameters"] == "None":
                    param_list = ""
                else:
                    param_types = [map_type_to_llvm(param["type"]) for param in decl["parameters"]]
                    param_list = ", ".join(param_types)
                emitter.context.define_function(name, ret_type, decl["parameters"])
                emitter << f"declare {ret_type} @{name}({param_list})"
        emitter.set_dealing_with_globals()

        # Adding functions in the context
        for func in node["functions"]:
            func_name = func["name"]
            ret_type = map_type_to_llvm(func["type"])
            parameters = func["parameters"]
            emitter.context.define_function(func_name, ret_type, parameters)

        # Compile function main first
        main_function = next((func for func in node["functions"] if func["name"] == "main"), None)
        if main_function:
            compilador(main_function, emitter)
        
        # Compile rest of the functions
        for func in node["functions"]:
            if func["name"] != "main":
                compilador(func, emitter)

        return emitter.get_code()

    
######################################################
    elif node_type == "functiondecl":
        func_name = node["name"]
        ret_type = map_type_to_llvm(node["type"])

        parameters = node["parameters"]

        # Function signature
        if isinstance(parameters, list):
            param_list = ', '.join(f"{map_type_to_llvm(p['type'])} %{p['name']}" for p in parameters)
        else:
            param_list = ""

        emitter << f"define {ret_type} @{func_name}({param_list}) {{"
        
        emitter.context.enter_function()

        # Parameters as local variables
        if isinstance(parameters, list):
            for param in parameters:
                param_name = param["name"]
                param_type = map_type_to_llvm(param["type"])
                
                emitter.declare_variable(param_name, param_type)
                ptr_name = emitter.get_pointer_name(param_name)
                emitter << f"   {ptr_name} = alloca {param_type}"
                emitter << f"   store {param_type} %{param_name}, {param_type}* {ptr_name}"


        # Compile body of the function
        for statement in node["body"]:
            compilador(statement, emitter)
        
        if ret_type == "void":
            emitter << "ret void"
        else:
            _, _, ret_value = emitter.context.get_function(func_name)
            emitter << f"ret {ret_type} {ret_value}"

        emitter << "}"
        
        emitter.context.exit_function()


######################################################
    elif node["nt"] == "vardecl":
        name = node["name"]
        initializer = node["initializer"]
        var_type = map_type_to_llvm(node["type"])
        isGlobal = emitter.get_dealing_with_globals()
        emitter.declare_variable(name, var_type, is_global=isGlobal)

        if isGlobal: # Global variables 
            if "value" in initializer:
                emitter << f"@{name} = global {var_type} {initializer['value']}"
            else:
                reg, var_type = compilador(initializer, emitter)
                emitter << f"@{name} = global {var_type} {reg}"

        else:  # Local variables
            size = ""
            if node["type"] == "arrayint":
                size = ", i32 10"
            pname = emitter.get_pointer_name(name)
            emitter << f"   {pname} = alloca {var_type}{size}"

            if isinstance(initializer, str):
                reg_value = emitter.get_pointer_name(initializer)
                reg_loaded = "%" + emitter.get_id()
                emitter << f"   {reg_loaded} = load {var_type}, {var_type}* {reg_value}"
                emitter << f"   store {var_type} {reg_loaded}, {var_type}* {pname}"
            else:
                reg, _ = compilador(initializer, emitter)
                emitter << f"   store {var_type} {reg}, {var_type}* {pname}"


######################################################
    elif node["nt"] == "if":
        condition = node["condition"]
        if_true = node["if"]
        if_false = node["else"]

        cond_result, _ = compilador(condition, emitter)
        true_label = emitter.get_id()
        false_label = emitter.get_id()
        end_label = emitter.get_id()

        emitter << f"   br i1 {cond_result}, label %{true_label}, label %{false_label}"
        emitter << f"{true_label}:"

        for stmt in if_true:
            compilador(stmt, emitter)

        emitter << f"   br label %{end_label}"
        emitter << f"{false_label}:"
        
        if isinstance(if_false, list):
            for stmt in if_false:
                compilador(stmt, emitter)
        elif if_false != "None":
            raise ValueError("Unexpected type for 'else' clause")
        
        emitter << f"   br label %{end_label}"
        emitter << f"{end_label}:"


######################################################
    elif node["nt"] == "expression":
        operator = node["operator"]

        # Left side of the expression
        if isinstance(node["left"], dict) and "nt" in node["left"]:
            left_reg, left_type = compilador(node["left"], emitter)
        else:
            left_ptr_name = emitter.get_pointer_name(node["left"])
            _ , left_type = emitter.context.get_variable(node["left"])
            left_reg = "%" + emitter.get_id()
            emitter << f"   {left_reg} = load {left_type}, {left_type}* {left_ptr_name}"

        # Right side of the expression
        if isinstance(node["right"], dict) and "nt" in node["right"]:
            right_reg, right_type = compilador(node["right"], emitter)
        else:
            right_ptr_name = emitter.get_pointer_name(node["right"])
            _ , right_type = emitter.context.get_variable(node["right"])
            right_reg = "%" + emitter.get_id()
            emitter << f"   {right_reg} = load {right_type}, {right_type}* {right_ptr_name}"
        

        if left_type.endswith("*"):
            deref_left_reg = "%" + emitter.get_id()
            left_type = left_type[:-1]  # Remove
            emitter << f"   {deref_left_reg} = load {left_type}, {left_type}* {left_reg}"
            left_reg = deref_left_reg

        if right_type.endswith("*"):
            deref_right_reg = "%" + emitter.get_id()
            right_type = right_type[:-1]  # Remove
            emitter << f"   {deref_right_reg} = load {right_type}, {right_type}* {right_reg}"
            right_reg = deref_right_reg

        # left_type and right_type are always equal
        reg = "%" + emitter.get_id()

        if left_type == "i32":
            if operator == "^":
                if right_reg == "2":  # Verificar se o expoente é 2
                    emitter << f"   {reg} = mul i32 {left_reg}, {left_reg}"
                else:
                    raise NotImplementedError("General integer power not implemented")

            elif operator == ">":
                emitter << f"   {reg} = icmp sgt i32 {left_reg}, {right_reg}"
            elif operator == "<":
                emitter << f"   {reg} = icmp slt i32 {left_reg}, {right_reg}"
            elif operator == ">=":
                emitter << f"   {reg} = icmp sge i32 {left_reg}, {right_reg}"
            elif operator == "<=":
                emitter << f"   {reg} = icmp sle i32 {left_reg}, {right_reg}"
            elif operator == "=":
                emitter << f"   {reg} = icmp eq i32 {left_reg}, {right_reg}"
            elif operator == "!=":
                emitter << f"   {reg} = icmp ne i32 {left_reg}, {right_reg}"
            elif operator == "&&":
                emitter << f"   {reg} = and i1 {left_reg}, {right_reg}"  # Boolean operation
            elif operator == "||":
                emitter << f"   {reg} = or i1 {left_reg}, {right_reg}"   # Boolean operation
            elif operator == "+":
                emitter << f"   {reg} = add nsw i32 {left_reg}, {right_reg}"
            elif operator == "-":
                emitter << f"   {reg} = sub nsw i32 {left_reg}, {right_reg}"
            elif operator == "*":
                emitter << f"   {reg} = mul nsw i32 {left_reg}, {right_reg}"
            elif operator == "/":
                emitter << f"   {reg} = sdiv i32 {left_reg}, {right_reg}"
            elif operator == "%":
                emitter << f"   {reg} = srem i32 {left_reg}, {right_reg}"
            else:
                raise ValueError(f"Unknown operator: {operator}")
        elif left_type == "float":
            if operator == ">":
                emitter << f"   {reg} = fcmp ogt float {left_reg}, {right_reg}"
            elif operator == "<":
                emitter << f"   {reg} = fcmp olt float {left_reg}, {right_reg}"
            elif operator == ">=":
                emitter << f"   {reg} = fcmp oge float {left_reg}, {right_reg}"
            elif operator == "<=":
                emitter << f"   {reg} = fcmp ole float {left_reg}, {right_reg}"
            elif operator == "=":
                emitter << f"   {reg} = fcmp oeq float {left_reg}, {right_reg}"
            elif operator == "!=":
                emitter << f"   {reg} = fcmp one float {left_reg}, {right_reg}"
            elif operator == "&&":
                emitter << f"   {reg} = and i1 {left_reg}, {right_reg}"  # Boolean operation
            elif operator == "||":
                emitter << f"   {reg} = or i1 {left_reg}, {right_reg}"   # Boolean operation
            elif operator == "+":
                emitter << f"   {reg} = fadd float {left_reg}, {right_reg}"
            elif operator == "-":
                emitter << f"   {reg} = fsub float {left_reg}, {right_reg}"
            elif operator == "*":
                emitter << f"   {reg} = fmul float {left_reg}, {right_reg}"
            elif operator == "/":
                emitter << f"   {reg} = fdiv float {left_reg}, {right_reg}"
            elif operator == "%":
                emitter << f"   {reg} = frem float {left_reg}, {right_reg}"
            else:
                raise ValueError(f"Unknown operator: {operator}")
        else:
            raise TypeError(f"Unknown type: {left_type}")

        return reg, right_type


######################################################
    elif node["nt"] == "parenteses":
            # Priority
            return compilador(node["value"], emitter)


######################################################
    elif node["nt"] == "assignment":
        variable_name = node["name"]
        value_node = node["expression"]

        if isinstance(variable_name, dict) and "nt" in variable_name:
            # arraycallinline
            index, _ = compilador(variable_name, emitter)
            reg, type = compilador(value_node, emitter)
            emitter << f"   store {type} {reg}, {type}* {index}"
            
        elif variable_name in emitter.context.functions:
            # RETURN
            if isinstance(value_node, dict) and "nt" in value_node:
                return_reg, _ = compilador(value_node, emitter)
            else:
                if isinstance(value_node, str):
                    if emitter.context.is_global_variable(value_node):
                        reg_value = "@" + value_node
                        value_type = emitter.context.globals[value_node][1]
                    else:
                        reg_value, value_type = emitter.context.get_variable(value_node)
                    reg_loaded = "%" + emitter.get_id()
                    emitter << f"   {reg_loaded} = load {value_type}, {value_type}* {reg_value}"
                    return_reg = reg_loaded
                else:
                    return_reg = value_node

            emitter.context.set_return_function(variable_name, return_reg)
        else:
            # Normal variable
            var_pointer, var_type = emitter.context.get_variable(variable_name)
            pname = emitter.get_pointer_name(variable_name)

            if isinstance(value_node, str):
                reg_loaded = "%" + emitter.get_id()
                if emitter.context.is_global_variable(value_node):
                    value_pointer = "@" + value_node
                    value_type = emitter.context.globals[value_node][1]
                else:
                    value_pointer, value_type = emitter.context.get_variable(value_node)
                emitter << f"   {reg_loaded} = load {value_type}, {value_type}* {value_pointer}"  # Carrega o valor da variável
                emitter << f"   store {var_type} {reg_loaded}, {var_type}* {pname}"  # Armazena o valor na nova variável
            else:
                reg, _ = compilador(value_node, emitter)
                emitter << f"   store {var_type} {reg}, {var_type}* {pname}"


######################################################
    elif node_type == "functioncallinline":
        func_name = node["name"]
        param_list = node["parameter_list"]

        if param_list is None or param_list == "None":
            param_list = []

        func_def = emitter.context.get_function(func_name)
        ret_type = func_def[0]

        params = []
        for param in param_list:
            if isinstance(param, dict) and "nt" in param:
                param_value, param_type = compilador(param, emitter)
            else:
                param_ptr_name, param_type = emitter.context.get_variable(param)
                param_value = "%" + emitter.get_id()
                emitter << f"   {param_value} = load {param_type}, {param_type}* {param_ptr_name}"

            params.append(f"{param_type} {param_value}")

        param_str = ', '.join(params)
        if ret_type == "void":
            emitter << f"   call {ret_type} @{func_name}({param_str})"
            return None, ret_type
        else:
            reg = "%" + emitter.get_id()
            emitter << f"   {reg} = call {ret_type} @{func_name}({param_str})"
            return reg, ret_type


######################################################
    elif node_type == "arraycallinline":
        array_name = node["name"]
        first_index = node["first_index"]
        second_index = node.get("second_index")  # Might not exist

        # First index
        if isinstance(first_index, dict) and "nt" in first_index:
            first_index_value, first_index_type = compilador(first_index, emitter)
        else:
            first_index_ptr_name, first_index_type = emitter.context.get_variable(first_index)
            first_index_value = "%" + emitter.get_id()
            emitter << f"   {first_index_value} = load {first_index_type}, {first_index_type}* {first_index_ptr_name}"

        # Second index
        if second_index:
            if isinstance(second_index, dict) and "nt" in second_index:
                second_index_value, second_index_type = compilador(second_index, emitter)
            else:
                second_index_ptr_name, second_index_type = emitter.context.get_variable(second_index)
                second_index_value = "%" + emitter.get_id()
                emitter << f"   {second_index_value} = load {second_index_type}, {second_index_type}* {second_index_ptr_name}"

            # Adress of first index
            internal_array_ptr = "%" + emitter.get_id()
            ptr_name = emitter.get_pointer_name(array_name)
            emitter << f"   {internal_array_ptr} = getelementptr inbounds [10 x [10 x i32]], [10 x [10 x i32]]* {ptr_name}, i32 0, i32 {first_index_value}"

            # Adress of second index
            element_ptr = "%" + emitter.get_id()
            emitter << f"   {element_ptr} = getelementptr inbounds [10 x i32], [10 x i32]* {internal_array_ptr}, i32 0, i32 {second_index_value}"

            return element_ptr, "i32*"
        else:
            # Second index does not exist
            element_ptr = "%" + emitter.get_id()
            ptr_name = emitter.get_pointer_name(array_name)
            emitter << f"   {element_ptr} = getelementptr inbounds [10 x i32], [10 x i32]* {ptr_name}, i32 0, i32 {first_index_value}"

            return element_ptr, "i32*"


######################################################
    elif node["nt"] == "print":
        value_node = node["value"]
        value_type = map_type_to_llvm(node["type"])

        if isinstance(value_node, dict) and "nt" in value_node:
            var_ptr, value_type = compilador(value_node, emitter)
        else:
            var_ptr = emitter.context.get_variable(value_node)[0]
            value_type = emitter.context.get_variable(value_node)[1]  
            value = "%" + emitter.get_id()
            emitter << f"   {value} = load {value_type}, {value_type}* {var_ptr}" 
            
        if value_type == "[10 x i32]":
            emitter << f"   call void @print_arrayint([10 x i32]* {var_ptr})"

        elif value_type == "i32":
            emitter << f"   call void @print_int(i32 {value})"

        elif value_type == "i8*":
            str_name = f"@.casual_str_{emitter.get_id()}"
            string_value = var_ptr.strip('"') 
            string_length = len(string_value) + 1
            str_decl = f"""{str_name} = private unnamed_addr constant [{string_length} x i8] c"{string_value}\\00", align 1"""
            emitter.lines.insert(0, str_decl)
            nreg = "%" + emitter.get_id()
            emitter << f"   {nreg} = getelementptr inbounds [{string_length} x i8], [{string_length} x i8]* {str_name}, i64 0, i64 0"
            emitter << f"   call void @print_string(i8* {nreg})"

        elif value_type == "float":
            float_value = "%" + emitter.get_id()
            emitter << f"   {float_value} = load float, float* {var_ptr}"
            emitter << f"   call void @print_float(float {float_value})"

        else:
            raise ValueError(f"Unsupported print type: {value_type}")


######################################################
    elif node_type == "while":
        loop_start_label = emitter.get_label()
        loop_body_label = emitter.get_label()
        loop_end_label = emitter.get_label()

        emitter << f"br label %{loop_start_label}"
        emitter << f"{loop_start_label}:"

        condition_reg, _ = compilador(node["condition"], emitter)

        emitter << f"br i1 {condition_reg}, label %{loop_body_label}, label %{loop_end_label}"
        emitter << f"{loop_body_label}:"

        for statement in node["body"]:
            compilador(statement, emitter)

        emitter << f"br label %{loop_start_label}"
        emitter << f"{loop_end_label}:"


######################################################
    elif node["nt"] in {"int", "string", "float", "arrayint", "arrayint2", "void", "boolean"}:
        return node["value"], map_type_to_llvm(node["nt"])


######################################################
    else:
        raise Exception("Oops, not implemented yet: {}".format(node_type))

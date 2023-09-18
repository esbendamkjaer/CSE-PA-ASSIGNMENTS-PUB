from assignment03.folds.syntax_fold import SyntaxFold
from assignment03.models.class_diagram.access_modifiers import AccessModifier
from assignment03.models.class_diagram.field_model import FieldModel
from assignment03.models.class_diagram.method_model import MethodModel


class ClassFold(SyntaxFold):
    def default(self, node, results, path):
        def res(class_object: tuple):
            for fun in results:
                class_object = fun(class_object)

            return class_object

        return res

    def visit_interfaces(self, node, results, path):
        def interfaces(class_object: tuple):
            (dependencies, interfaces, fields, methods, compositions) = class_object

            for interface in node["interfaces"]:
                interfaces.add(interface["name"])

            return class_object

        return interfaces

    def get_deps(self, node, results, path):
        def deps(class_object: tuple):
            (dependencies, interfaces, fields, methods, compositions) = class_object

            if node is None:
                return class_object

            if "name" in node and "/" in node["name"] and not node["name"] == "java/lang/Object":
                dependencies.add(node["name"])

            return class_object

        return deps

    def visit_ref(self, node, results, path):
        return self.get_deps(node["ref"], results, path)

    def visit_type(self, node, results, path):
        return self.get_deps(node["type"], results, path)

    def visit_fields(self, node, results, path):
        def fields(class_object: tuple):
            (dependencies, interfaces, fields, methods, compositions) = class_object

            for field in node["fields"]:
                field_model = FieldModel(field["name"])

                modifier = AccessModifier.DEFAULT
                if "access" in field and field["access"]:
                    if "public" in field["access"]:
                        modifier = AccessModifier.PUBLIC
                    elif "protected" in field["access"]:
                        modifier = AccessModifier.PROTECTED
                    elif "private" in field["access"]:
                        modifier = AccessModifier.PRIVATE
                field_model.access_modifier = modifier

                if "name" in field["type"]:
                    field_model.type_name = field["type"]["name"].split("/")[-1]
                elif "base" in field["type"]:
                    field_model.type_name = field["type"]["base"]

                fields.add(field_model)

            return class_object

        return fields

    def visit_methods(self, node, results, path):
        def methods(class_object: tuple):
            (dependencies, interfaces, fields, methods, compositions) = class_object

            for method in node["methods"]:
                method_model = MethodModel(method["name"])

                modifier = AccessModifier.DEFAULT
                if "access" in method and method["access"]:
                    if "public" in method["access"]:
                        modifier = AccessModifier.PUBLIC
                    elif "protected" in method["access"]:
                        modifier = AccessModifier.PROTECTED
                    elif "private" in method["access"]:
                        modifier = AccessModifier.PRIVATE
                method_model.access_modifier = modifier

                if method["returns"]["type"]:
                    if "name" in method["returns"]["type"]:
                        method_model.return_type = method["returns"]["type"]["name"].split("/")[-1]
                    elif "base" in method["returns"]["type"]:
                        method_model.return_type = method["returns"]["type"]["base"]
                else:
                    method_model.return_type = "void"

                for parameter in method["params"]:
                    if "type" in parameter and "type" in parameter["type"] and "name" in parameter["type"]["type"]:
                        method_model.parameter_types.append(parameter["type"]["type"]["name"].split("/")[-1])
                        print(parameter["type"]["type"]["name"].split("/")[-1])

                print(method_model.parameter_types)
                methods.add(method_model)

            return class_object

        return methods

    def visit_innerclasses(self, node, results, path):
        def innerclasses(class_object: tuple):
            (dependencies, interfaces, fields, methods, compositions) = class_object

            for composition in node["innerclasses"]:
                if composition["class"] == node["name"]:
                    compositions.add(composition["outer"])

            return class_object

        return innerclasses

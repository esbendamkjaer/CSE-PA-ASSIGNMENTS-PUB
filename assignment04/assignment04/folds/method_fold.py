from assignment04.folds.syntax_fold import SyntaxFold


class MethodFold(SyntaxFold):
    def default(self, node, results, path):
        def res(obj: dict):
            for fun in results:
                obj = fun(obj)

            return obj

        return res

    def visit_methods(self, node, results, path):
        def methods(obj: dict):
            for method in node["methods"]:
                annotations = method["annotations"]

                if any(
                        annotation["type"] == "dtu/compute/exec/Case"
                        for annotation in annotations
                ):
                    obj[method["name"]] = method["code"]

        return methods

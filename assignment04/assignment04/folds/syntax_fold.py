class SyntaxFold:
    def visit(self, node: any, path=None):
        if path is None:
            path = []

        results = []
        if isinstance(node, dict):
            for key, value in node.items():
                results.append(self.visit(value, path + [key]))

                attr_name = 'visit_' + key
                if hasattr(self, attr_name) and callable(getattr(self, attr_name)):
                    result = getattr(self, attr_name)(node, results, path)
                    results.append(result)
        elif isinstance(node, list):
            results = []
            for i, item in enumerate(node):
                result = self.visit(item, path + [i])
                results.append(result)

        return self.default(node, results, path)

    def default(self, node, results, path):
        raise NotImplementedError


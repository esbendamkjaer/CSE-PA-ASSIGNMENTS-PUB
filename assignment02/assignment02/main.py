import glob
from typing import Generic, TypeVar

import graphviz
from graphviz import Digraph
from tree_sitter import Language, Parser, Node

JAVA_LANG = None


class SyntaxFold:
    def visit(self, node: Node):
        results = [self.visit(child) for child in node.children]
        if hasattr(self, node.type):
            return getattr(self, node.type)(node, results)
        else:
            return self.default(node, results)

    def default(self, node: Node, results: list):
        raise NotImplementedError


class Printer(SyntaxFold):
    def default(self, node: Node, results: list):
        print(node.type)


class TypeIdentifiers(SyntaxFold):
    def default(self, node: Node, results: list):
        return set().union(*results)

    def type_identifier(self, node: Node, results: list):
        return {node.text}


class MethodDeclarations(SyntaxFold):
    def default(self, node: Node, results: list):
        return set().union(*results)

    def method_declaration(self, node: Node, results: list):
        tp = node.child_by_field_name("type_parameters")
        if tp is None:
            return super().default(node, results)
        else:
            nids = Identifiers().visit(tp)
            return results + [nids]


class ImportDeclarations(SyntaxFold):
    def default(self, node: Node, results: list):
        return set().union(*results)

    def import_declaration(self, node: Node, results: list):
        return {node.children[0].text}


class Identifiers(SyntaxFold):
    def default(self, node: Node, results: list):
        return set().union(*results)

    def identifier(self, node: Node, results: list):
        return {node.text}


class ContextSensitive(SyntaxFold):
    def type_identifier(self, node: Node, results: list):
        def ret(ids):
            if node.text in ids:
                return set()
            else:
                return {node.text}

        return ret

    def method_declaration(self, node: Node, results: list):
        tp = node.child_by_field_name("type_parameters")
        if tp is None:
            print("no type parameters")
            return self.default(node, results)
        else:
            print("type parameters")
            nids = Identifiers().visit(tp)
            print(nids)

            def ret(ids):
                return {node.text: self.default(node, results)(ids | nids)}

            return ret

    def default(self, node: Node, results: list):
        def ret(ids):
            return set().union(*[r(ids) for r in results])

        return ret


class PackageDeclarations(SyntaxFold):
    def default(self, node: Node, results: list):
        return set().union(*results)

    def package_declaration(self, node: Node, results: list):
        child_types = [child.type for child in node.children]
        print(child_types)
        return {node.children[1].text}


class ClassDeclarations(SyntaxFold):
    def default(self, node: Node, results: list):
        return set().union(*results)

    def class_declaration(self, node: Node, results: list):
        return {f'{node.child_by_field_name("name").text}'}


def main():
    working_dir = "../examples/src/dependencies/java/dtu"
    files = find_all_java_files_from_root(working_dir)
    print("Files found. Parsing...")
    print(files)

    parser = Parser()
    parser.set_language(JAVA_LANG)

    classDiagram = ClassDiagram()

    for file in files[1:2]:
        print(file)
        file_contents = read_file_contents(file)
        tree = parser.parse(bytes(file_contents, "utf8"))

        #Printer().visit(tree.root_node)

        print("Class declarations:")
        print(ClassDeclarations().visit(tree.root_node))

        print("Package declarations:")
        print(PackageDeclarations().visit(tree.root_node))
        # print(MethodDeclarations().visit(tree.root_node))

        print("Type identifiers:")
        #print(TypeIdentifiers().visit(tree.root_node))

        # print(ImportDeclarations().visit(tree.root_node))
        print("Context sensitive:")
        #print(ContextSensitive().visit(tree.root_node)(set()))
        print(tree.root_node.sexp())


def find_all_java_files_from_root(root: str) -> list[str]:
    files = glob.glob(root + "/**/*.java", recursive=True)
    return files


def read_file_contents(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, data: T):
        self.data = data


class ClassModel():
    def __init__(self, name: str):
        self.package = None
        self.name = name
        self.methods = []
        self.fields = []


class Edge(Generic[T]):
    def __init__(self, source: Node[T], target: Node[T]):
        self.source = source
        self.target = target
        self.relationship = None


class Graph(Generic[T]):
    def __init__(self, nodes: set[Node[T]] = {}, edges: set[Edge[T]] = {}):
        self.nodes = nodes
        self.edges = edges

    def add_node(self, node: Node[T]):
        self.nodes.add(node)

    def add_edge(self, edge: Edge[T]):
        self.edges.add(edge)

    def get_node(self, data: T) -> Node[T] | None:
        for node in self.nodes:
            if node.data == data:
                return node
        return None

    def get_edges(self, node: Node[T]) -> list[Edge[T]]:
        return [edge for edge in self.edges if edge.source == node]


class ClassDiagram(Graph[ClassModel]):
    def to_dot(self) -> Digraph:
        dot = graphviz.Digraph()

        for node in self.nodes:
            dot.node(f'{node.data.package} {node.data.name}')
        for edge in self.edges:
            dot.edge(
                edge.source.data.name, edge.target.data.name,
                label=edge.relationship
            )
        return dot

    def render(self, outfile: str = "diagram.svg"):
        dot = self.to_dot()
        dot.render(outfile=outfile, format="svg", view=True)


if __name__ == "__main__":
    print("Starting lexer...")
    main()
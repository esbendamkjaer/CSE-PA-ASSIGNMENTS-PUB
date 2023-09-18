import html

from assignment03.models.class_diagram.class_model import ClassModel
from assignment03.models.graph.edge import Edge
from assignment03.models.graph.graph import Graph
from graphviz import Digraph

from assignment03.models.graph.node import Node
from assignment03.models.class_diagram.relationships import ClassRelationship


class ClassDiagram(Graph[ClassModel]):
    def to_dot(self) -> Digraph:
        dot = Digraph()

        relationship_mapping = {
            ClassRelationship.COMPOSITION: "diamond",
            ClassRelationship.AGGREGATION: "odiamond",
            ClassRelationship.REALIZATION: "onormal",
            ClassRelationship.INHERITANCE: "onormal",
            ClassRelationship.USES: "vee",
        }

        for node in self.nodes:
            name = html.escape(node.data.name)
            fields = [html.escape(str(field)) for field in node.data.fields]

            methods = [html.escape(str(method)) for method in node.data.methods]

            field_map = map(lambda field: f'<tr><td align="left">{field}</td></tr>', fields)
            fields = "".join(field_map)

            method_map = map(lambda method: f'<tr><td align="left">{method}</td></tr>', methods)
            methods = "".join(method_map)

            fields = f'''<table align="left" border="0" cellborder="0" cellspacing="0">{fields}</table>''' if fields else ""
            methods = f'''<table align="left" border="0" cellborder="0" cellspacing="0">{methods}</table>''' if methods else ""

            dot.node(
                name=f'{node.data.name}',
                shape="plain",
                label=f'''<
<table border="0" cellborder="1" cellspacing="0" cellpadding="4">
    <tr><td>{name}</td></tr>
    <tr><td>{fields}</td></tr>
    <tr><td>{methods}</td></tr>
</table>>''')

        for edge in self.edges:
            dot.edge(
                edge.source.data.name, edge.target.data.name,
                label=edge.relationship.value,
                style="dashed" if edge.relationship == ClassRelationship.REALIZATION
                                  or edge.relationship == ClassRelationship.USES else "solid",
                arrowhead=relationship_mapping[edge.relationship],
            )
        return dot

    def add_class(self, class_model: ClassModel):
        self.add_node(Node(class_model))

    def add_relationship(self, source: ClassModel, target: ClassModel, relationship: ClassRelationship):
        edge = Edge(Node(source), Node(target))
        edge.relationship = relationship

        self.add_edge(
            edge
        )

    def render(self, outfile: str = "diagram.svg"):
        dot = self.to_dot()
        dot.render(outfile=outfile, format="svg", view=False)

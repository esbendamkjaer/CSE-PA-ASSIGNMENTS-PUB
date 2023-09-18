from assignment03.models.class_diagram.field_model import FieldModel
from assignment03.models.class_diagram.method_model import MethodModel


class ClassModel:
    def __init__(self, name):
        self.name: str = name
        self.methods: [MethodModel] = []
        self.fields: [FieldModel] = []

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
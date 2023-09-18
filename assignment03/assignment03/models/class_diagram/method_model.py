from assignment03.models.class_diagram.access_modifiers import AccessModifier


class MethodModel:
    def __init__(
            self,
            name,
            return_type="void",
            parameter_types=[],
            access_modifier=AccessModifier.DEFAULT
    ):
        self.name: str = name
        self.return_type: str = return_type
        self.parameter_types: [str] = parameter_types
        self.access_modifier: AccessModifier = access_modifier

    def __str__(self):
        return f"{self.access_modifier.value} {self.name}({', '.join(self.parameter_types)}): {self.return_type}"

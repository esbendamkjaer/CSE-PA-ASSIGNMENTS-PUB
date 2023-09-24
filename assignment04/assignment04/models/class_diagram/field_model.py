from assignment04.models.class_diagram.access_modifiers import AccessModifier


class FieldModel:
    def __init__(
            self, name,
            type_name=None,
            access_modifier=AccessModifier.DEFAULT
    ):
        self.name: str = name
        self.type_name: str = type_name
        self.access_modifier: AccessModifier = access_modifier

    def __str__(self):
        return f"{self.access_modifier.value} {self.name}: {self.type_name}"

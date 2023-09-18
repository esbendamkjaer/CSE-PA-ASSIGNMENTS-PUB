import glob
import json
import subprocess

from assignment03.folds.class_fold import ClassFold
from assignment03.models.class_diagram.class_diagram import ClassDiagram
from assignment03.models.class_diagram.class_model import ClassModel
from assignment03.models.class_diagram.relationships import ClassRelationship


def main() -> None:
    directory = "../../testclassfiles"
    files = find_all_class_files_from_root(directory)

    class_diagram = ClassDiagram()

    for file in files:
        json_output = file_to_json(file)
        analyze_json(json_output, class_diagram)

    class_diagram.render()


def file_to_json(file: str) -> dict:
    json_output = subprocess.check_output(["jvm2json", "-s", file])
    json_output = json.loads(json_output.strip())
    return json_output


def analyze_json(json_output: dict, class_diagram: ClassDiagram) -> None:
    class_name = json_output["name"]

    class_model = ClassModel(class_name)
    class_diagram.add_class(class_model)

    dependencies, interfaces, fields, methods, compositions = (set(), set(), set(), set(), set())

    ClassFold().visit(json_output)((dependencies, interfaces, fields, methods, compositions))

    class_model.methods.extend(methods)
    class_model.fields.extend(fields)

    for composition in compositions:
        target = ClassModel(composition)

        class_diagram.add_relationship(
            class_model, target, ClassRelationship.COMPOSITION
        )

    for interface in interfaces:
        target = ClassModel(interface)

        class_diagram.add_relationship(
            class_model, target, ClassRelationship.REALIZATION
        )


    for dependency in dependencies:
        target = ClassModel(dependency)

        class_diagram.add_relationship(
            class_model, target, ClassRelationship.USES
        )




def find_all_class_files_from_root(root: str) -> list[str]:
    files = glob.glob(root + "/**/*.class", recursive=True)
    return files


if __name__ == "__main__":
    main()

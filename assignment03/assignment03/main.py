import glob
import json
import subprocess
import random
import string

from assignment03.folds.class_fold import ClassFold
from assignment03.models.class_diagram.class_diagram import ClassDiagram
from assignment03.models.class_diagram.class_model import ClassModel
from assignment03.models.class_diagram.relationships import ClassRelationship


def main() -> None:

    jarFile = "../../testclassfiles/HelperBot.jar"

    # generate random number
    random_string = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=8))

    extract_jar(jarFile, "/tmp/"+random_string)
    files = find_all_class_files_from_root("/tmp/"+random_string)

    print("Done extracting jar file.")

    totalFiles = len(files)
    current = 0

    class_diagram = ClassDiagram()

    for file in files:
        current += 1
        json_output = file_to_json(file)
        analyze_json(json_output, class_diagram)
        print("Analyzed file " + str(current) + " of " + str(totalFiles) + " (" + str(current/totalFiles*100) + "%)")

    print("Done analyzing json files.")

    class_diagram.render("diagram.svg")

    print("Done rendering class diagram.")


def file_to_json(file: str) -> dict:
    pwd = subprocess.check_output(["pwd"])
    pwd = pwd.replace(b"\n", b"").decode("utf-8")
    fileName = file.split("/")[-1]
    filePath = "/".join(file.split("/")[:-1])
    json_output = subprocess.check_output([
        "docker",
        "run",
        "--rm",
        "-v", filePath+':/opt/build/data',
        "amatzen/jvm2json",
        "-s", "data/"+fileName
    ])
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


def extract_jar(jarFile: str, directory: str) -> None:
    subprocess.run(["unzip", jarFile, "-d", directory])


def find_all_class_files_from_root(root: str) -> list[str]:
    files = glob.glob(root + "/**/*.class", recursive=True)
    return files


if __name__ == "__main__":
    main()

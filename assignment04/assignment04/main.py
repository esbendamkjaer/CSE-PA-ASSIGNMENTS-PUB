import glob
import json
import subprocess

from assignment04.folds.method_fold import MethodFold
from assignment04.interpreter.bytecodeinterpreter import BytecodeInterpreter


def main() -> None:
    files = find_files_by_extension_from_root("../../examples/decompiled/dtu/compute/exec/", "json")

    totalFiles = len(files)
    current = 0

    program = {}
    for file in files:
        current += 1
        json_output = file_to_json(file)
        (class_name, methods) = analyze_json(json_output)
        program[class_name] = methods
        print("Analyzed file " + str(current) + " of " + str(totalFiles) + " (" + str(current / totalFiles * 100) + "%)")

    cases = [
        # (("dtu/compute/exec/Simple", "noop"), []),
        # (("dtu/compute/exec/Simple", "zero"), []),
        # (("dtu/compute/exec/Simple", "hundredAndTwo"), []),
        # (("dtu/compute/exec/Simple", "identity"), [42]),
        # (("dtu/compute/exec/Simple", "add"), [4, 5]),
        (("dtu/compute/exec/Simple", "min"), [4, 5]),
        # (("dtu/compute/exec/Simple", "factorial"), [4]),
        # (("dtu/compute/exec/Calls", "fib"), [10]),
        # (("dtu/compute/exec/Array", "newArray"), []),
        # (("dtu/compute/exec/Array", "first"), [[10, 4, 5]]),
        # (("dtu/compute/exec/Array", "access"), [1, [10, 4, 5]]),
    ]

    for (method, args) in cases:
        print(f"Running method ({method}) with args ({args})")
        bi = BytecodeInterpreter(method, args)
        output = bi.run(program)
        print(f"Output: {output}")


def class_file_to_json(file: str) -> dict:
    json_output = subprocess.check_output(["jvm2json", "-s", file])
    json_output = json.loads(json_output.strip())
    return json_output


def file_to_json(file: str) -> dict:
    string = read_file(file)
    json_output = string_to_json(string)
    return json_output


def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read()


def string_to_json(string: str) -> dict:
    json_output = json.loads(string.strip())
    return json_output


def analyze_json(json_output: dict):
    class_name = json_output["name"]

    methods: dict[str, dict[str, any]] = {}
    MethodFold().visit(json_output)(methods)

    return class_name, methods


def extract_jar(jarFile: str, directory: str) -> None:
    subprocess.run(["unzip", jarFile, "-d", directory])


def find_files_by_extension_from_root(root: str, extension: str) -> list[str]:
    files = glob.glob(root + f"/**/*.{extension}", recursive=True)
    return files


if __name__ == "__main__":
    main()

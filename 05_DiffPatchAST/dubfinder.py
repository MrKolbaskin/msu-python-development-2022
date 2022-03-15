from argparse import ArgumentParser
from difflib import SequenceMatcher
from importlib import import_module
from inspect import getmembers, isclass, isfunction, getsource
import ast
from textwrap import dedent

ATTRIBUTES = {"name", "id", "arg", "attr"}
EMPTY_ATTRIBUTE = "_"
MIN_RATIO = 0.95


def parse_module(module, path="") -> None:
    res = {}
    for member_name, member in getmembers(module):
        if isclass(member):
            if not member_name.startswith("__"):
                res.update(parse_module(member, f"{path}.{member_name}"))

        if isfunction(member):
            src = getsource(member)
            parse_tree = ast.parse(dedent(src))

            for node in ast.walk(parse_tree):
                for attr in ATTRIBUTES:
                    if hasattr(node, attr):
                        setattr(node, attr, EMPTY_ATTRIBUTE)

            res[f"{path}.{member_name}"] = ast.unparse(parse_tree)

    return res


def parse_modules(modules):
    functions = {}

    for module in modules:
        functions.update(parse_module(import_module(module), module))

    return functions


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("modules", help="Modules to inspect", nargs="+", type=str)

    args = parser.parse_args()

    functions = parse_modules(args.modules)
    function_names = sorted(functions.keys())

    for index, first_function_name in enumerate(function_names):
        for second_function_name in function_names[index + 1 :]:

            ratio = SequenceMatcher(
                None,
                functions[first_function_name],
                functions[second_function_name],
            ).ratio()
            if ratio > MIN_RATIO:
                print(first_function_name, ":", second_function_name)

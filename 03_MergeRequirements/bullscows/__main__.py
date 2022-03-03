from argparse import ArgumentParser
from pathlib import Path
from typing import List
from urllib.request import urlopen

from .gameplay import gameplay


def parse_dict(text: str, length: int):
    return [line for line in text.splitlines() if len(line) == length]


def ask(prompt: str, valid: List[str] = None) -> str:
    while True:
        input_word = input(prompt)
        if not valid or input_word in valid:
            break

    return input_word


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def read_dictionary(args) -> List[str]:
    path = Path(args.dictionary)
    if path.exists():
        with open(path, "r") as f:
            words = parse_dict(f.read(), args.len)
    else:
        text = urlopen(args.dictionary).read().decode()
        words = parse_dict(text, args.len)

    return words


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("dictionary", help="Dictionary (File path or URL)")
    parser.add_argument(
        "-l",
        "--len",
        help="Words length",
        type=int,
        default=5,
    )

    args = parser.parse_args()
    words = read_dictionary(args)

    attempts = gameplay(ask, inform, words)
    print("Количетсво попыток:", attempts)

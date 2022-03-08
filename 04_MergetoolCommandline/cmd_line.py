from __future__ import generators
import cmd
from typing import List

from pynames import GENDER, LANGUAGE
import pynames.generators as generators

GENERATORS = {
    "scandinavian": generators.scandinavian.ScandinavianNamesGenerator(),
    "russian": generators.russian.PaganNamesGenerator(),
    "mongolian": generators.mongolian.MongolianNamesGenerator(),
    "korean": generators.korean.KoreanNamesGenerator(),
    "elven dnd": generators.elven.DnDNamesGenerator(),
    "elven warhammer": generators.elven.WarhammerNamesGenerator(),
    "goblins": generators.goblin.GoblinGenerator(),
    "orcs": generators.orc.OrcNamesGenerator(),
    "iron_kingdoms caspian": generators.iron_kingdoms.CaspianMidlunderSuleseFullnameGenerator(),
    "iron_kingdoms dwarf": generators.iron_kingdoms.DwarfFullnameGenerator(),
    "iron_kingdoms gobber": generators.iron_kingdoms.GobberFullnameGenerator(),
    "iron_kingdoms iossan": generators.iron_kingdoms.IossanNyssFullnameGenerator(),
    "iron_kingdoms khadoran": generators.iron_kingdoms.KhadoranFullnameGenerator(),
    "iron_kingdoms ogrun": generators.iron_kingdoms.OgrunFullnameGenerator(),
    "iron_kingdoms ryn": generators.iron_kingdoms.RynFullnameGenerator(),
    "iron_kingdoms thurian": generators.iron_kingdoms.ThurianMorridaneFullnameGenerator(),
    "iron_kingdoms tordoran": generators.iron_kingdoms.TordoranFullnameGenerator(),
    "iron_kingdoms trollkin": generators.iron_kingdoms.TrollkinFullnameGenerator(),
}


class InvalidCommand(Exception):
    message = "Invalid Command"


class InvalidGenerator(Exception):
    message = "Invalid Generator"


class InvalidGender(Exception):
    message = "Invalid Gender"


class CommandLine(cmd.Cmd):
    language = LANGUAGE.NATIVE

    GENDERS = {"male": GENDER.MALE, "female": GENDER.FEMALE}

    def do_language(self, lang: str) -> None:
        if lang.lower() not in LANGUAGE.ALL:
            self.language = LANGUAGE.NATIVE
        else:
            self.language = lang

    def complete_language(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ) -> List[str]:
        return [lang for lang in LANGUAGE.ALL if lang.startswith(text)]

    def do_generate(self, args: str) -> None:
        try:
            self._generate_handler(*self._parse_arg(args))
        except (InvalidCommand, InvalidGenerator, InvalidGender) as e:
            print(e.message)

    def _generate_handler(self, generator_name: str, gender: str = "male") -> None:
        if generator_name not in GENERATORS:
            raise InvalidGenerator
        generator = GENERATORS[generator_name]

        if gender not in self.GENDERS:
            raise InvalidGender
        gender = self.GENDERS[gender]

        if self.language in generator.languages:
            name = generator.get_name_simple(gender, self.language)
        else:
            name = generator.get_name_simple(gender, LANGUAGE.NATIVE)
        print(name)

    def complete_generate(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ) -> List[str]:
        return self._complete_handler(
            "generate", text, line, begidx, additional_parameters=self.GENDERS.keys()
        )

    def do_info(self, args: str) -> None:
        try:
            self._info_handler(*self._parse_arg(args))
        except (InvalidCommand, InvalidGenerator) as e:
            print(e.message)

    def _info_handler(self, generator_name: str, arg: str = "all") -> None:
        if generator_name not in GENERATORS:
            raise InvalidGenerator

        generator = GENERATORS[generator_name]

        if arg == "language":
            print(*generator.languages)
        else:
            gender = self.GENDERS.get(arg, GENDER.ALL)
            print(generator.get_names_number(gender))

    def complete_info(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ) -> List[str]:
        return self._complete_handler("info", text, line, begidx)

    def _complete_handler(
        self,
        command: str,
        text: str,
        line: str,
        begidx: int,
        additional_parameters: List[str] = ["male", "female", "language"],
    ) -> List[str]:
        word_count = len(line[:begidx].split())

        if word_count == 1:
            return [generator for generator in GENERATORS if generator.startswith(text)]

        if word_count == 2 and line.startswith(f"{command} elven"):
            return [
                generator.split()[-1]
                for generator in GENERATORS
                if generator.startswith(f"elven {text}")
            ]

        if word_count == 2 and line.startswith(f"{command} iron_kingdoms"):
            return [
                generator.split()[-1]
                for generator in GENERATORS
                if generator.startswith(f"iron_kingdoms {text}")
            ]

        return [gender for gender in additional_parameters if gender.startswith(text)]

    def _parse_arg(self, args: str) -> List[str]:
        if args in GENERATORS:
            res = [args]
        else:
            res = args.rsplit(maxsplit=1)
            if len(res) != 2:
                raise InvalidCommand

        return res

    def do_quit(self, args: str) -> None:
        self._quit_handler()
        return True

    def do_EOF(self, args: str) -> None:
        self._quit_handler()
        return True

    def _quit_handler(self) -> None:
        print()
        print("Bye!")


if __name__ == "__main__":
    try:
        CommandLine().cmdloop()
    except KeyboardInterrupt:
        print()
        print("Bye!")

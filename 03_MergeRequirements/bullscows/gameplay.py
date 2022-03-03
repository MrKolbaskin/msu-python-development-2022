from random import choice
from typing import List

from .bullscows import bullscows


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    secret, attempts = choice(words), 0
    while True:

        guess = ask("Введите слово: ", words)
        attempts += 1
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)

        if guess == secret:
            break

    return attempts

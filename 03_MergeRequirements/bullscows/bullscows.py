from typing import Tuple

import textdistance


def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    return textdistance.hamming.similarity(guess, secret), textdistance.bag.similarity(
        guess, secret
    )

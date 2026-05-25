"""
Author: Mohamadamin Kazemi
Date: 2024-05-25
Title: Password Generator
Description: A Python module for generating secure and memorable passwords using various strategies.
"""

from __future__ import annotations

import random
import string
from abc import ABC, abstractmethod
from typing import Sequence

import nltk

WORD_LIST = nltk.corpus.words.words()


class PasswordGenerator(ABC):
    """Abstract base class for password generators."""

    @abstractmethod
    def generate(self) -> str:
        """Generate a password.

        :returns: Generated password string.
        """
        raise NotImplementedError


class PinGenerator(PasswordGenerator):
    """Generate numeric PIN codes."""

    def __init__(self, length: int) -> None:
        """Initialize the PIN generator.

        :param length: Length of the PIN.
        """
        self.length = length

    def generate(self) -> str:
        """Generate a random numeric PIN.

        :returns: Randomly generated PIN.
        """
        return "".join(random.choices(string.digits, k=self.length))


class RandomPasswordGenerator(PasswordGenerator):
    """Generate random passwords using configurable character sets."""

    def __init__(
        self,
        length: int = 10,
        include_numbers: bool = True,
        include_symbols: bool = True,
    ) -> None:
        """Initialize the random password generator.

        :param length: Length of the password.
        :param include_numbers: Include digits in the password.
        :param include_symbols: Include punctuation symbols in the password.
        """
        characters = string.ascii_letters

        if include_numbers:
            characters += string.digits

        if include_symbols:
            characters += string.punctuation

        self.length = length
        self.characters = characters

    def generate(self) -> str:
        """Generate a random password.

        :returns: Randomly generated password.
        """
        return "".join(random.choices(self.characters, k=self.length))


class MemorablePasswordGenerator(PasswordGenerator):
    """Generate memorable passwords from random words."""

    def __init__(
        self,
        number_of_words: int = 4,
        separator: str = "-",
        capitalization: bool = False,
        vocabulary: Sequence[str] | None = None,
    ) -> None:
        """Initialize the memorable password generator.

        :param number_of_words: Number of words in the password.
        :param separator: Separator between words.
        :param capitalization: Randomly capitalize words.
        :param vocabulary: Custom vocabulary list.
        """
        self.number_of_words = number_of_words
        self.separator = separator
        self.capitalization = capitalization
        self.vocabulary = vocabulary or WORD_LIST

    def generate(self) -> str:
        """Generate a memorable password.

        :returns: Memorable password string.
        """
        words = random.choices(self.vocabulary, k=self.number_of_words)

        if self.capitalization:
            words = [
                word.upper() if random.choice((True, False)) else word.lower()
                for word in words
            ]

        return self.separator.join(words)


def main() -> None:
    """Run password generator examples."""
    pin_generator = PinGenerator(length=6)
    print(f"Generated PIN: {pin_generator.generate()}")

    random_password_generator = RandomPasswordGenerator(
        length=12,
        include_numbers=True,
        include_symbols=True,
    )
    print(
        f"Generated Random Password: "
        f"{random_password_generator.generate()}"
    )

    memorable_password_generator = MemorablePasswordGenerator(
        number_of_words=4,
        separator="-",
        capitalization=True,
    )
    print(
        f"Generated Memorable Password: "
        f"{memorable_password_generator.generate()}"
    )


if __name__ == "__main__":
    main()

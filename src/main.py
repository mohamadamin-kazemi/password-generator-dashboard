
"""
Author: Mohamadamin Kazemi
Date: 2024-05-25
Title: Password Generator
Description: A Streamlit application for generating secure and memorable passwords.
"""


from __future__ import annotations

import re
import streamlit as st


from password_generators import (
    MemorablePasswordGenerator,
    PinGenerator,
    RandomPasswordGenerator,
)


def password_strength(password: str) -> int:
    """Calculate the strength score of a password.

    The score is based on password length and character diversity.

    :param password: Password to evaluate.

    :return: Password strength score between 0 and 100.
    """
    score = 0

    length_rules = (
        (8, 20),
        (12, 20),
        (16, 10),
    )

    for min_length, points in length_rules:
        if len(password) >= min_length:
            score += points

    patterns = {
        r"[a-z]": 10,
        r"[A-Z]": 15,
        r"\d": 15,
        r'[!@#$%^&*(),.?":{}|<>_\-]': 20,
    }

    score += sum(
        points
        for pattern, points in patterns.items()
        if re.search(pattern, password)
    )

    return min(score, 100)


def show_strength(password: str) -> None:
    """Display the password strength in the Streamlit UI.

    :param password: Password to evaluate and display.
    """
    strength = password_strength(password)

    st.write("### 🔐 Password Strength")
    st.progress(strength / 100)
    st.metric("Score", f"{strength}/100")

    if strength < 40:
        st.error("Weak password ❌")
    elif strength < 70:
        st.warning("Medium strength ⚠️")
    else:
        st.success("Strong password ✅")


def generate_pin() -> None:
    """Render the PIN code generator section."""
    length = st.slider("Select PIN length:", 4, 32, 10)

    if st.button("Generate PIN"):
        pin = PinGenerator(length=length).generate()

        st.code(pin)
        show_strength(pin)


def generate_random_password() -> None:
    """Render the random password generator section."""
    length = st.slider("Select password length:", 8, 64, 16)
    include_numbers = st.checkbox("Include numbers")
    include_symbols = st.checkbox("Include symbols")

    if st.button("Generate Password"):
        password = RandomPasswordGenerator(
            length=length,
            include_numbers=include_numbers,
            include_symbols=include_symbols,
        ).generate()

        st.code(password)
        show_strength(password)


def generate_memorable_password() -> None:
    """Render the memorable password generator section."""
    number_of_words = st.slider("Number of words:", 2, 10, 4)
    separator = st.text_input("Separator:", "-")
    capitalization = st.checkbox("Random capitalization")

    if st.button("Generate Password"):
        password = MemorablePasswordGenerator(
            number_of_words=number_of_words,
            separator=separator,
            capitalization=capitalization,
        ).generate()

        st.code(password)
        show_strength(password)


def main() -> None:
    """Run the Streamlit password generator application."""
    st.set_page_config(page_title="Password Generator", page_icon="🔐")

    st.image(
        "/Users/mohammadaminkazemi/my_project/python_project/"
        "password-generator-dashboard/images/banner.jpg"
    )

    st.title("Password Generator 🔐")

    option = st.radio(
        "Select password type:",
        ("PIN Code", "Random Password", "Memorable Password"),
    )

    generators = {
        "PIN Code": generate_pin,
        "Random Password": generate_random_password,
        "Memorable Password": generate_memorable_password,
    }

    generators[option]()


if __name__ == "__main__":
    main()

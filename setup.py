"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from setuptools import setup, find_packages

setup(
    name="ciel",
    version="0.1.0",
    packages=find_packages(exclude=("ext", "ext.*")),
    install_requires=["numpy", "scipy", "matplotlib", "networkx", "sympy", "pandas"],
    description="CIEL — Consciousness-Integrated Emergent Logic (organized from project drafts)",
    author="Adrian Lipa",
    license="CIEL-Research-NonCommercial-1.1",
)

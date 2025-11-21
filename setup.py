"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from setuptools import find_packages, setup


setup(
    name="ciel",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["numpy", "scipy", "matplotlib", "networkx", "sympy", "pandas"],
    entry_points={
        "console_scripts": [
            "ciel-engine=ciel.cli:run_engine",
            "ciel-smoke=ciel.cli:smoke_test",
        ]
    },
    description="CIEL — Consciousness-Integrated Emergent Logic (organized from project drafts)",
    author="Adrian Lipa",
    license="CIEL-Research-NonCommercial-1.1",
)

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

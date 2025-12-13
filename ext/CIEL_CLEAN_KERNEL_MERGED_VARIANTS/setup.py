from setuptools import setup, find_packages

setup(
    name="ciel-kernel",
    version="0.1.0",
    author="Adrian Lipa",
    description="CIEL/Ω clean kernel: zunifikowane stałe + orkiestrator.",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy",
    ],
    include_package_data=True,
)

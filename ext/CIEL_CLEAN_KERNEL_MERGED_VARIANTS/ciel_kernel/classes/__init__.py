"""Podstawowe klasy modułów CIEL.

Tutaj zaczyna się biblioteka konkretnych modułów, np.:
- pola falowe,
- pamięć,
- operator intencji,
- warstwy EEG/EM,
- itp.
"""

from .base import BaseCIELModule
# Generated modules from ext1–21, extemot, extfwcku
from . import generated

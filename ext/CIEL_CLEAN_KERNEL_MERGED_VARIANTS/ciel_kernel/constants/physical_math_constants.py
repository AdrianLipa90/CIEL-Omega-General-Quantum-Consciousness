# -*- coding: utf-8 -*-
"""Stałe fizyczne i matematyczne CIEL/Ω (wersja kanoniczna po unifikacji nazw)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PhysicalConstants:
    G: float = 6.6743e-11
    Lp: float = 1.616255e-35
    c: float = 299792458.0
    eps0: float = 8.8541878128e-12
    hbar: float = 1.054571817e-34
    k_B: float = 1.380649e-23
    mp: float = 2.176434e-08
    schumann_base_freq: float = 7.83
    tp: float = 5.391247e-44


@dataclass(frozen=True)
class MathematicalConstants:
    EULER_MASCHERONI: float = 0.5772156649
    HOLOGRAPHIC_RATIO: float = 0.123456789
    LAMBDA_ZETA: float = 0.146

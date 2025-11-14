# ciel_extensions.py
# -*- coding: utf-8 -*-
"""
CIEL/0 – Minimal Extensions Pack (definitions + missing classes)
Nie modyfikuje kernela bazowego; daje gotowe klasy i hooki do wpięcia.
Zaprojektowane z myślą o wektoryzacji (NumPy/Numba/CuPy) i bezpieczeństwie.

Użycie (przykład):
    from ciel_extensions import (
        EthicsGuard, RealityLogger, RealityLayer, KernelSpec,
        SoulInvariantOperator, GPUEngine, GlyphDataset, GlyphInterpreter, CielConfig
    )
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Protocol
import json, os, time
import numpy as np

# =========================
# 1) ENUM / SPEC / CONFIG
# =========================

class RealityLayer:
    """Kategoryzacja pól – kompatybilna z Twoimi nazwami w kernelu."""
    QUANTUM_WAVEFUNCTION = "consciousness_field"   # Ψ(x,t)
    SYMBOLIC_FIELD       = "symbolic_field"        # S(x,t)
    TEMPORAL_FIELD       = "temporal_field"        # τ(x,t)
    RESONANCE_FIELD      = "resonance_field"       # R(S,Ψ)
    MASS_FIELD           = "mass_field"            # m(x,t)
    ENERGY_FIELD         = "energy_field"          # E(x,t)

class KernelSpec(Protocol):
    """Minimalny interfejs, by uruchamiać A/B porównania rdzeni."""
    grid_size: int
    time_steps: int
    constants: Any

    def evolve_reality(self, steps: Optional[int] = None) -> Dict[str, List[float]]: ...
    def update_reality_fields(self) -> None: ...
    def normalize_field(self, field: np.ndarray) -> None: ...

@dataclass
class CielConfig:
    """Parametry uruchomieniowe przenoszone poza kod."""
    enable_gpu: bool = True
    enable_numba: bool = True
    log_path: str = "logs/reality.jsonl"
    ethics_min_coherence: float = 0.4
    ethics_block_on_violation: bool = True
    dataset_path: Optional[str] = None  # np. CVOS_GliphSigils_MariaKamecka.json

# =========================
# 2) ETHICS / LOGGING
# =========================

class EthicsGuard:
    """Lekki strażnik: szybka kontrola metryk względem polityki życia."""
    def __init__(self, bound: float = 0.90, min_coh: float = 0.4, block: bool = True):
        self.ethical_bound = float(bound)
        self.min_coherence = float(min_coh)
        self.block = bool(block)

    def check_step(self, coherence: float, ethical_ok: bool, info_fidelity: float) -> None:
        # proste, zrozumiałe reguły – bez „magii”
        if coherence < self.min_coherence or not ethical_ok:
            msg = (f"[EthicsGuard] breach: coherence={coherence:.3f} "
                   f"ethical_ok={ethical_ok} fidelity={info_fidelity:.3f}")
            if self.block:
                raise RuntimeError(msg)
            else:
                print("⚠", msg)

class RealityLogger:
    """Logger w formacie JSONL (przyjazny narzędziom)."""
    def __init__(self, path: str = "logs/reality.jsonl"):
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    def record(self, step: int, metrics: Dict[str, Any]) -> None:
        rec = dict(step=step, t=time.time(), **metrics)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

# ====================================
# 3) SOUL INVARIANT (Σ) – WERSJA LITE
# ====================================

@dataclass
class SoulInvariantOperator:
    """Spektralna miara Σ: prosta, wektoryzowana, stabilna numerycznie."""
    eps: float = 1e-12

    def compute_sigma_invariant(self, field: np.ndarray) -> float:
        # FFT2 → gęstość mocy → log-wagi
        F = np.fft.fft2(field)
        power = np.abs(F)**2
        # |k|^2 w dziedzinie indeksów – bez drogich meshgridów dla dużych rozmiarów
        h, w = field.shape
        ky = np.fft.fftfreq(h)
        kx = np.fft.fftfreq(w)
        # broadcasting bez tworzenia pełnych siatek (mniejsze zużycie RAM)
        k2 = (ky[:, None]**2) + (kx[None, :]**2)
        sigma = float(np.mean(power * np.log1p(k2 + self.eps)))
        return sigma

    def rescale_to_ethics_bound(self, field: np.ndarray, bound: float = 0.90) -> np.ndarray:
        # delikatna normalizacja amplitudy do granicy etycznej
        amp = np.sqrt(np.mean(np.abs(field)**2)) + self.eps
        target = np.sqrt(bound)
        return field * (target / amp)

# =====================================
# 4) GPU / NUMBA BACKENDS (STUB-READY)
# =====================================

class GPUEngine:
    """Automatyczny wybór backendu dla ciężkich operacji (laplace/grad)."""
    def __init__(self, enable_gpu: bool = True, enable_numba: bool = True):
        self._cupy = None
        self.enable_numba = enable_numba
        if enable_gpu:
            try:
                import cupy as cp  # type: ignore
                self._cupy = cp
            except Exception:
                self._cupy = None

        # opcjonalny numba (fallback przy dużych siatkach CPU)
        self._numba_njit = None
        if enable_numba:
            try:
                from numba import njit
                self._numba_njit = njit
            except Exception:
                self._numba_njit = None

        # przygotuj wersję JIT laplasjanu dla CPU, jeśli możliwe
        self._laplacian_cpu = self._build_laplacian_cpu()

    def xp(self):
        """Zwraca moduł: cupy lub numpy."""
        return self._cupy if self._cupy is not None else np

    def to_xp(self, arr: np.ndarray):
        """Przeniesienie tablicy do backendu (no-op dla NumPy)."""
        if self._cupy is None:  # CPU
            return arr
        return self._cupy.asarray(arr)

    def to_np(self, arr):
        """Przeniesienie tablicy na CPU (NumPy)."""
        if self._cupy is None:
            return arr
        return self._cupy.asnumpy(arr)

    def gradient2(self, field):
        """Szybki grad 2D z backendem; unika pętli w Pythonie."""
        xp = self.xp()
        # prosta różnica centralna (wektoryzowana)
        gx = xp.zeros_like(field)
        gy = xp.zeros_like(field)
        gx[:, 1:-1] = 0.5 * (field[:, 2:] - field[:, :-2])
        gy[1:-1, :] = 0.5 * (field[2:, :] - field[:-2, :])
        return gy, gx  # (d/dy, d/dx)

    def laplacian(self, field):
        """Wersja GPU/CPU; dla CPU używa numba-JIT jeśli dostępne."""
        if self._cupy is not None:
            xp = self._cupy
            out = xp.zeros_like(field)
            out[1:-1,1:-1] = (
                field[2:,1:-1] + field[:-2,1:-1] + field[1:-1,2:] + field[1:-1,:-2]
                - 4.0*field[1:-1,1:-1]
            )
            return out
        # CPU
        return self._laplacian_cpu(field)

    def _build_laplacian_cpu(self):
        def lap_cpu(a: np.ndarray) -> np.ndarray:
            out = np.zeros_like(a)
            out[1:-1,1:-1] = (
                a[2:,1:-1] + a[:-2,1:-1] + a[1:-1,2:] + a[1:-1,:-2]
                - 4.0*a[1:-1,1:-1]
            )
            return out

        if self._numba_njit is not None:
            return self._numba_njit(cache=True, fastmath=True)(lap_cpu)  # type: ignore
        return lap_cpu

# ============================================
# 5) SYMBOLIC LAYER – DATASET + INTERPRETER
# ============================================

@dataclass
class GlyphDataset:
    """Prosty loader datasetów sygli (JSON → struktura wektorowa)."""
    path: str
    items: List[Dict[str, Any]] = field(default_factory=list)

    def load(self) -> "GlyphDataset":
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Akceptuj zarówno listę, jak i dict z kluczem "items"
        self.items = data if isinstance(data, list) else data.get("items", [])
        return self

    def to_vectors(self, key: str = "features") -> np.ndarray:
        # spodziewamy się, że każdy element ma np. "features": [..]
        feats = [it.get(key, []) for it in self.items]
        # bezpieczne wypełnianie długości
        maxlen = max((len(v) for v in feats), default=0)
        arr = np.zeros((len(feats), maxlen), dtype=float)
        for i, v in enumerate(feats):
            arr[i, :len(v)] = np.asarray(v, dtype=float)
        return arr

class GlyphInterpreter:
    """
    Minimalny interpreter: mapuje sygil → modyfikator pola S(x).
    Prawdziwy „język życia” możesz oprzeć na tym szkielecie.
    """
    def __init__(self, vectors: np.ndarray):
        self.vectors = np.asarray(vectors, dtype=float)  # [N, D]
        # pre-normalizacja do stabilnych wag
        norms = np.linalg.norm(self.vectors, axis=1, keepdims=True) + 1e-12
        self.vectors = self.vectors / norms

    def to_field(self, shape: Tuple[int, int], code: Optional[List[int]] = None) -> np.ndarray:
        """
        Rzuca sygil(e) jako pole 2D – bardzo prosty embed:
        sum( w_i * basis_i(x,y) ), gdzie basis_i to radialne „plamki”.
        """
        h, w = shape
        Y = np.linspace(-1.0, 1.0, h)[:, None]
        X = np.linspace(-1.0, 1.0, w)[None, :]
        field = np.zeros((h, w), dtype=np.complex128)

        if not len(self.vectors):
            return field

        idx = code if code is not None else list(range(min(4, len(self.vectors))))
        for k in idx:
            vec = self.vectors[k]
            # prosty radialny „basis”: gauss, gdzie μ sterujemy przez wskaźnik k
            cx = ( (k+1) / (len(self.vectors)+1) ) * 1.6 - 0.8
            cy = -cx
            r2 = (X - cx)**2 + (Y - cy)**2
            basis = np.exp(-3.0 * r2)  # szerokość stała – szybko, stabilnie
            weight = np.tanh(np.sum(vec))  # skalarna waga
            field += weight * basis

        return field.astype(np.complex128)

# ============================================
# 6) LEKKIE HOOKI INTEGRACYJNE (opcjonalne)
# ============================================

def attach_soul_invariant_hooks(kernel: KernelSpec) -> SoulInvariantOperator:
    """
    Zwraca operator Σ i niczego nie „patrzy w środek” kernela.
    Wołasz ręcznie w swojej pętli, jeśli chcesz.
    """
    return SoulInvariantOperator()

def attach_ethics_and_logging(kernel: KernelSpec, cfg: Optional[CielConfig] = None):
    """
    Tworzy gotowe obiekty do ręcznego użycia w Twojej pętli.
    Nie zmienia kernela – pełna kontrola po Twojej stronie.
    """
    cfg = cfg or CielConfig()
    guard = EthicsGuard(bound=getattr(kernel.constants, "ETHICAL_BOUND", 0.90),
                        min_coh=cfg.ethics_min_coherence,
                        block=cfg.ethics_block_on_violation)
    logger = RealityLogger(cfg.log_path)
    return guard, logger

def make_gpu_engine(cfg: Optional[CielConfig] = None) -> GPUEngine:
    cfg = cfg or CielConfig()
    return GPUEngine(enable_gpu=cfg.enable_gpu, enable_numba=cfg.enable_numba)
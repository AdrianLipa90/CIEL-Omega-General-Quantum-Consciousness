from __future__ import annotations

import random
from collections import deque
from typing import Any, Dict, Optional, Tuple

import numpy as np

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..engine_bridge import EngineBridge
from ..settings_store import save_settings
from ..utils import dig


class GraphsPage(QWidget):
    def __init__(self, *, bridge: EngineBridge, settings: Dict[str, Any], parent=None) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._settings = settings

        self._paused = False
        self.raw_buffer = deque(maxlen=512)
        self.lambda_buffer = deque(maxlen=512)

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Graphs & metrics")
        title.setStyleSheet("border: none; background: transparent; font-size: 16px; font-weight: 700;")
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)

        charts_row = QHBoxLayout()
        layout.addLayout(charts_row)

        self.fig_main = Figure(figsize=(6, 4), facecolor="#0d1b2a")
        self.ax_signal = self.fig_main.add_subplot(311)
        self.ax_fft = self.fig_main.add_subplot(312)
        self.ax_lambda = self.fig_main.add_subplot(313)
        self.canvas_main = FigureCanvas(self.fig_main)
        self.canvas_main.setStyleSheet(
            "border: 2px solid #ffffff; border-radius: 5px; background-color: #0d1b2a;"
        )
        charts_row.addWidget(self.canvas_main, 3)

        self.fig_tensor = Figure(figsize=(4, 4), facecolor="#0d1b2a")
        self.ax_tensor = self.fig_tensor.add_subplot(111)
        self.canvas_tensor = FigureCanvas(self.fig_tensor)
        self.canvas_tensor.setStyleSheet(
            "border: 2px solid #ffffff; border-radius: 5px; background-color: #0d1b2a;"
        )
        charts_row.addWidget(self.canvas_tensor, 2)

        self.fig_field = Figure(figsize=(6, 3), facecolor="#0d1b2a")
        self.ax_field = self.fig_field.add_subplot(111)
        self.canvas_field = FigureCanvas(self.fig_field)
        self.canvas_field.setStyleSheet(
            "border: 2px solid #ffffff; border-radius: 5px; background-color: #0d1b2a;"
        )
        layout.addWidget(self.canvas_field, 1)

        controls_group = QGroupBox("Graph controls")
        controls_form = QFormLayout()
        controls_group.setLayout(controls_form)
        layout.addWidget(controls_group)

        self.metrics_label = QLabel("-")
        controls_form.addRow("Metrics", self.metrics_label)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(50, 5000)
        self.interval_spin.setSingleStep(50)
        self.interval_spin.setValue(int(((settings.get("realtime") or {}).get("timer_interval_ms")) or 500))
        self.interval_spin.valueChanged.connect(self.set_interval)
        controls_form.addRow("Update interval (ms)", self.interval_spin)

        btn_row = QHBoxLayout()
        btn_wrap = QWidget()
        btn_wrap.setLayout(btn_row)

        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_pause.clicked.connect(self.toggle_pause)
        btn_row.addWidget(self.btn_pause)

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_buffers)
        btn_row.addWidget(self.btn_clear)

        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.clicked.connect(self.update_tick)
        btn_row.addWidget(self.btn_refresh)

        btn_row.addStretch(1)
        controls_form.addRow("", btn_wrap)

        self.timer = QTimer()
        self.timer.setInterval(self.interval_spin.value())
        self.timer.timeout.connect(self.update_tick)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        try:
            self.timer.start()
        except Exception:
            pass
        self.update_tick()

    def hideEvent(self, event) -> None:
        super().hideEvent(event)
        try:
            self.timer.stop()
        except Exception:
            pass

    def set_interval(self, value: int) -> None:
        try:
            self.timer.setInterval(int(value))
        except Exception:
            pass

        rt_cfg = self._settings.get("realtime") or {}
        rt_cfg["timer_interval_ms"] = int(value)
        self._settings["realtime"] = rt_cfg
        save_settings(self._settings)

    def toggle_pause(self) -> None:
        self._paused = not self._paused
        self.btn_pause.setText("▶ Resume" if self._paused else "⏸ Pause")

    def clear_buffers(self) -> None:
        self.raw_buffer.clear()
        self.lambda_buffer.clear()

    def _simulate_signal(self, n: int) -> np.ndarray:
        base = np.linspace(0, 1, n)
        wave = np.sin(2 * np.pi * (6.0 * base + random.random() * 0.2))
        noise = np.random.normal(0.0, 0.25, size=n)
        return (wave * 1.5 + noise).astype(float)

    def _compute_fft(self, signal: np.ndarray, fs: float = 100.0) -> Tuple[np.ndarray, np.ndarray]:
        if signal.size < 4:
            return np.array([]), np.array([])

        x = signal - float(np.mean(signal))
        n = x.size
        freqs = np.fft.rfftfreq(n, d=1.0 / fs)
        mags = np.abs(np.fft.rfft(x))
        return freqs, mags

    def update_tick(self) -> None:
        if self._paused:
            return

        result = self._bridge.step_status()
        if result is None:
            self.metrics_label.setText("Engine unavailable")
            return

        raw = dig(result, "simulation", "raw", default=None)
        if raw is None:
            eeg = self._simulate_signal(64)
        else:
            try:
                eeg = np.array(list(raw), dtype=float)
            except Exception:
                eeg = self._simulate_signal(64)

        for v in eeg[-64:]:
            self.raw_buffer.append(float(v))

        lambda0 = dig(result, "simulation", "lambda0", default=None)
        try:
            lambda_val = float(lambda0) if lambda0 is not None else None
        except Exception:
            lambda_val = None
        self.lambda_buffer.append(lambda_val if lambda_val is not None else float("nan"))

        buffer_np = np.array(list(self.raw_buffer), dtype=float) if self.raw_buffer else np.array([], dtype=float)

        if buffer_np.size:
            rms = float(np.sqrt(np.mean(np.square(buffer_np))))
            min_v = float(np.min(buffer_np))
            max_v = float(np.max(buffer_np))
        else:
            rms = 0.0
            min_v = 0.0
            max_v = 0.0

        freqs, mags = self._compute_fft(buffer_np[-256:] if buffer_np.size > 256 else buffer_np)

        parts = [f"RMS {rms:.2f}", f"min {min_v:.2f}", f"max {max_v:.2f}"]
        if lambda_val is not None:
            parts.append(f"λ₀ {lambda_val:.3f}")
        self.metrics_label.setText(" · ".join(parts))

        self.ax_signal.clear()
        if buffer_np.size:
            self.ax_signal.plot(buffer_np, linewidth=1.0, color="#22d3ee")
        self.ax_signal.set_facecolor("#0d1b2a")
        self.ax_signal.set_title("Signal (raw mean field)", color="white", fontweight="bold")
        self.ax_signal.tick_params(colors="white")
        self.ax_signal.grid(color="#334155", linestyle="--", linewidth=0.5)

        self.ax_fft.clear()
        if freqs.size and mags.size:
            self.ax_fft.plot(freqs, mags, linewidth=1.0, color="#a78bfa")
        self.ax_fft.set_facecolor("#0d1b2a")
        self.ax_fft.set_title("FFT", color="white", fontweight="bold")
        self.ax_fft.tick_params(colors="white")
        self.ax_fft.grid(color="#334155", linestyle="--", linewidth=0.5)

        self.ax_lambda.clear()
        lambda_np = np.array(list(self.lambda_buffer), dtype=float) if self.lambda_buffer else np.array([], dtype=float)
        if lambda_np.size:
            self.ax_lambda.plot(lambda_np, linewidth=1.0, color="#f97316")
        self.ax_lambda.set_facecolor("#0d1b2a")
        self.ax_lambda.set_title("Lambda₀", color="white", fontweight="bold")
        self.ax_lambda.tick_params(colors="white")
        self.ax_lambda.grid(color="#334155", linestyle="--", linewidth=0.5)

        self.fig_main.patch.set_facecolor("#0d1b2a")
        self.canvas_main.draw()

        tensor_raw = dig(result, "simulation", "resonance_tensor", default=None)
        if tensor_raw is None:
            tensor = np.random.rand(5, 5)
        else:
            arr = np.array(tensor_raw)
            try:
                tensor = arr.reshape((5, 5))
            except Exception:
                flat = arr.flatten()
                padded = np.zeros(25, dtype=float)
                padded[: min(25, flat.size)] = flat[:25]
                tensor = padded.reshape((5, 5))

        self.fig_tensor.clear()
        self.ax_tensor = self.fig_tensor.add_subplot(111)
        im = self.ax_tensor.imshow(tensor, cmap="plasma")
        self.ax_tensor.set_title("Resonance tensor", color="white", fontweight="bold")
        self.ax_tensor.tick_params(colors="white")
        self.fig_tensor.colorbar(im, ax=self.ax_tensor)
        self.fig_tensor.patch.set_facecolor("#0d1b2a")
        self.canvas_tensor.draw()

        field_raw = dig(result, "simulation", "field", default=None)
        if field_raw is None:
            field = np.random.rand(12, 12)
        else:
            try:
                field = np.array(field_raw, dtype=float)
            except Exception:
                field = np.random.rand(12, 12)

        self.fig_field.clear()
        self.ax_field = self.fig_field.add_subplot(111)
        im2 = self.ax_field.imshow(field, aspect="auto", cmap="viridis")
        self.ax_field.set_title("Kernel field", color="white", fontweight="bold")
        self.ax_field.tick_params(colors="white")
        self.fig_field.colorbar(im2, ax=self.ax_field)
        self.fig_field.patch.set_facecolor("#0d1b2a")
        self.canvas_field.draw()

    def shutdown(self) -> None:
        try:
            self.timer.stop()
        except Exception:
            pass


__all__ = ["GraphsPage"]

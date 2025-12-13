from __future__ import annotations

import random
import threading
import time
from collections import deque
from typing import Any, Dict, Optional, Tuple

import numpy as np

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QFormLayout,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..engine_bridge import EngineBridge
from ..settings_store import save_settings
from ..utils import dig

try:
    import cv2
except Exception:
    cv2 = None

try:
    import sounddevice as sd
except Exception:
    sd = None

try:
    import soundfile as sf
except Exception:
    sf = None


class RealtimePage(QWidget):
    def __init__(self, *, bridge: EngineBridge, settings: Dict[str, Any], parent=None) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._settings = settings

        self._paused = False
        self._cap = None
        self._recording = False
        self._audio_thread: Optional[threading.Thread] = None

        self.eeg_buffer = deque(maxlen=256)
        self.tensor_buffer = deque(maxlen=10)

        layout = QVBoxLayout()
        self.setLayout(layout)

        charts_row = QHBoxLayout()
        layout.addLayout(charts_row)

        self.fig_eeg = Figure(figsize=(5, 3), facecolor="#0d1b2a")
        self.ax_eeg = self.fig_eeg.add_subplot(211)
        self.ax_fft = self.fig_eeg.add_subplot(212)
        self.canvas_eeg = FigureCanvas(self.fig_eeg)
        self.canvas_eeg.setStyleSheet("border: 2px solid #ffffff; border-radius: 5px; background-color: #0d1b2a;")
        charts_row.addWidget(self.canvas_eeg, 2)

        self.fig_tensor = Figure(figsize=(4, 3), facecolor="#0d1b2a")
        self.ax_tensor = self.fig_tensor.add_subplot(111)
        self.canvas_tensor = FigureCanvas(self.fig_tensor)
        self.canvas_tensor.setStyleSheet("border: 2px solid #ffffff; border-radius: 5px; background-color: #0d1b2a;")
        charts_row.addWidget(self.canvas_tensor, 2)

        self.video_label = QLabel("\n\n📷 Camera")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(220, 160)
        charts_row.addWidget(self.video_label, 1)

        controls_group = QGroupBox("Realtime controls")
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

        self.btn_camera = QPushButton("Camera")
        self.btn_camera.clicked.connect(self.toggle_camera)
        btn_row.addWidget(self.btn_camera)

        self.btn_mic = QPushButton("Mic")
        self.btn_mic.clicked.connect(self.toggle_mic)
        btn_row.addWidget(self.btn_mic)

        btn_row.addStretch(1)
        controls_form.addRow("", btn_wrap)

        self.timer = QTimer()
        self.timer.setInterval(self.interval_spin.value())
        self.timer.timeout.connect(self.update_tick)
        self.timer.start()

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
        self.eeg_buffer.clear()
        self.tensor_buffer.clear()

    def toggle_camera(self) -> None:
        if cv2 is None:
            self.video_label.setText("Camera requires opencv-python")
            return

        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None
            self.video_label.setText("\n\n📷 Camera")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.video_label.setText("Camera error")
            try:
                cap.release()
            except Exception:
                pass
            return

        self._cap = cap

    def toggle_mic(self) -> None:
        if sd is None or sf is None:
            self.metrics_label.setText("Mic requires sounddevice + soundfile")
            return

        if self._recording:
            self._recording = False
            return

        self._recording = True
        self._audio_thread = threading.Thread(target=self._record_audio, daemon=True)
        self._audio_thread.start()

    def _record_audio(self) -> None:
        if sd is None or sf is None:
            return

        fs = 44100
        duration = 5

        try:
            audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)
            for _ in range(duration * 10):
                if not self._recording:
                    sd.stop()
                    return
                sd.sleep(100)
            sd.wait()
            if self._recording:
                sf.write("recording.wav", audio, fs)
        except Exception:
            pass
        finally:
            self._recording = False

    def _simulate_eeg(self, n: int) -> np.ndarray:
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

        eeg_raw = dig(result, "simulation", "raw", default=None)
        if eeg_raw is None:
            eeg = self._simulate_eeg(64)
        else:
            try:
                eeg = np.array(list(eeg_raw), dtype=float)
            except Exception:
                eeg = self._simulate_eeg(64)

        for v in eeg[-64:]:
            self.eeg_buffer.append(float(v))

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

        self.tensor_buffer.append(tensor)

        lambda0 = dig(result, "simulation", "lambda0", default=None)
        try:
            lambda_val = float(lambda0) if lambda0 is not None else None
        except Exception:
            lambda_val = None

        buffer_np = np.array(list(self.eeg_buffer), dtype=float)
        if buffer_np.size:
            rms = float(np.sqrt(np.mean(np.square(buffer_np))))
            min_v = float(np.min(buffer_np))
            max_v = float(np.max(buffer_np))
        else:
            rms = 0.0
            min_v = 0.0
            max_v = 0.0

        freqs, mags = self._compute_fft(buffer_np[-128:] if buffer_np.size > 128 else buffer_np)

        parts = [f"RMS {rms:.2f}", f"min {min_v:.2f}", f"max {max_v:.2f}"]
        if lambda_val is not None:
            parts.append(f"λ₀ {lambda_val:.3f}")
        self.metrics_label.setText(" · ".join(parts))

        self.ax_eeg.clear()
        self.ax_eeg.plot(buffer_np, linewidth=1.0, color="#22d3ee")
        self.ax_eeg.set_facecolor("#0d1b2a")
        self.ax_eeg.set_title("EEG", color="white", fontweight="bold")
        self.ax_eeg.tick_params(colors="white")
        self.ax_eeg.grid(color="#334155", linestyle="--", linewidth=0.5)

        self.ax_fft.clear()
        if freqs.size and mags.size:
            self.ax_fft.plot(freqs, mags, linewidth=1.0, color="#a78bfa")
        self.ax_fft.set_facecolor("#0d1b2a")
        self.ax_fft.set_title("FFT", color="white", fontweight="bold")
        self.ax_fft.tick_params(colors="white")
        self.ax_fft.grid(color="#334155", linestyle="--", linewidth=0.5)

        self.fig_eeg.patch.set_facecolor("#0d1b2a")
        self.canvas_eeg.draw()

        self.fig_tensor.clear()
        self.ax_tensor = self.fig_tensor.add_subplot(111)
        im = self.ax_tensor.imshow(tensor, cmap="plasma")
        self.ax_tensor.set_title("Tensor", color="white", fontweight="bold")
        self.ax_tensor.tick_params(colors="white")
        self.fig_tensor.colorbar(im, ax=self.ax_tensor)
        self.fig_tensor.patch.set_facecolor("#0d1b2a")
        self.canvas_tensor.draw()

        if cv2 is not None and self._cap is not None and self._cap.isOpened():
            ret, frame = self._cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytes_per_line = ch * w
                img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(img).scaled(220, 160, Qt.KeepAspectRatio))
            else:
                try:
                    self._cap.release()
                except Exception:
                    pass
                self._cap = None
                self.video_label.setText("Camera disabled")

    def shutdown(self) -> None:
        try:
            self.timer.stop()
        except Exception:
            pass

        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None


__all__ = ["RealtimePage"]

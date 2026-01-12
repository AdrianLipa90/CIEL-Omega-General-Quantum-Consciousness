"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""
import sys

if __name__ == "__main__":
    from ciel.ui import run_control_center

    raise SystemExit(run_control_center(sys.argv))

import time
import random
import json
import threading
import importlib.util
try:
    import sounddevice as sd
except Exception:
    sd = None
try:
    import soundfile as sf
except Exception:
    sf = None
from collections import deque
import numpy as np
from typing import Any
import argparse
import os

try:
    import cv2
except Exception:
    cv2 = None

# Set Qt platform before importing PyQt5
if os.environ.get('DISPLAY') is None or '--headless' in sys.argv:
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'

_pyqt5_spec = importlib.util.find_spec("PyQt5")
if _pyqt5_spec and _pyqt5_spec.origin:
    _pyqt5_root = os.path.dirname(_pyqt5_spec.origin)
    _qt_plugins = os.path.join(_pyqt5_root, "Qt5", "plugins")
    _qt_platforms = os.path.join(_qt_plugins, "platforms")
    if os.path.isdir(_qt_plugins):
        os.environ.setdefault("QT_PLUGIN_PATH", _qt_plugins)
    if os.path.isdir(_qt_platforms):
        os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", _qt_platforms)

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QLineEdit,
    QLabel,
    QFileDialog,
    QComboBox,
    QTabWidget,
    QFormLayout,
    QSpinBox,
    QGroupBox,
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
try:
    from reportlab.pdfgen import canvas as pdfcanvas
    from reportlab.lib.pagesizes import A4
except Exception:
    pdfcanvas = None
    A4 = None

# --- IMPORT SILNIKA CIEL/Ω ---
try:
    from ciel import CielEngine, build_default_bundle
    engine_enabled = True
except Exception:
    engine_enabled = False
    print("⚠ CIEL engine not found. Simulation mode enabled.")

def dig(obj: Any, *path, default=None):
    """
    Safely traverse a nested attribute/key path.
    Supports dicts and objects via getattr. Returns default when missing.
    """
    cur = obj
    for key in path:
        if cur is None:
            return default
        if isinstance(cur, dict):
            cur = cur.get(key, None)
        else:
            cur = getattr(cur, key, None)
    return default if cur is None else cur

def safe_chat_add(chat_widget: QListWidget, item: Any):
    """
    Append any item to a QListWidget.
    dict/list are rendered as pretty JSON; None becomes an empty string.
    """
    if isinstance(item, (dict, list)):
        text = json.dumps(item, ensure_ascii=False, indent=2)
    elif item is None:
        text = ""
    else:
        text = str(item)
    chat_widget.addItem(text)
    chat_widget.scrollToBottom()

class CIELUltra(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CIEL/Ω Control Center")
        self.resize(1400, 800)
        
        # Enhanced styling for cleaner UI
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e2e8f0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
            }
            QListWidget {
                border: 1px solid #475569;
                border-radius: 8px;
                background-color: #1e293b;
                padding: 8px;
                selection-background-color: #334155;
            }
            QPushButton {
                border: 1px solid #475569;
                border-radius: 6px;
                background-color: #1e40af;
                color: #ffffff;
                padding: 10px 16px;
                font-weight: 600;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2563eb;
                border-color: #60a5fa;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QLabel {
                border: 1px solid #475569;
                border-radius: 6px;
                background-color: #1e293b;
                padding: 8px;
                font-weight: 500;
            }
            QLineEdit {
                border: 1px solid #475569;
                border-radius: 6px;
                background-color: #1e293b;
                color: #e2e8f0;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
            QComboBox {
                border: 1px solid #475569;
                border-radius: 6px;
                background-color: #1e293b;
                color: #e2e8f0;
                padding: 8px;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #475569;
                background-color: #1e293b;
                selection-background-color: #334155;
                padding: 4px;
            }
        """)

        self.engine = CielEngine() if engine_enabled else None
        self.llm_bundle = build_default_bundle() if engine_enabled else None
        self._engine_lock = threading.Lock()
        self._busy = False
        self.dialogue = []
        self.eeg_buffer = deque(maxlen=100)
        self.tensor_buffer = deque(maxlen=10)
        self.paused = False
        self.cap = None
        self.recording = False
        self.audio_thread = None

        if self.engine:
            try:
                self.engine.boot()
            except Exception:
                pass

        main = QVBoxLayout()
        header = QHBoxLayout()
        self.logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "Logo1.png")
        if os.path.isfile(logo_path):
            pixmap = QPixmap(logo_path)
            self.logo_label.setPixmap(pixmap.scaledToHeight(48, Qt.SmoothTransformation))
        else:
            self.logo_label.setText("CIEL/Ω")
        self.logo_label.setStyleSheet("border: none; background: transparent;")

        header_title = QLabel("CIEL/Ω Control Center")
        header_title.setStyleSheet(
            "border: none; background: transparent; font-size: 18px; font-weight: 700;"
        )
        header.addWidget(self.logo_label)
        header.addWidget(header_title)
        header.addStretch(1)
        main.addLayout(header)

        top = QHBoxLayout()
        bottom = QHBoxLayout()

        # EEG
        self.fig_eeg = Figure(figsize=(4,3), facecolor='#0d1b2a')
        self.ax_eeg = self.fig_eeg.add_subplot(111)
        self.canvas_eeg = FigureCanvas(self.fig_eeg)
        self.canvas_eeg.setStyleSheet("border: 2px solid #ffffff; border-radius: 5px; background-color: #0d1b2a;")
        top.addWidget(self.canvas_eeg)

        # Tensor
        self.fig_tensor = Figure(figsize=(4,3), facecolor='#0d1b2a')
        self.ax_tensor = self.fig_tensor.add_subplot(111)
        self.canvas_tensor = FigureCanvas(self.fig_tensor)
        self.canvas_tensor.setStyleSheet("border: 2px solid #ffffff; border-radius: 5px; background-color: #0d1b2a;")
        top.addWidget(self.canvas_tensor)

        # Camera
        self.video_label = QLabel("\n\n📷 Camera preview")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(200, 150)
        top.addWidget(self.video_label)

        main.addLayout(top)

        # Chat and side panel
        self.chat_log = QListWidget()
        bottom.addWidget(self.chat_log, 3)

        side_tabs = QTabWidget()

        controls_page = QWidget()
        controls_layout = QVBoxLayout()
        controls_page.setLayout(controls_layout)

        self.label_status = QLabel("Lambda₀: no data")
        controls_layout.addWidget(self.label_status)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["standard", "creative", "analytic", "experimental"])
        controls_layout.addWidget(QLabel("🎛 AI mode:"))
        controls_layout.addWidget(self.mode_selector)

        self.llm_profile_selector = QComboBox()
        profiles = [
            ("lite", "Fast, lightweight responses"),
            ("standard", "Balanced performance"),
            ("science", "Detailed, analytical responses"),
            ("ultra", "Maximum capability"),
        ]
        for profile, desc in profiles:
            self.llm_profile_selector.addItem(f"{profile} - {desc}", profile)
        self.llm_profile_selector.setCurrentText("standard - Balanced performance")
        controls_layout.addWidget(QLabel("🧠 LLM profile:"))
        controls_layout.addWidget(self.llm_profile_selector)

        self.memory_selector = QComboBox()
        self.memory_selector.addItems(["echo", "dream", "adam", "braid"])
        controls_layout.addWidget(QLabel("🧠 Memory:"))
        controls_layout.addWidget(self.memory_selector)

        self.field_viz_selector = QComboBox()
        for label, key in [
            ("Scalar field view", "scalar"),
            ("Vector field flow", "vector"),
            ("Tensor resonance", "tensor"),
            ("Spectral coherence", "spectral"),
        ]:
            self.field_viz_selector.addItem(label, key)
        controls_layout.addWidget(QLabel("🌊 Field viz:"))
        controls_layout.addWidget(self.field_viz_selector)

        btn_load_file = QPushButton("📁 Add file")
        btn_load_file.clicked.connect(self.load_file)
        controls_layout.addWidget(btn_load_file)

        btn_export_json = QPushButton("📦 Export JSON")
        btn_export_json.clicked.connect(self.export_json)
        controls_layout.addWidget(btn_export_json)

        btn_export_pdf = QPushButton("🧾 Export PDF")
        btn_export_pdf.clicked.connect(self.export_pdf)
        controls_layout.addWidget(btn_export_pdf)

        btn_camera = QPushButton("🎥 Camera ON/OFF")
        btn_camera.clicked.connect(self.toggle_camera)
        controls_layout.addWidget(btn_camera)

        btn_mic = QPushButton("🎙️ Microphone ON/OFF")
        btn_mic.clicked.connect(self.toggle_mic)
        controls_layout.addWidget(btn_mic)

        self.btn_pause = QPushButton("⏸ Pause EEG")
        self.btn_pause.clicked.connect(self.toggle_timer)
        controls_layout.addWidget(self.btn_pause)

        controls_layout.addStretch(1)

        settings_page = QWidget()
        settings_layout = QVBoxLayout()
        settings_page.setLayout(settings_layout)

        llm_group = QGroupBox("LLM settings")
        llm_form = QFormLayout()
        llm_group.setLayout(llm_form)

        self.backend_selector = QComboBox()
        self.backend_selector.addItem("HF (Transformers)", "hf")
        self.backend_selector.addItem("GGUF (llama.cpp)", "gguf")
        backend_default = (os.getenv("CIEL_LLM_BACKEND") or "hf").strip().lower()
        self.backend_selector.setCurrentIndex(1 if backend_default == "gguf" else 0)
        llm_form.addRow("Backend", self.backend_selector)

        gguf_row = QWidget()
        gguf_row_layout = QHBoxLayout()
        gguf_row_layout.setContentsMargins(0, 0, 0, 0)
        gguf_row.setLayout(gguf_row_layout)

        self.gguf_model_path = QLineEdit()
        self.gguf_model_path.setText(os.getenv("CIEL_GGUF_MODEL_PATH") or "")
        btn_browse_gguf = QPushButton("Browse")
        btn_browse_gguf.clicked.connect(self.browse_gguf_model)
        gguf_row_layout.addWidget(self.gguf_model_path)
        gguf_row_layout.addWidget(btn_browse_gguf)
        llm_form.addRow("GGUF model path", gguf_row)

        self.gguf_n_ctx = QSpinBox()
        self.gguf_n_ctx.setRange(256, 262144)
        self.gguf_n_ctx.setValue(2048)
        llm_form.addRow("n_ctx", self.gguf_n_ctx)

        self.gguf_n_threads = QSpinBox()
        self.gguf_n_threads.setRange(1, 256)
        self.gguf_n_threads.setValue(4)
        llm_form.addRow("n_threads", self.gguf_n_threads)

        self.gguf_n_gpu_layers = QSpinBox()
        self.gguf_n_gpu_layers.setRange(0, 256)
        self.gguf_n_gpu_layers.setValue(0)
        llm_form.addRow("n_gpu_layers", self.gguf_n_gpu_layers)

        self.gguf_system_prompt = QLineEdit()
        llm_form.addRow("System prompt", self.gguf_system_prompt)

        btn_apply_llm = QPushButton("Apply")
        btn_apply_llm.clicked.connect(self.apply_llm_settings)
        llm_form.addRow("", btn_apply_llm)

        settings_layout.addWidget(llm_group)

        rt_group = QGroupBox("Realtime")
        rt_form = QFormLayout()
        rt_group.setLayout(rt_form)

        self.timer_interval = QSpinBox()
        self.timer_interval.setRange(50, 5000)
        self.timer_interval.setSingleStep(50)
        self.timer_interval.setValue(500)
        self.timer_interval.valueChanged.connect(self.on_timer_interval_changed)
        rt_form.addRow("Update interval (ms)", self.timer_interval)

        btn_clear_buffers = QPushButton("Clear buffers")
        btn_clear_buffers.clicked.connect(self.clear_buffers)
        rt_form.addRow("", btn_clear_buffers)

        settings_layout.addWidget(rt_group)
        settings_layout.addStretch(1)

        side_tabs.addTab(controls_page, "Controls")
        side_tabs.addTab(settings_page, "Settings")

        bottom.addWidget(side_tabs, 1)
        main.addLayout(bottom)

        # Input
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type a message and press Enter…")
        self.btn_send = QPushButton("Send")
        self.btn_send.clicked.connect(self.send_message)
        self.input_line.returnPressed.connect(self.send_message)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.btn_send)
        main.addLayout(input_layout)

        self.setLayout(main)

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_visuals)
        self.timer.start()

    def _get_status_result(self):
        try:
            result = self.engine.step("status") if self.engine else None
            return result
        except Exception as e:
            safe_chat_add(self.chat_log, f"⚠ Engine error: {e}")
            return None

    def update_visuals(self):
        if self.paused:
            return

        if self.engine:
            if not self._engine_lock.acquire(blocking=False):
                return
            try:
                result = self._get_status_result()
            finally:
                self._engine_lock.release()
            eeg_data = dig(result, "simulation", "raw", default=None)
            if eeg_data is None:
                eeg_data = [np.sin(i*0.03)*2 + random.uniform(-0.5,0.5) for i in range(100)]
            else:
                eeg_data = list(eeg_data)
                if len(eeg_data)<100:
                    eeg_data = (eeg_data + [0.0]*100)[:100]

            tensor_raw = dig(result, "simulation", "resonance_tensor", default=None)
            if tensor_raw is None:
                tensor = np.random.rand(5,5)
            else:
                arr = np.array(tensor_raw)
                try:
                    tensor = arr.reshape((5,5))
                except Exception:
                    flat = arr.flatten()
                    padded = np.zeros(25, dtype=flat.dtype)
                    padded[:min(25, flat.size)] = flat[:25]
                    tensor = padded.reshape((5,5))

            lambda_val = dig(result, "simulation", "lambda0", default=None)
            if lambda_val is None:
                lambda_val = round(random.uniform(0.3, 0.9),3)
        else:
            eeg_data = [np.sin(i*0.03 + random.random()*0.1)*2 + random.uniform(-0.5,0.5) for i in range(100)]
            tensor = np.random.rand(5,5)
            lambda_val = round(random.uniform(0.3,0.9),3)

        self.eeg_buffer.extend(eeg_data[-100:])
        self.tensor_buffer.append(tensor)

        # EEG
        self.ax_eeg.clear()
        self.ax_eeg.plot(list(self.eeg_buffer), linewidth=1.0, color='cyan')
        self.ax_eeg.set_facecolor("#0d1b2a")
        self.fig_eeg.patch.set_facecolor('#0d1b2a')
        self.ax_eeg.set_title("EEG (δ-γ)", color="white", fontweight='bold')
        self.ax_eeg.set_ylabel("Amplitude", color="white")
        self.ax_eeg.set_xlabel("Time (step)", color="white")
        self.ax_eeg.grid(color='#4a90e2', linestyle='--', linewidth=0.5)
        self.ax_eeg.set_ylim(-3,3)
        self.ax_eeg.tick_params(colors='white')
        self.ax_eeg.spines['bottom'].set_color('white')
        self.ax_eeg.spines['top'].set_color('white')
        self.ax_eeg.spines['right'].set_color('white')
        self.ax_eeg.spines['left'].set_color('white')
        self.canvas_eeg.draw()

        # Tensor
        self.fig_tensor.clear()
        self.ax_tensor = self.fig_tensor.add_subplot(111)
        self.fig_tensor.patch.set_facecolor('#0d1b2a')
        im = self.ax_tensor.imshow(tensor, cmap='plasma')
        self.ax_tensor.set_facecolor("#0d1b2a")
        self.ax_tensor.set_title("Intention tensor (Ψ/Σ)", color="white", fontweight='bold')
        self.ax_tensor.tick_params(colors='white')
        self.ax_tensor.spines['bottom'].set_color('white')
        self.ax_tensor.spines['top'].set_color('white')
        self.ax_tensor.spines['right'].set_color('white')
        self.ax_tensor.spines['left'].set_color('white')
        cbar = self.fig_tensor.colorbar(im, ax=self.ax_tensor)
        cbar.ax.tick_params(colors='white')
        self.canvas_tensor.draw()

        # Camera
        if cv2 is not None and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytes_per_line = ch * w
                img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(img).scaled(200, 150, Qt.KeepAspectRatio))
            else:
                # Camera stopped responding
                self.cap.release()
                self.cap = None
                self.video_label.setText("📷 Camera disabled")

        self.label_status.setText(f"Lambda₀: {lambda_val}")

    def toggle_timer(self):
        self.paused = not self.paused
        if hasattr(self, "btn_pause"):
            self.btn_pause.setText("▶ Resume EEG" if self.paused else "⏸ Pause EEG")

    def toggle_camera(self):
        if cv2 is None:
            safe_chat_add(self.chat_log, "⚠ OpenCV is not available; camera requires opencv-python.")
            return
        if self.cap:
            self.cap.release()
            self.cap = None
            self.video_label.setText("📷 Camera disabled")
        else:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.cap = None
                safe_chat_add(self.chat_log, "⚠ Unable to open camera")
                self.video_label.setText("📷 Camera error")

    def toggle_mic(self):
        if sd is None or sf is None:
            safe_chat_add(self.chat_log, "⚠ Microphone requires sounddevice and soundfile.")
            return
        if not self.recording:
            self.recording = True
            self.audio_thread = threading.Thread(target=self.record_audio, daemon=True)
            self.audio_thread.start()
            safe_chat_add(self.chat_log, "🎙️ Microphone: recording...")
        else:
            self.recording = False
            safe_chat_add(self.chat_log, "🛑 Microphone: stopped")

    def record_audio(self):
        if sd is None or sf is None:
            return
        try:
            fs = 44100
            duration = 5
            audio = sd.rec(int(duration*fs), samplerate=fs, channels=2)
            # Wait until recording finishes or the user stops it
            for _ in range(duration * 10):  # Check every 100ms
                if not self.recording:
                    sd.stop()
                    return
                sd.sleep(100)
            if not self.recording:
                sd.stop()
                return
            sd.wait()
            if self.recording:  # Re-check after recording completes
                sf.write("recording.wav", audio, fs)
                # Use QTimer.singleShot to call from the main thread
                QTimer.singleShot(0, lambda: safe_chat_add(self.chat_log, "🎧 Saved as recording.wav"))
        except Exception as e:
            # Use QTimer.singleShot to call from the main thread
            error_msg = f"⚠ Recording error: {e}"
            QTimer.singleShot(0, lambda msg=error_msg: safe_chat_add(self.chat_log, msg))
        finally:
            self.recording = False

    def send_message(self):
        user = self.input_line.text().strip()
        if not user or self._busy:
            return

        mode = self.mode_selector.currentText()
        memory = self.memory_selector.currentText()
        safe_chat_add(self.chat_log, f"You ({mode}/{memory}): {user}")

        dialogue_snapshot = list(self.dialogue)
        dialogue_snapshot.append({"role": "user", "content": user})
        self.dialogue = dialogue_snapshot

        self.input_line.clear()

        if not self.engine:
            state = random.choice(["calm", "active", "distracted"])
            ud = random.randint(20, 90)
            response_str = (
                f"Analysis complete. Emotional state: {state}. ŨD index: {ud}%.\n"
                f"CIEL ({mode}): "
                + random.choice(
                    [
                        "Your intentions resonate within the coherence field.",
                        "A spike in β-wave activity was detected.",
                        "The tensor indicates task focus.",
                        "Analytic mode engaged.",
                    ]
                )
            )
            lambda_val = round(random.uniform(0.3, 0.9), 3)
            safe_chat_add(self.chat_log, response_str)
            self.label_status.setText(f"Lambda₀: {lambda_val}")
            self.autosave_chat()
            return

        profile = (
            self.llm_profile_selector.currentData()
            if hasattr(self, "llm_profile_selector")
            else "standard"
        )

        self.set_busy(True)
        threading.Thread(
            target=self.run_engine_interact,
            args=(user, dialogue_snapshot, mode, profile),
            daemon=True,
        ).start()

    def set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.btn_send.setEnabled(not busy)
        self.input_line.setEnabled(not busy)

    def run_engine_interact(
        self,
        user: str,
        dialogue_snapshot: list[dict[str, str]],
        mode: str,
        profile: str,
    ) -> None:
        result = None
        error: str | None = None
        latency_ms: float | None = None

        try:
            if self.llm_bundle is not None:
                self.engine.language_backend = self.llm_bundle.primary_for(profile)
                self.engine.aux_backend = self.llm_bundle.composite_aux()

            t0 = time.perf_counter()
            with self._engine_lock:
                result = self.engine.interact(user, dialogue_snapshot, context=mode)
            latency_ms = (time.perf_counter() - t0) * 1000.0
        except Exception as exc:
            error = str(exc)

        QTimer.singleShot(
            0,
            lambda: self.on_engine_interact_done(result=result, error=error, latency_ms=latency_ms),
        )

    def on_engine_interact_done(
        self,
        *,
        result,
        error: str | None,
        latency_ms: float | None,
    ) -> None:
        try:
            if error is not None:
                safe_chat_add(self.chat_log, f"⚠ Engine error: {error}")
                return

            if latency_ms is not None:
                safe_chat_add(self.chat_log, f"⏱ latency: {latency_ms:.1f} ms")

            reply = dig(result, "reply", default=None)
            if reply is None:
                reply = dig(result, "ciel_state", "cognition", default=None)
            if isinstance(reply, (dict, list)):
                response_str = json.dumps(reply, ensure_ascii=False, indent=2)
            else:
                response_str = str(reply)

            self.dialogue.append({"role": "assistant", "content": response_str})

            lambda_val = dig(result, "ciel_state", "simulation", "lambda0", default=None)
            if lambda_val is None:
                lambda_val = round(random.uniform(0.3, 0.9), 3)

            safe_chat_add(self.chat_log, response_str)
            self.label_status.setText(f"Lambda₀: {lambda_val}")
            self.autosave_chat()
        finally:
            self.set_busy(False)
            self.input_line.setFocus()

    def browse_gguf_model(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select GGUF model", "", "GGUF (*.gguf);;All files (*)")
        if path:
            self.gguf_model_path.setText(path)

    def apply_llm_settings(self) -> None:
        if not engine_enabled:
            safe_chat_add(self.chat_log, "⚠ CIEL engine is not available; cannot apply LLM settings.")
            return

        backend = self.backend_selector.currentData()
        gguf_path = self.gguf_model_path.text().strip()
        if gguf_path:
            os.environ["CIEL_GGUF_MODEL_PATH"] = gguf_path
        elif "CIEL_GGUF_MODEL_PATH" in os.environ:
            del os.environ["CIEL_GGUF_MODEL_PATH"]

        try:
            self.llm_bundle = build_default_bundle(
                backend=str(backend),
                gguf_n_ctx=int(self.gguf_n_ctx.value()),
                gguf_n_threads=int(self.gguf_n_threads.value()),
                gguf_n_gpu_layers=int(self.gguf_n_gpu_layers.value()),
                gguf_system_prompt=str(self.gguf_system_prompt.text()),
            )
            safe_chat_add(self.chat_log, f"✅ Applied LLM settings (backend={backend}).")
        except Exception as exc:
            safe_chat_add(self.chat_log, f"⚠ Failed to apply LLM settings: {exc}")

    def on_timer_interval_changed(self, value: int) -> None:
        try:
            self.timer.setInterval(int(value))
        except Exception:
            pass

    def clear_buffers(self) -> None:
        try:
            self.eeg_buffer.clear()
            self.tensor_buffer.clear()
            safe_chat_add(self.chat_log, "✅ Buffers cleared")
        except Exception as exc:
            safe_chat_add(self.chat_log, f"⚠ Failed to clear buffers: {exc}")

    def autosave_chat(self):
        data = {
            "chat": [self.chat_log.item(i).text() for i in range(self.chat_log.count())],
            "lambda0": self.label_status.text(),
            "eeg_buffer": list(self.eeg_buffer),
            "tensor": self.tensor_buffer[-1].tolist() if self.tensor_buffer else []
        }
        try:
            with open("ciel_autosave.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            safe_chat_add(self.chat_log, f"⚠ Autosave write error: {e}")

    def export_json(self):
        self.autosave_chat()
        safe_chat_add(self.chat_log, "✅ JSON export completed.")

    def export_pdf(self):
        if pdfcanvas is None or A4 is None:
            safe_chat_add(self.chat_log, "⚠ PDF export requires reportlab.")
            return
        try:
            pdf = pdfcanvas.Canvas("ciel_report.pdf", pagesize=A4)
            textobject = pdf.beginText(40, 800)
            textobject.setFont("Helvetica", 10)
            y_position = 800
            for i in range(self.chat_log.count()):
                line = self.chat_log.item(i).text()
                # Long lines can be problematic; limit line length
                if len(line) > 100:
                    # Split long lines
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 100:
                            current_line += word + " "
                        else:
                            if current_line:
                                textobject.textLine(current_line.strip())
                                y_position -= 12
                                if y_position < 50:  # New page if needed
                                    pdf.drawText(textobject)
                                    pdf.showPage()
                                    textobject = pdf.beginText(40, 800)
                                    y_position = 800
                            current_line = word + " "
                    if current_line:
                        textobject.textLine(current_line.strip())
                        y_position -= 12
                else:
                    textobject.textLine(line)
                    y_position -= 12
                    if y_position < 50:  # New page if needed
                        pdf.drawText(textobject)
                        pdf.showPage()
                        textobject = pdf.beginText(40, 800)
                        y_position = 800
            pdf.drawText(textobject)
            pdf.save()
            safe_chat_add(self.chat_log, "📄 PDF saved as ciel_report.pdf")
        except Exception as e:
            safe_chat_add(self.chat_log, f"⚠ PDF export error: {e}")

    def load_file(self):
        path,_ = QFileDialog.getOpenFileName(self, "Select a file")
        if path:
            safe_chat_add(self.chat_log, f"📂 Loaded file: {path}")

    def closeEvent(self, event):
        try:
            if hasattr(self, "timer"):
                self.timer.stop()
        except Exception:
            pass

        try:
            if self.cap:
                self.cap.release()
                self.cap = None
        except Exception:
            pass

        try:
            if self.engine:
                self.engine.shutdown()
        except Exception:
            pass

        super().closeEvent(event)

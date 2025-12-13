import sys
import time
import random
import json
import threading
import sounddevice as sd
import soundfile as sf
from collections import deque
import numpy as np
from typing import Any
import argparse

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QListWidget, QLineEdit, QLabel, QFileDialog, QComboBox)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A4

# --- IMPORT SILNIKA CIEL/Ω ---
try:
    from ciel import CielEngine, build_default_bundle
    engine_enabled = True
except Exception:
    engine_enabled = False
    print("⚠️ Nie znaleziono silnika CIEL. Tryb symulacji aktywny.")

def dig(obj: Any, *path, default=None):
    """
    Bezpiecznie zjedź po ścieżce atrybutów/kluczy.
    - obsługuje dict i obiekty z getattr
    - jeśli brak któregokolwiek elementu, zwraca default
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
    Dodaje cokolwiek do QListWidget bez wywalania błędu
    - dict/list konwertuje do ładnego JSON
    - None -> pusty string
    """
    if isinstance(item, (dict, list)):
        text = json.dumps(item, ensure_ascii=False, indent=2)
    elif item is None:
        text = ""
    else:
        text = str(item)
    chat_widget.addItem(text)

class CIELUltra(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfejs CIEL/Ω Ultra Świadomości — AI")
        self.resize(1200, 700)
        # Ciemno niebieskie tło z ramkami
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a3e;
                color: #ffffff;
                font-family: Consolas;
            }
            QListWidget {
                border: 2px solid #ffffff;
                border-radius: 5px;
                background-color: #0d1b2a;
                padding: 5px;
            }
            QPushButton {
                border: 2px solid #ffffff;
                border-radius: 5px;
                background-color: #1e3a5f;
                color: #ffffff;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a4a6f;
            }
            QPushButton:pressed {
                background-color: #0f2a4f;
            }
            QLabel {
                border: 2px solid #ffffff;
                border-radius: 5px;
                background-color: #0d1b2a;
                padding: 5px;
            }
            QLineEdit {
                border: 2px solid #ffffff;
                border-radius: 5px;
                background-color: #0d1b2a;
                color: #ffffff;
                padding: 5px;
            }
            QComboBox {
                border: 2px solid #ffffff;
                border-radius: 5px;
                background-color: #0d1b2a;
                color: #ffffff;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: 1px solid #ffffff;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #ffffff;
                background-color: #1a1a3e;
                selection-background-color: #1e3a5f;
            }
        """)

        self.engine = CielEngine() if engine_enabled else None
        self.llm_bundle = build_default_bundle() if engine_enabled else None
        self.dialogue = []
        self.eeg_buffer = deque(maxlen=100)
        self.tensor_buffer = deque(maxlen=10)
        self.paused = False
        self.cap = None
        self.recording = False
        self.audio_thread = None

        main = QVBoxLayout()
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

        # Kamera
        self.video_label = QLabel("\n\n📷 Podgląd kamery")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(200, 150)
        top.addWidget(self.video_label)

        main.addLayout(top)

        # Chat i boczny panel
        self.chat_log = QListWidget()
        bottom.addWidget(self.chat_log, 3)

        side = QVBoxLayout()
        self.label_status = QLabel("Lambda₀: brak danych")
        side.addWidget(self.label_status)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["standard", "kreatywny", "analityczny", "eksperymentalny"])
        side.addWidget(QLabel("🎛 Tryb AI:"))
        side.addWidget(self.mode_selector)

        self.llm_profile_selector = QComboBox()
        self.llm_profile_selector.addItems(["lite", "standard", "science"])
        self.llm_profile_selector.setCurrentText("standard")
        side.addWidget(QLabel("🧠 LLM profil:"))
        side.addWidget(self.llm_profile_selector)

        self.memory_selector = QComboBox()
        self.memory_selector.addItems(["echo", "dream", "adam", "braid"])
        side.addWidget(QLabel("🧠 Pamięć:"))
        side.addWidget(self.memory_selector)

        btn_load_file = QPushButton("📁 Dodaj plik")
        btn_load_file.clicked.connect(self.load_file)
        side.addWidget(btn_load_file)

        btn_export_json = QPushButton("📦 Eksportuj JSON")
        btn_export_json.clicked.connect(self.export_json)
        side.addWidget(btn_export_json)

        btn_export_pdf = QPushButton("🧾 Eksportuj PDF")
        btn_export_pdf.clicked.connect(self.export_pdf)
        side.addWidget(btn_export_pdf)

        btn_camera = QPushButton("🎥 Kamera ON/OFF")
        btn_camera.clicked.connect(self.toggle_camera)
        side.addWidget(btn_camera)

        btn_mic = QPushButton("🎙️ Mikrofon ON/OFF")
        btn_mic.clicked.connect(self.toggle_mic)
        side.addWidget(btn_mic)

        btn_pause = QPushButton("⏸️ Pauza EEG")
        btn_pause.clicked.connect(self.toggle_timer)
        side.addWidget(btn_pause)

        bottom.addLayout(side, 1)
        main.addLayout(bottom)

        # Input
        self.input_line = QLineEdit()
        self.btn_send = QPushButton("Wyślij do CIEL/Ω")
        self.btn_send.clicked.connect(self.send_message)
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
            safe_chat_add(self.chat_log, f"⚠️ Błąd silnika: {e}")
            return None

    def update_visuals(self):
        if self.paused:
            return

        if self.engine:
            result = self._get_status_result()
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
        self.ax_eeg.set_ylabel("Amplituda", color="white")
        self.ax_eeg.set_xlabel("Czas (krok)", color="white")
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
        self.ax_tensor.set_title("Tensor Intencji (Ψ/Σ)", color="white", fontweight='bold')
        self.ax_tensor.tick_params(colors='white')
        self.ax_tensor.spines['bottom'].set_color('white')
        self.ax_tensor.spines['top'].set_color('white')
        self.ax_tensor.spines['right'].set_color('white')
        self.ax_tensor.spines['left'].set_color('white')
        cbar = self.fig_tensor.colorbar(im, ax=self.ax_tensor)
        cbar.ax.tick_params(colors='white')
        self.canvas_tensor.draw()

        # Kamera
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytes_per_line = ch * w
                img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(img).scaled(200, 150, Qt.KeepAspectRatio))
            else:
                # Kamera przestała działać
                self.cap.release()
                self.cap = None
                self.video_label.setText("📷 Kamera wyłączona")

        self.label_status.setText(f"Lambda₀: {lambda_val}")

    def toggle_timer(self):
        self.paused = not self.paused

    def toggle_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
            self.video_label.setText("📷 Kamera wyłączona")
        else:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.cap = None
                safe_chat_add(self.chat_log, "⚠️ Nie można otworzyć kamery")
                self.video_label.setText("📷 Błąd kamery")

    def toggle_mic(self):
        if not self.recording:
            self.recording = True
            self.audio_thread = threading.Thread(target=self.record_audio, daemon=True)
            self.audio_thread.start()
            safe_chat_add(self.chat_log, "🎙️ Mikrofon: nagrywanie...")
        else:
            self.recording = False
            safe_chat_add(self.chat_log, "🛑 Mikrofon: zatrzymano")

    def record_audio(self):
        try:
            fs = 44100
            duration = 5
            audio = sd.rec(int(duration*fs), samplerate=fs, channels=2)
            # Czekaj aż nagranie się zakończy lub użytkownik zatrzyma
            for _ in range(duration * 10):  # Sprawdzaj co 100ms
                if not self.recording:
                    sd.stop()
                    return
                sd.sleep(100)
            if not self.recording:
                sd.stop()
                return
            sd.wait()
            if self.recording:  # Sprawdź ponownie po zakończeniu nagrywania
                sf.write("nagranie.wav", audio, fs)
                # Użyj QTimer.singleShot aby wywołać z głównego wątku
                QTimer.singleShot(0, lambda: safe_chat_add(self.chat_log, "🎧 Zapisano jako nagranie.wav"))
        except Exception as e:
            # Użyj QTimer.singleShot aby wywołać z głównego wątku
            error_msg = f"⚠️ Błąd nagrywania: {e}"
            QTimer.singleShot(0, lambda msg=error_msg: safe_chat_add(self.chat_log, msg))
        finally:
            self.recording = False

    def send_message(self):
        user = self.input_line.text().strip()
        if not user:
            return

        tryb = self.mode_selector.currentText()
        pamiec = self.memory_selector.currentText()
        safe_chat_add(self.chat_log, f"Ty ({tryb}/{pamiec}): {user}")

        if self.engine:
            try:
                profile = self.llm_profile_selector.currentText() if hasattr(self, "llm_profile_selector") else "standard"
                if self.llm_bundle is not None:
                    self.engine.language_backend = self.llm_bundle.primary_for(profile)
                    self.engine.aux_backend = self.llm_bundle.composite_aux()

                self.dialogue.append({"role": "user", "content": user})
                t0 = time.perf_counter()
                result = self.engine.interact(user, self.dialogue, context=tryb)
                latency_ms = (time.perf_counter() - t0) * 1000.0
                safe_chat_add(self.chat_log, f"⏱️ latency: {latency_ms:.1f} ms")
            except Exception as e:
                safe_chat_add(self.chat_log, f"⚠️ Błąd silnika przy step: {e}")
                result = None

            reply = dig(result, "reply", default=None)
            if reply is None:
                reply = dig(result, "ciel_state", "cognition", default=None)
            if isinstance(reply, (dict, list)):
                response_str = json.dumps(reply, ensure_ascii=False, indent=2)
            else:
                response_str = str(reply)

            if result is not None:
                self.dialogue.append({"role": "assistant", "content": response_str})

            lambda_val = dig(result, "ciel_state", "simulation", "lambda0", default=None)
            if lambda_val is None:
                lambda_val = round(random.uniform(0.3,0.9),3)
        else:
            state = random.choice(["spokojny","aktywny","rozproszony"])
            ud = random.randint(20,90)
            response_str = (
                f"Analiza zakończona. Stan emocjonalny: {state}. Wskaźnik ŨD: {ud}%.\n"
                f"CIEL ({tryb}): " + random.choice([
                    "Twoje intencje rezonują w polu koherencji.",
                    "Wykryto skok aktywności fal β.",
                    "Tensor wskazuje skupienie na zadaniu.",
                    "Tryb analityczny aktywowany."
                ])
            )
            lambda_val = round(random.uniform(0.3,0.9),3)

        safe_chat_add(self.chat_log, response_str)
        self.label_status.setText(f"Lambda₀: {lambda_val}")
        self.input_line.clear()
        self.autosave_chat()

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
            safe_chat_add(self.chat_log, f"⚠️ Błąd zapisu autosave: {e}")

    def export_json(self):
        self.autosave_chat()
        safe_chat_add(self.chat_log, "✅ Eksport JSON zakończony.")

    def export_pdf(self):
        try:
            pdf = pdfcanvas.Canvas("ciel_raport.pdf", pagesize=A4)
            textobject = pdf.beginText(40, 800)
            textobject.setFont("Helvetica", 10)
            y_position = 800
            for i in range(self.chat_log.count()):
                line = self.chat_log.item(i).text()
                # Długie linie mogą być problemem - ogranicz długość
                if len(line) > 100:
                    # Podziel długie linie
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 100:
                            current_line += word + " "
                        else:
                            if current_line:
                                textobject.textLine(current_line.strip())
                                y_position -= 12
                                if y_position < 50:  # Nowa strona jeśli potrzeba
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
                    if y_position < 50:  # Nowa strona jeśli potrzeba
                        pdf.drawText(textobject)
                        pdf.showPage()
                        textobject = pdf.beginText(40, 800)
                        y_position = 800
            pdf.drawText(textobject)
            pdf.save()
            safe_chat_add(self.chat_log, "📄 PDF zapisany jako ciel_raport.pdf")
        except Exception as e:
            safe_chat_add(self.chat_log, f"⚠️ Błąd przy zapisie PDF: {e}")

    def load_file(self):
        path,_ = QFileDialog.getOpenFileName(self, "Wybierz plik")
        if path:
            safe_chat_add(self.chat_log, f"📂 Wczytano plik: {path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CIELUltra()
    win.show()
    sys.exit(app.exec_())

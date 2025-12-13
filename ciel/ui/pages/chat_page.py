from __future__ import annotations

import json
import threading
import time
from typing import Any, Dict, Optional

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QApplication,
)

from ..engine_bridge import EngineBridge
from ..settings_store import save_settings
from ..widgets import ChatInput, ChatTranscript


class ChatPage(QWidget):
    def __init__(self, *, bridge: EngineBridge, settings: Dict[str, Any], parent=None) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._settings = settings
        self._busy = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        top_row = QHBoxLayout()
        layout.addLayout(top_row)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["standard", "creative", "analytic", "experimental"])
        self.mode_selector.setCurrentText(str((settings.get("chat") or {}).get("mode") or "standard"))
        top_row.addWidget(QLabel("Mode"))
        top_row.addWidget(self.mode_selector)

        self.memory_selector = QComboBox()
        self.memory_selector.addItems(["echo", "dream", "adam", "braid"])
        self.memory_selector.setCurrentText(str((settings.get("chat") or {}).get("memory") or "echo"))
        top_row.addWidget(QLabel("Memory"))
        top_row.addWidget(self.memory_selector)

        self.profile_selector = QComboBox()
        for label, key in [
            ("Lite", "lite"),
            ("Standard", "standard"),
            ("Science", "science"),
            ("Ultra", "ultra"),
        ]:
            self.profile_selector.addItem(label, key)
        profile_default = str((settings.get("chat") or {}).get("profile") or "standard").strip().lower()
        index = self.profile_selector.findData(profile_default)
        if index >= 0:
            self.profile_selector.setCurrentIndex(index)
        top_row.addWidget(QLabel("Profile"))
        top_row.addWidget(self.profile_selector)

        top_row.addStretch(1)

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_chat)
        top_row.addWidget(self.btn_clear)

        self.btn_copy = QPushButton("Copy")
        self.btn_copy.clicked.connect(self.copy_chat)
        top_row.addWidget(self.btn_copy)

        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save_chat)
        top_row.addWidget(self.btn_save)

        self.transcript = ChatTranscript()
        layout.addWidget(self.transcript, 1)

        bottom_row = QHBoxLayout()
        layout.addLayout(bottom_row)

        self.busy_label = QLabel("")
        self.busy_label.setStyleSheet("border: none; background: transparent; color: #94a3b8;")
        bottom_row.addWidget(self.busy_label)
        bottom_row.addStretch(1)

        input_row = QHBoxLayout()
        layout.addLayout(input_row)

        self.input = ChatInput()
        self.input.setPlaceholderText("Type a message. Enter sends, Shift+Enter adds a new line.")
        self.input.setFixedHeight(70)
        self.input.sendRequested.connect(self.send)
        input_row.addWidget(self.input, 1)

        self.btn_send = QPushButton("Send")
        self.btn_send.clicked.connect(self.send)
        input_row.addWidget(self.btn_send)

    def _persist_chat_settings(self) -> None:
        chat_cfg = self._settings.get("chat") or {}
        chat_cfg["mode"] = str(self.mode_selector.currentText())
        chat_cfg["memory"] = str(self.memory_selector.currentText())
        chat_cfg["profile"] = str(self.profile_selector.currentData())
        self._settings["chat"] = chat_cfg
        save_settings(self._settings)

    def set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.btn_send.setEnabled(not busy)
        self.input.setEnabled(not busy)
        self.busy_label.setText("Thinking…" if busy else "")

    def append_system(self, text: str) -> None:
        self.transcript.append_message(role="system", content=text, meta={"ts": time.time()})

    def clear_chat(self) -> None:
        self._bridge.reset_dialogue()
        self.transcript.clear_transcript()
        self.append_system("Conversation cleared.")

    def copy_chat(self) -> None:
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.transcript.transcript_plaintext())
            self.append_system("Transcript copied to clipboard.")
        except Exception:
            self.append_system("Failed to copy transcript.")

    def save_chat(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save transcript", "", "Text (*.txt);;All files (*)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.transcript.transcript_plaintext())
            self.append_system(f"Saved to {path}")
        except Exception as exc:
            self.append_system(f"Save failed: {exc}")

    def send(self) -> None:
        if self._busy:
            return

        text = self.input.toPlainText().strip()
        if not text:
            return

        self._persist_chat_settings()

        mode = str(self.mode_selector.currentText())
        memory = str(self.memory_selector.currentText())
        profile = str(self.profile_selector.currentData())

        self.input.clear()

        self.transcript.append_message(
            role="user",
            content=f"[{mode}/{memory}]\n\n{text}",
            meta={"ts": time.time()},
        )

        if not self._bridge.is_available():
            self.transcript.append_message(
                role="assistant",
                content="Engine is unavailable.\n\nRun this inside an environment with all dependencies installed.",
                meta={"ts": time.time()},
            )
            return

        self.set_busy(True)
        threading.Thread(
            target=self._run_interact,
            args=(text, mode, profile),
            daemon=True,
        ).start()

    def _run_interact(self, text: str, mode: str, profile: str) -> None:
        result: Optional[Dict[str, Any]] = None
        error: Optional[str] = None
        latency_ms: Optional[float] = None

        try:
            result = self._bridge.interact(user_text=text, mode=mode, profile=profile)
            latency_ms = self._bridge.last_latency_ms
        except Exception as exc:
            error = str(exc)

        QTimer.singleShot(
            0,
            lambda: self._on_interact_done(result=result, error=error, latency_ms=latency_ms),
        )

    def _on_interact_done(
        self,
        *,
        result: Optional[Dict[str, Any]],
        error: Optional[str],
        latency_ms: Optional[float],
    ) -> None:
        try:
            if error is not None:
                self.transcript.append_message(
                    role="assistant",
                    content=f"Error: {error}",
                    meta={"ts": time.time()},
                )
                return

            reply: Any = None
            if result is not None:
                reply = result.get("reply")
                if reply is None:
                    reply = ((result.get("ciel_state") or {}).get("cognition"))

            if isinstance(reply, (dict, list)):
                text = json.dumps(reply, ensure_ascii=False, indent=2)
            else:
                text = str(reply) if reply is not None else ""

            meta: Dict[str, Any] = {"ts": time.time()}
            if latency_ms is not None:
                meta["latency_ms"] = latency_ms

            self.transcript.append_message(role="assistant", content=text, meta=meta)
        finally:
            self.set_busy(False)
            self.input.setFocus()


__all__ = ["ChatPage"]

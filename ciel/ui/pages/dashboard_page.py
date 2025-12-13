from __future__ import annotations

from typing import Any, Dict, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QGroupBox, QFormLayout


class DashboardPage(QWidget):
    def __init__(self, *, settings: Dict[str, Any], parent=None) -> None:
        super().__init__(parent)
        self._settings = settings

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title = QLabel("System overview")
        self.title.setStyleSheet("border: none; background: transparent; font-size: 16px; font-weight: 700;")
        self.title.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.title)

        self.status_group = QGroupBox("Status")
        status_form = QFormLayout()
        self.status_group.setLayout(status_form)

        self.backend_value = QLabel("-")
        self.engine_value = QLabel("-")
        self.latency_value = QLabel("-")
        self.lambda_value = QLabel("-")

        status_form.addRow("Backend", self.backend_value)
        status_form.addRow("Engine", self.engine_value)
        status_form.addRow("Last latency", self.latency_value)
        status_form.addRow("Lambda₀", self.lambda_value)

        layout.addWidget(self.status_group)

        self.models_group = QGroupBox("Models")
        models_form = QFormLayout()
        self.models_group.setLayout(models_form)

        self.model_lite = QLabel("-")
        self.model_standard = QLabel("-")
        self.model_science = QLabel("-")

        models_form.addRow("Lite", self.model_lite)
        models_form.addRow("Standard", self.model_standard)
        models_form.addRow("Science", self.model_science)

        layout.addWidget(self.models_group)
        layout.addStretch(1)

    def refresh(
        self,
        *,
        engine_available: bool,
        backend: str,
        last_latency_ms: Optional[float],
        last_lambda0: Optional[float],
        settings: Dict[str, Any],
    ) -> None:
        self.backend_value.setText(str(backend))
        self.engine_value.setText("available" if engine_available else "unavailable")

        if last_latency_ms is None:
            self.latency_value.setText("-")
        else:
            self.latency_value.setText(f"{float(last_latency_ms):.0f} ms")

        if last_lambda0 is None:
            self.lambda_value.setText("-")
        else:
            self.lambda_value.setText(f"{float(last_lambda0):.3f}")

        backend_key = (settings.get("backend") or "hf").strip().lower()
        if backend_key == "gguf":
            gguf_cfg = settings.get("gguf") or {}
            self.model_lite.setText(str(gguf_cfg.get("lite_model_path") or "(auto)"))
            self.model_standard.setText(str(gguf_cfg.get("standard_model_path") or "(auto)"))
            self.model_science.setText(str(gguf_cfg.get("science_model_path") or "(auto)"))
        else:
            hf_cfg = settings.get("hf") or {}
            self.model_lite.setText(str(hf_cfg.get("lite_model") or ""))
            self.model_standard.setText(str(hf_cfg.get("standard_model") or ""))
            self.model_science.setText(str(hf_cfg.get("science_model") or ""))


__all__ = ["DashboardPage"]

from __future__ import annotations

import threading
from typing import Any, Dict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)

from ..engine_bridge import EngineBridge
from ..settings_store import DEFAULT_SETTINGS, save_settings


class SettingsPage(QWidget):
    install_done = pyqtSignal(str, object, object)

    def __init__(self, *, bridge: EngineBridge, settings: Dict[str, Any], parent=None) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._settings = settings
        self._install_thread: threading.Thread | None = None
        self.install_done.connect(self._on_install_done)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.backend_group = QGroupBox("Backend")
        backend_form = QFormLayout()
        self.backend_group.setLayout(backend_form)

        self.backend_selector = QComboBox()
        self.backend_selector.addItem("HF (Transformers)", "hf")
        self.backend_selector.addItem("GGUF (llama.cpp)", "gguf")
        backend_value = str(settings.get("backend") or "hf").strip().lower()
        self.backend_selector.setCurrentIndex(1 if backend_value == "gguf" else 0)
        self.backend_selector.currentIndexChanged.connect(self._toggle_groups)
        backend_form.addRow("Backend", self.backend_selector)

        layout.addWidget(self.backend_group)

        self.hf_group = QGroupBox("HF models")
        hf_form = QFormLayout()
        self.hf_group.setLayout(hf_form)

        hf_cfg = settings.get("hf") or {}
        self.hf_lite = QLineEdit(str(hf_cfg.get("lite_model") or "phi-3-mini-3.8b"))
        self.hf_standard = QLineEdit(str(hf_cfg.get("standard_model") or "mistral-7b-instruct"))
        self.hf_science = QLineEdit(str(hf_cfg.get("science_model") or "qwen2.5-7b-instruct"))
        self.hf_analysis = QLineEdit(str(hf_cfg.get("analysis_model") or "phi-3-mini-3.8b"))
        self.hf_validator = QLineEdit(str(hf_cfg.get("validator_model") or "mistral-7b-instruct"))

        hf_form.addRow("Lite", self.hf_lite)
        hf_form.addRow("Standard", self.hf_standard)
        hf_form.addRow("Science", self.hf_science)
        hf_form.addRow("Analysis", self.hf_analysis)
        hf_form.addRow("Validator", self.hf_validator)

        layout.addWidget(self.hf_group)

        self.gguf_group = QGroupBox("GGUF models")
        gguf_form = QFormLayout()
        self.gguf_group.setLayout(gguf_form)

        gguf_cfg = settings.get("gguf") or {}

        self.gguf_models_dir = self._make_dir_row(str(gguf_cfg.get("models_dir") or ""))
        gguf_form.addRow("Models dir", self.gguf_models_dir["row"])

        self.gguf_lite = self._make_path_row(str(gguf_cfg.get("lite_model_path") or ""))
        self.gguf_standard = self._make_path_row(str(gguf_cfg.get("standard_model_path") or ""))
        self.gguf_science = self._make_path_row(str(gguf_cfg.get("science_model_path") or ""))

        gguf_form.addRow("Lite model", self.gguf_lite["row"])
        gguf_form.addRow("Standard model", self.gguf_standard["row"])
        gguf_form.addRow("Science model", self.gguf_science["row"])

        self.gguf_n_ctx = QSpinBox()
        self.gguf_n_ctx.setRange(256, 262144)
        self.gguf_n_ctx.setValue(int(gguf_cfg.get("n_ctx") or 2048))
        gguf_form.addRow("n_ctx", self.gguf_n_ctx)

        self.gguf_n_threads = QSpinBox()
        self.gguf_n_threads.setRange(1, 256)
        self.gguf_n_threads.setValue(int(gguf_cfg.get("n_threads") or 4))
        gguf_form.addRow("n_threads", self.gguf_n_threads)

        self.gguf_n_gpu_layers = QSpinBox()
        self.gguf_n_gpu_layers.setRange(0, 256)
        self.gguf_n_gpu_layers.setValue(int(gguf_cfg.get("n_gpu_layers") or 0))
        gguf_form.addRow("n_gpu_layers", self.gguf_n_gpu_layers)

        self.gguf_system_prompt = QLineEdit(str(gguf_cfg.get("system_prompt") or ""))
        gguf_form.addRow("System prompt", self.gguf_system_prompt)

        self.gguf_install_profile = QComboBox()
        for label, key in [("Lite", "lite"), ("Standard", "standard"), ("Science", "science")]:
            self.gguf_install_profile.addItem(label, key)
        install_profile = str(gguf_cfg.get("install_profile") or "standard").strip().lower()
        index = self.gguf_install_profile.findData(install_profile)
        if index >= 0:
            self.gguf_install_profile.setCurrentIndex(index)
        gguf_form.addRow("Install profile", self.gguf_install_profile)

        self.gguf_install_url = QLineEdit(str(gguf_cfg.get("install_url") or ""))
        self.gguf_install_url.setPlaceholderText("https://.../model.gguf")
        gguf_form.addRow("Install URL", self.gguf_install_url)

        self.gguf_install_sha256 = QLineEdit(str(gguf_cfg.get("install_sha256") or ""))
        self.gguf_install_sha256.setPlaceholderText("sha256:...")
        gguf_form.addRow("Install SHA256", self.gguf_install_sha256)

        install_row = QWidget()
        install_layout = QHBoxLayout()
        install_layout.setContentsMargins(0, 0, 0, 0)
        install_row.setLayout(install_layout)
        self.btn_gguf_install = QPushButton("Install")
        self.btn_gguf_install.clicked.connect(self.install_gguf)
        install_layout.addWidget(self.btn_gguf_install)
        install_layout.addStretch(1)
        gguf_form.addRow("", install_row)

        layout.addWidget(self.gguf_group)

        self.actions_group = QGroupBox("Actions")
        actions_row = QHBoxLayout()
        self.actions_group.setLayout(actions_row)

        self.btn_apply = QPushButton("Apply")
        self.btn_apply.clicked.connect(self.apply)
        actions_row.addWidget(self.btn_apply)

        self.btn_defaults = QPushButton("Restore defaults")
        self.btn_defaults.clicked.connect(self.restore_defaults)
        actions_row.addWidget(self.btn_defaults)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("border: none; background: transparent; color: #94a3b8;")
        actions_row.addWidget(self.status_label, 1)

        layout.addWidget(self.actions_group)
        layout.addStretch(1)

        self._toggle_groups()

    def _make_path_row(self, value: str) -> Dict[str, Any]:
        row = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row.setLayout(row_layout)

        edit = QLineEdit(value)
        btn = QPushButton("Browse")
        row_layout.addWidget(edit, 1)
        row_layout.addWidget(btn)

        btn.clicked.connect(lambda: self._browse_into(edit))

        return {"row": row, "edit": edit, "button": btn}

    def _make_dir_row(self, value: str) -> Dict[str, Any]:
        row = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row.setLayout(row_layout)

        edit = QLineEdit(value)
        btn = QPushButton("Browse")
        row_layout.addWidget(edit, 1)
        row_layout.addWidget(btn)

        btn.clicked.connect(lambda: self._browse_dir_into(edit))

        return {"row": row, "edit": edit, "button": btn}

    def _browse_into(self, edit: QLineEdit) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select GGUF model", "", "GGUF (*.gguf);;All files (*)")
        if path:
            edit.setText(path)

    def _browse_dir_into(self, edit: QLineEdit) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select GGUF models directory", edit.text().strip() or "")
        if path:
            edit.setText(path)

    def _toggle_groups(self) -> None:
        backend = str(self.backend_selector.currentData() or "hf").strip().lower()
        self.hf_group.setVisible(backend == "hf")
        self.gguf_group.setVisible(backend == "gguf")

    def apply(self) -> None:
        backend = str(self.backend_selector.currentData() or "hf").strip().lower()
        self._settings["backend"] = backend

        hf_cfg = {
            "lite_model": self.hf_lite.text().strip(),
            "standard_model": self.hf_standard.text().strip(),
            "science_model": self.hf_science.text().strip(),
            "analysis_model": self.hf_analysis.text().strip(),
            "validator_model": self.hf_validator.text().strip(),
            "device": None,
        }
        self._settings["hf"] = hf_cfg

        gguf_cfg = {
            "models_dir": self.gguf_models_dir["edit"].text().strip(),
            "lite_model_path": self.gguf_lite["edit"].text().strip(),
            "standard_model_path": self.gguf_standard["edit"].text().strip(),
            "science_model_path": self.gguf_science["edit"].text().strip(),
            "n_ctx": int(self.gguf_n_ctx.value()),
            "n_threads": int(self.gguf_n_threads.value()),
            "n_gpu_layers": int(self.gguf_n_gpu_layers.value()),
            "system_prompt": self.gguf_system_prompt.text(),
            "install_profile": str(self.gguf_install_profile.currentData() or "standard"),
            "install_url": self.gguf_install_url.text().strip(),
            "install_sha256": self.gguf_install_sha256.text().strip(),
        }
        self._settings["gguf"] = gguf_cfg

        save_settings(self._settings)
        self._bridge.apply_settings(self._settings)
        self.status_label.setText("Settings applied")

    def restore_defaults(self) -> None:
        self._settings.clear()
        self._settings.update(DEFAULT_SETTINGS)
        save_settings(self._settings)
        self._bridge.apply_settings(self._settings)

        backend = str(self._settings.get("backend") or "hf")
        self.backend_selector.setCurrentIndex(1 if backend == "gguf" else 0)

        hf_cfg = self._settings.get("hf") or {}
        self.hf_lite.setText(str(hf_cfg.get("lite_model") or ""))
        self.hf_standard.setText(str(hf_cfg.get("standard_model") or ""))
        self.hf_science.setText(str(hf_cfg.get("science_model") or ""))
        self.hf_analysis.setText(str(hf_cfg.get("analysis_model") or ""))
        self.hf_validator.setText(str(hf_cfg.get("validator_model") or ""))

        gguf_cfg = self._settings.get("gguf") or {}
        self.gguf_models_dir["edit"].setText(str(gguf_cfg.get("models_dir") or ""))
        self.gguf_lite["edit"].setText(str(gguf_cfg.get("lite_model_path") or ""))
        self.gguf_standard["edit"].setText(str(gguf_cfg.get("standard_model_path") or ""))
        self.gguf_science["edit"].setText(str(gguf_cfg.get("science_model_path") or ""))
        self.gguf_n_ctx.setValue(int(gguf_cfg.get("n_ctx") or 2048))
        self.gguf_n_threads.setValue(int(gguf_cfg.get("n_threads") or 4))
        self.gguf_n_gpu_layers.setValue(int(gguf_cfg.get("n_gpu_layers") or 0))
        self.gguf_system_prompt.setText(str(gguf_cfg.get("system_prompt") or ""))

        install_profile = str(gguf_cfg.get("install_profile") or "standard").strip().lower()
        index = self.gguf_install_profile.findData(install_profile)
        if index >= 0:
            self.gguf_install_profile.setCurrentIndex(index)
        self.gguf_install_url.setText(str(gguf_cfg.get("install_url") or ""))
        self.gguf_install_sha256.setText(str(gguf_cfg.get("install_sha256") or ""))

        self.status_label.setText("Defaults restored")

    def install_gguf(self) -> None:
        url = self.gguf_install_url.text().strip()
        if not url:
            self.status_label.setText("Install URL is empty")
            return

        sha256 = self.gguf_install_sha256.text().strip()
        profile = str(self.gguf_install_profile.currentData() or "standard")
        models_dir = self.gguf_models_dir["edit"].text().strip()

        self.btn_gguf_install.setEnabled(False)
        self.status_label.setText("Downloading...")

        self._install_thread = threading.Thread(
            target=self._run_install_gguf,
            args=(url, sha256, profile, models_dir),
            daemon=True,
        )
        self._install_thread.start()

    def _run_install_gguf(self, url: str, sha256: str, profile: str, models_dir: str) -> None:
        path: str | None = None
        error: str | None = None
        try:
            from ...gguf_installer import install_gguf_model

            path = install_gguf_model(
                url=url,
                models_dir=models_dir or None,
                expected_sha256=sha256 or None,
                profile=profile,
            )
        except Exception as exc:
            error = str(exc)

        self.install_done.emit(profile, path, error)

    def _on_install_done(self, profile: str, path: object, error: object) -> None:
        self.btn_gguf_install.setEnabled(True)

        if error:
            self.status_label.setText(f"Install failed: {error}")
            return

        if not path:
            self.status_label.setText("Install failed")
            return

        path_str = str(path)

        key = (profile or "standard").strip().lower()
        if key == "lite":
            self.gguf_lite["edit"].setText(path_str)
        elif key == "science":
            self.gguf_science["edit"].setText(path_str)
        else:
            self.gguf_standard["edit"].setText(path_str)

        self.apply()
        self.status_label.setText(f"Installed: {path_str}")


__all__ = ["SettingsPage"]

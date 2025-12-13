from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def _configure_qt(argv: Optional[list[str]] = None) -> None:
    argv = argv or sys.argv

    if os.environ.get("DISPLAY") is None or "--headless" in argv:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    spec = importlib.util.find_spec("PyQt5")
    if spec and spec.origin:
        pyqt_root = os.path.dirname(spec.origin)
        qt_plugins = os.path.join(pyqt_root, "Qt5", "plugins")
        qt_platforms = os.path.join(qt_plugins, "platforms")
        if os.path.isdir(qt_plugins):
            os.environ.setdefault("QT_PLUGIN_PATH", qt_plugins)
        if os.path.isdir(qt_platforms):
            os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", qt_platforms)


_configure_qt()

from PyQt5.QtCore import QTimer, Qt  # noqa: E402
from PyQt5.QtGui import QPixmap  # noqa: E402
from PyQt5.QtWidgets import (  # noqa: E402
    QApplication,
    QLabel,
    QListWidget,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)

from .engine_bridge import EngineBridge  # noqa: E402
from .pages import ChatPage, DashboardPage, RealtimePage, SettingsPage  # noqa: E402
from .settings_store import load_settings, save_settings  # noqa: E402
from .theme import dark_stylesheet  # noqa: E402


class ControlCenterWindow(QWidget):
    def __init__(self, *, bridge: EngineBridge, settings: Dict[str, Any], parent=None) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._settings = settings

        self.setWindowTitle("CIEL/Ω Control Center")

        window_cfg = settings.get("window") or {}
        try:
            self.resize(int(window_cfg.get("width") or 1400), int(window_cfg.get("height") or 800))
        except Exception:
            self.resize(1400, 800)

        layout = QVBoxLayout()
        self.setLayout(layout)

        header = QHBoxLayout()
        layout.addLayout(header)

        self.logo_label = QLabel()
        logo_path = Path(__file__).resolve().parents[2] / "Logo1.png"
        if logo_path.is_file():
            pixmap = QPixmap(str(logo_path))
            self.logo_label.setPixmap(pixmap.scaledToHeight(48, Qt.SmoothTransformation))
        else:
            self.logo_label.setText("CIEL/Ω")
        self.logo_label.setStyleSheet("border: none; background: transparent;")

        title = QLabel("CIEL/Ω Control Center")
        title.setStyleSheet("border: none; background: transparent; font-size: 18px; font-weight: 700;")

        header.addWidget(self.logo_label)
        header.addWidget(title)
        header.addStretch(1)

        body = QHBoxLayout()
        layout.addLayout(body, 1)

        self.nav = QListWidget()
        self.nav.setFixedWidth(190)
        self.nav.addItem("Dashboard")
        self.nav.addItem("Realtime")
        self.nav.addItem("Chat")
        self.nav.addItem("Settings")
        self.nav.currentRowChanged.connect(self._on_nav_changed)
        body.addWidget(self.nav)

        self.stack = QStackedWidget()
        body.addWidget(self.stack, 1)

        self.page_dashboard = DashboardPage(settings=self._settings)
        self.page_realtime = RealtimePage(bridge=self._bridge, settings=self._settings)
        self.page_chat = ChatPage(bridge=self._bridge, settings=self._settings)
        self.page_settings = SettingsPage(bridge=self._bridge, settings=self._settings)

        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_realtime)
        self.stack.addWidget(self.page_chat)
        self.stack.addWidget(self.page_settings)

        self.nav.setCurrentRow(0)

        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(750)
        self.refresh_timer.timeout.connect(self._refresh_dashboard)
        self.refresh_timer.start()

        self._refresh_dashboard()

    def _on_nav_changed(self, row: int) -> None:
        try:
            self.stack.setCurrentIndex(int(row))
        except Exception:
            pass

    def _refresh_dashboard(self) -> None:
        try:
            backend = str(self._settings.get("backend") or "hf")
            self.page_dashboard.refresh(
                engine_available=self._bridge.is_available(),
                backend=backend,
                last_latency_ms=self._bridge.last_latency_ms,
                last_lambda0=self._bridge.last_lambda0,
                settings=self._settings,
            )
        except Exception:
            return

    def closeEvent(self, event) -> None:
        try:
            window_cfg = self._settings.get("window") or {}
            window_cfg["width"] = int(self.width())
            window_cfg["height"] = int(self.height())
            self._settings["window"] = window_cfg
            save_settings(self._settings)
        except Exception:
            pass

        try:
            if hasattr(self, "page_realtime"):
                self.page_realtime.shutdown()
        except Exception:
            pass

        try:
            self._bridge.shutdown()
        except Exception:
            pass

        super().closeEvent(event)


def run_control_center(argv: Optional[list[str]] = None) -> int:
    argv = argv or sys.argv

    _configure_qt(argv)

    app = QApplication.instance() or QApplication(argv)
    try:
        app.setStyleSheet(dark_stylesheet())
    except Exception:
        pass

    settings = load_settings()
    bridge = EngineBridge(settings)

    win = ControlCenterWindow(bridge=bridge, settings=settings)
    win.show()

    return int(app.exec_())


__all__ = ["run_control_center", "ControlCenterWindow"]

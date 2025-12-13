from __future__ import annotations

ACCENT = "#3b82f6"
BG = "#0f172a"
PANEL_BG = "#1e293b"
BORDER = "#475569"
TEXT = "#e2e8f0"
MUTED_TEXT = "#94a3b8"


def dark_stylesheet() -> str:
    return """
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
        QPushButton:disabled {
            background-color: #334155;
            color: #94a3b8;
            border-color: #475569;
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
        QTextEdit {
            border: 1px solid #475569;
            border-radius: 6px;
            background-color: #1e293b;
            color: #e2e8f0;
            padding: 10px;
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
        QGroupBox {
            border: 1px solid #475569;
            border-radius: 8px;
            margin-top: 10px;
            padding: 10px;
            background-color: #0f172a;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 6px;
            color: #94a3b8;
        }
        QTabWidget::pane {
            border: 1px solid #475569;
            border-radius: 8px;
            background-color: #0f172a;
        }
        QTabBar::tab {
            background-color: #1e293b;
            border: 1px solid #475569;
            border-bottom: none;
            padding: 8px 12px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #0f172a;
            border-color: #60a5fa;
        }
    """.strip()


__all__ = ["dark_stylesheet", "ACCENT", "BG", "PANEL_BG", "BORDER", "TEXT", "MUTED_TEXT"]

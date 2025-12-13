from __future__ import annotations

from .chat_page import ChatPage
from .dashboard_page import DashboardPage
from .graphs_page import GraphsPage
from .realtime_page import RealtimePage
from .settings_page import SettingsPage

__all__: list[str] = ["ChatPage", "DashboardPage", "GraphsPage", "RealtimePage", "SettingsPage"]

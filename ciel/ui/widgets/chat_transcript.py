from __future__ import annotations

import html
import time
from typing import Any, Dict, Optional

from PyQt5.QtWidgets import QTextBrowser


def _markdown_to_html(text: str) -> str:
    try:
        import markdown

        return markdown.markdown(text, extensions=["fenced_code", "tables"], output_format="html5")
    except Exception:
        escaped = html.escape(text)
        return escaped.replace("\n", "<br/>")


class ChatTranscript(QTextBrowser):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setOpenExternalLinks(True)
        self.setReadOnly(True)
        self._messages_html: list[str] = []

        self.document().setDefaultStyleSheet(
            """
            body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; }
            .wrap { margin: 6px 0; }
            .meta { color: #94a3b8; font-size: 11px; margin-bottom: 4px; }
            .bubble { padding: 10px 12px; border-radius: 10px; border: 1px solid #475569; }
            .user { background: #1e40af; color: #ffffff; }
            .assistant { background: #334155; color: #e2e8f0; }
            .system { background: #0f172a; color: #94a3b8; border-style: dashed; }
            pre { background: #0b1220; border: 1px solid #475569; padding: 10px; border-radius: 8px; overflow-x: auto; }
            code { font-family: 'JetBrains Mono', 'Consolas', monospace; }
            a { color: #60a5fa; }
            """.strip()
        )

    def append_message(
        self,
        *,
        role: str,
        content: str,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        role_key = (role or "system").strip().lower()
        if role_key not in {"user", "assistant", "system"}:
            role_key = "system"

        meta_parts: list[str] = []
        meta = meta or {}
        ts = meta.get("ts")
        if ts is None:
            ts = time.time()
        try:
            meta_parts.append(time.strftime("%H:%M:%S", time.localtime(float(ts))))
        except Exception:
            pass

        latency = meta.get("latency_ms")
        if latency is not None:
            try:
                meta_parts.append(f"{float(latency):.0f} ms")
            except Exception:
                pass

        meta_text = " · ".join(meta_parts)
        safe_meta = html.escape(meta_text)

        body_html = _markdown_to_html(content or "")
        msg_html = (
            f"<div class='wrap'>"
            f"<div class='meta'>{safe_meta}</div>"
            f"<div class='bubble {role_key}'>{body_html}</div>"
            f"</div>"
        )

        self._messages_html.append(msg_html)
        self.setHtml("<body>" + "".join(self._messages_html) + "</body>")
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def clear_transcript(self) -> None:
        self._messages_html = []
        self.setHtml("<body></body>")

    def transcript_plaintext(self) -> str:
        return self.toPlainText()


__all__ = ["ChatTranscript"]

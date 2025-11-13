"""Simple in-memory representation of persistent clusters."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, MutableMapping, Sequence


@dataclass
class ClusterEntry:
    symbol: str
    intent: str
    tensor: Sequence[float]
    metadata: Mapping[str, object]
    table: Mapping[str, object]


@dataclass
class PersistentMemory:
    """Stores entries grouped by symbol/intent in plain Python structures."""

    clusters: MutableMapping[str, MutableMapping[str, List[ClusterEntry]]] = field(default_factory=dict)

    def store(
        self,
        symbol: str,
        intent: str,
        tensor: Sequence[float],
        metadata: Mapping[str, object] | None = None,
        table: Mapping[str, object] | None = None,
    ) -> Dict[str, object]:
        metadata = metadata or {}
        table = table or {}
        symbol_map = self.clusters.setdefault(symbol, {})
        intent_entries = symbol_map.setdefault(intent, [])
        entry = ClusterEntry(symbol=symbol, intent=intent, tensor=list(tensor), metadata=metadata, table=table)
        intent_entries.append(entry)
        return {
            "symbol": symbol,
            "intent": intent,
            "count": len(intent_entries),
        }


__all__ = ["PersistentMemory", "ClusterEntry"]

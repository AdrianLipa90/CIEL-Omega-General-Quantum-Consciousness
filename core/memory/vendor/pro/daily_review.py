#!/usr/bin/env python3
from ciel_memory.orchestrator import UnifiedMemoryOrchestrator
if __name__ == "__main__":
    orch = UnifiedMemoryOrchestrator()
    stats = orch.daily_maintenance()
    print("[daily-review]", stats)

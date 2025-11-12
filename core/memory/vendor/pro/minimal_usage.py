from ciel_memory.orchestrator import UnifiedMemoryOrchestrator
orch = UnifiedMemoryOrchestrator()
D = orch.capture(context="Example", sense="A sufficiently long sense to pass A1/A2.", meta={"novelty_hint": True})
out = orch.run_tmp(D); print("TMP:", out["OUT"]["verdict"])
refs = orch.promote_if_bifurcated(D, out) or orch.user_force_save(D, out, reason="example")
print("Durable:", refs)

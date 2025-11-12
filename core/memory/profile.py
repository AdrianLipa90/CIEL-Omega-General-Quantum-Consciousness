import os
VENDOR = os.environ.get("CIEL_MEM_VENDOR", "").strip().lower()
ORCH_VENDOR   = VENDOR or "repo"
POLICY_VENDOR = VENDOR or "ultimate"
STORE_VENDOR  = VENDOR or "ultimate"

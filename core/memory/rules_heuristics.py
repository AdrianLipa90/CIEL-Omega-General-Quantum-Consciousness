from .profile import POLICY_VENDOR as _V
if _V == "pro":
    from .vendor.pro.rules_heuristics import *  # type: ignore
else:
    from .vendor.ultimate.rules_heuristics import *  # type: ignore

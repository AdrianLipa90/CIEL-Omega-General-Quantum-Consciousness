from .profile import ORCH_VENDOR as _V
if _V == "ultimate":
    from .vendor.ultimate.weighting import *  # type: ignore
else:
    from .vendor.pro.weighting import *  # type: ignore

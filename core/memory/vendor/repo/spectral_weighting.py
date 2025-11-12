from .weighting import spectral_weight, clamp, decision_thresholds
from .policy import Policy

def compute_weight(entry, features, user_subjective=0.0, self_subjective=0.0, policy:Policy=None):
    policy = policy or Policy()
    w, G, M = spectral_weight(entry, features, user_subjective, self_subjective, policy)

    # context-aware tweak: boost by emotion ([-1,1] → [-0.1,+0.2]) and coherence (0..1 → [-0.1,+0.2])
    emo = float(features.get("M",{}).get("emotion", 0.0))
    coh = float(features.get("M",{}).get("coherence", 0.5))
    ctx_conf = float(features.get("M",{}).get("context_conf", 0.5))

    emo_add = 0.2*max(0.0, emo) - 0.1*max(0.0, -emo)
    coh_add = 0.2*coh - 0.1*(1.0 - coh)
    ctx_add = 0.1*ctx_conf - 0.05*(1.0 - ctx_conf)

    w2 = w * (1.0 + emo_add + coh_add + ctx_add)
    return max(0.0, float(w2)), G, M, {"emo_add":emo_add, "coh_add":coh_add, "ctx_add":ctx_add}

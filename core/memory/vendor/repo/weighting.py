from .policy import Policy

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def spectral_weight(entry, features, user_subjective=0.0, self_subjective=0.0, policy:Policy=None):
    policy = policy or Policy()
    spec = policy.spectral_conf()
    base = float(spec.get('base', 1.0))

    user_boost = clamp(policy.float_boost_user(entry.get('data',''), features), spec['cap_low'], spec['cap_high'])
    self_boost = clamp(policy.float_boost_self(entry.get('data',''), features), spec['cap_low'], spec['cap_high'])
    imm_boost = policy.immutable_boost(entry.get('data',''), features)

    # Subjective modifiers in [-1,1]
    user_s = clamp(float(user_subjective), spec['cap_low'], spec['cap_high'])
    self_s = clamp(float(self_subjective), spec['cap_low'], spec['cap_high'])

    # Compute G from tokens + length (normalized)
    tokens = int(features.get('C',{}).get('tokens', 0))
    length = int(features.get('C',{}).get('length', 0))
    gm = spec.get('G_map', {})
    token_norm = tokens/float(gm.get('token_norm_div', 32))
    length_norm = (length/float(gm.get('length_norm_div', 280))) * float(gm.get('length_weight', 0.25))
    G = clamp(token_norm + length_norm - float(gm.get('token_offset', 0.25)), spec['cap_low'], spec['cap_high'])

    # Compute M from immutable baseline + policy floats
    M = (imm_boost - 1.0) + float(spec.get('M_base_from_immutable',0.5)) + user_boost + self_boost
    M = clamp(M, spec['cap_low'], spec['cap_high'])

    spectral_add = spec.get('G_weight',0.6)*G + spec.get('M_weight',0.4)*M + 0.5*user_s + 0.5*self_s
    weight = base * (1.0 + spectral_add)

    if imm_boost > 0:
        weight = max(weight, base*imm_boost)
    return max(0.0, float(weight)), G, M

def decision_thresholds(policy:Policy=None):
    spec = (policy or Policy()).spectral_conf().get('decision', {})
    return float(spec.get('to_mem', 1.65)), float(spec.get('to_out', 0.50))

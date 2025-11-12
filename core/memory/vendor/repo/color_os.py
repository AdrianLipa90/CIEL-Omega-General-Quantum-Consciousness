# Full ColorOS mapping from M in [-1,1] to color category, tag and intensity (0-100)
BANDS = [
    (-1.00, -0.75, ('abyss', 'infra')),
    (-0.75, -0.50, ('deep', 'infra')),
    (-0.50, -0.25, ('damped', 'subdued')),
    (-0.25,  0.00, ('low', 'subdued')),
    ( 0.00,  0.25, ('neutral', 'neutral')),
    ( 0.25,  0.50, ('rise', 'neutral')),
    ( 0.50,  0.75, ('bright', 'bright')),
    ( 0.75,  0.90, ('vivid', 'bright')),
    ( 0.90,  1.00, ('luminous', 'luminous')),
]

def color_tag(m_value: float):
    m = max(-1.0, min(1.0, float(m_value)))
    for lo, hi, (name, tag) in BANDS:
        if m >= lo and m < hi:
            # intensity relative to band window
            span = hi - lo
            rel = (m - lo) / span if span > 0 else 0.5
            intensity = int(round(rel * 100))
            return {'name': name, 'tag': tag, 'intensity': intensity}
    # edge case m==1.0
    return {'name':'luminous','tag':'luminous','intensity':100}

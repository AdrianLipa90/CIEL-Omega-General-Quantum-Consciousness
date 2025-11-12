from typing import Dict, Any

NEGATION_WORDS = {"nie","nigdy","żaden","żadne","brak"}

def semantic_checks(text: str) -> Dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        return {"coherence": 0.4, "negations": 0, "contradiction": False}

    toks = text.lower().split()
    negs = sum(t in NEGATION_WORDS for t in toks)
    # toy contradiction: "X i nie X"
    contradiction = any(toks.count(w)>=1 and ("nie " + w) in text.lower() for w in set(toks))

    # a softer coherence heuristic: more tokens and fewer negations → higher score
    base = 0.3 + min(0.4, 0.02*len(toks))
    penal = min(0.3, 0.05*negs) + (0.25 if contradiction else 0.0)
    coherence = max(0.0, min(1.0, base - penal))

    return {"coherence": float(coherence), "negations": int(negs), "contradiction": bool(contradiction)}

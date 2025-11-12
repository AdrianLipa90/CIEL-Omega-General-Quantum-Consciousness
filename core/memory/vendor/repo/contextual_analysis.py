from typing import Dict, Any

POSITIVE = {"kocham","dziękuję","dobrze","pięknie","świetnie","super","spoko","zajebiście"}
NEGATIVE = {"kurwa","nienawidzę","zjeb","wkurw","ból","trauma","źle","fatalnie","płacz","żal","gniew"}
INTENTS   = {"design","spec","result","kernel","orchestrator","weights","bifurkacja","tmp","mem","review","contract"}

def _tokenize(s: str):
    return [t for t in "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in s.lower()).split() if t]

def infer_context(entry: Dict[str, Any]) -> Dict[str, Any]:
    data = entry.get("data","")
    if not isinstance(data, str):
        return {"topic": "nontext", "intent": "raw", "emotion": 0.0, "confidence": 0.2}

    toks = _tokenize(data)
    if not toks:
        return {"topic": "empty", "intent": "raw", "emotion": 0.0, "confidence": 0.2}

    pos = sum(t in POSITIVE for t in toks)
    neg = sum(t in NEGATIVE for t in toks)
    emo = 0.0
    if pos+neg>0:
        emo = (pos - neg) / (pos + neg)

    # crude topic: first noun-like token
    topic = toks[0]
    intent = next((t for t in toks if t in INTENTS), "note")
    conf = min(1.0, 0.3 + 0.05*len(toks) + 0.2*(1 if intent!="note" else 0))

    return {"topic": topic, "intent": intent, "emotion": float(emo), "confidence": float(conf)}

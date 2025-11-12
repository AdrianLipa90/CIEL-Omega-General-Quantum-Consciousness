import numpy as np
from .contextual_analysis import infer_context
from .semantic_logic import semantic_checks

def analyze_input(d):
    features = {"C":{}, "S":{}, "A":{}, "T":{}, "M":{}}
    if isinstance(d, str):
        tokens = d.strip().split()
        features["C"]["length"] = len(d)
        features["C"]["tokens"] = len(tokens)
        features["S"]["vowels"] = sum(1 for c in d.lower() if c in 'aeiouy')
        features["A"]["has_numbers"] = any(t.isdigit() for t in tokens)
        features["T"]["type"] = "text"
        ctx = infer_context({"data": d})
        sem = semantic_checks(d)
        features["M"]["symbol"] = ctx["topic"]
        features["M"]["intent"] = ctx["intent"]
        features["M"]["emotion"] = ctx["emotion"]
        features["M"]["context_conf"] = ctx["confidence"]
        features["M"]["coherence"] = sem["coherence"]
        features["M"]["negations"] = sem["negations"]
        features["M"]["contradiction"] = sem["contradiction"]
    elif isinstance(d, (list,tuple,np.ndarray)):
        arr = np.array(d, dtype=float)
        features["T"]["type"] = "numeric"
        features["C"]["mean"] = float(np.mean(arr)) if arr.size else 0.0
        features["C"]["std"] = float(np.std(arr)) if arr.size else 0.0
        features["C"]["tokens"] = int(arr.size)
        features["M"]["symbol"] = "numeric"
        features["M"]["intent"] = "measurement"
        features["M"]["emotion"] = 0.0
        features["M"]["context_conf"] = 0.6
        features["M"]["coherence"] = 0.8
        features["M"]["negations"] = 0
        features["M"]["contradiction"] = False
    else:
        features["T"]["type"] = "raw"
        features["M"]["symbol"] = "raw"
        features["M"]["intent"] = "raw"
        features["M"]["emotion"] = 0.0
        features["M"]["context_conf"] = 0.3
        features["M"]["coherence"] = 0.5
        features["M"]["negations"] = 0
        features["M"]["contradiction"] = False
        features["C"]["tokens"] = 0
        features["C"]["length"] = 0
    return features

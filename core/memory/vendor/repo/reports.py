from datetime import datetime
from collections import Counter

def _avg(xs):
    return round(sum(xs)/max(1,len(xs)), 4)

def daily_report(tmp_memory):
    today = datetime.utcnow().date().isoformat()
    weights = [e.get('weight',1.0) for e in tmp_memory]
    intents = [e.get('features',{}).get('M',{}).get('intent','?') for e in tmp_memory]
    syms = [e.get('features',{}).get('M',{}).get('symbol','?') for e in tmp_memory]
    emos = [e.get('features',{}).get('M',{}).get('emotion',0.0) for e in tmp_memory]
    cohs = [e.get('features',{}).get('M',{}).get('coherence',0.0) for e in tmp_memory]

    hist = {"<0.5":0,"0.5-1.0":0,"1.0-1.6":0,">=1.6":0}
    for w in weights:
        if w < 0.5: hist["<0.5"]+=1
        elif w < 1.0: hist["0.5-1.0"]+=1
        elif w < 1.6: hist["1.0-1.6"]+=1
        else: hist[">=1.6"]+=1

    rep = {
        "date": today,
        "total": len(tmp_memory),
        "avg_weight": _avg(weights),
        "avg_emotion": _avg(emos),
        "avg_coherence": _avg(cohs),
        "weight_hist": hist,
        "top_intents": Counter(intents).most_common(5),
        "top_symbols": Counter(syms).most_common(5),
    }
    return rep

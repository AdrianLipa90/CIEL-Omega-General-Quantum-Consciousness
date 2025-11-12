def prefilter(data):
    if data is None: return None
    if isinstance(data,str):
        s=data.strip()
        return s if s else None
    return data

import h5py, numpy as np
from pathlib import Path
from datetime import datetime

class H5Store:
    def __init__(self, root='data/h5'):
        self.root=Path(root); self.root.mkdir(parents=True, exist_ok=True)
    def _path(self, symbol:str)->Path:
        d=self.root/symbol; d.mkdir(parents=True, exist_ok=True)
        day=datetime.utcnow().strftime('%Y%m%d')
        return d / f'{symbol}_{day}.h5'
    def append(self, symbol:str, intent:str, vector):
        path=self._path(symbol)
        v=np.asarray(vector,dtype='float32')
        with h5py.File(path,'a') as f:
            if 'vectors' not in f:
                cols=v.shape[-1] if v.ndim>0 else 1
                f.create_dataset('vectors', shape=(0,cols), maxshape=(None,cols), dtype='float32', chunks=True)
            if 'intents' not in f:
                dt=h5py.special_dtype(vlen=str)
                f.create_dataset('intents', shape=(0,), maxshape=(None,), dtype=dt, chunks=True)
            vs=f['vectors']; its=f['intents']
            new_len=vs.shape[0]+1
            vs.resize((new_len, vs.shape[1])); its.resize((new_len,))
            vs[-1]=v if v.ndim>0 else [v]
            its[-1]=intent
        return str(path)

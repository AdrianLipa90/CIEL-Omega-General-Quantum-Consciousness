import shutil
from pathlib import Path

def rotate_tmp_reports(src='data/tmp_reports', dst='data/archive/tmp_reports'):
    src_p=Path(src); dst_p=Path(dst)
    if not src_p.exists(): return False
    dst_p.mkdir(parents=True, exist_ok=True)
    for p in src_p.glob('*.json'):
        shutil.move(str(p), dst_p / p.name)
    return True

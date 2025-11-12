import json, sys
from pathlib import Path

QDIR = Path('data/verify_queue')
QDIR.mkdir(parents=True, exist_ok=True)

def list_queue():
    items = list(QDIR.glob('verify_*.json'))
    return [str(p) for p in sorted(items)]

def show(item_path):
    p = Path(item_path)
    print(p.read_text(encoding='utf-8'))

def main():
    if len(sys.argv)==1:
        print('\n'.join(list_queue()))
        return
    cmd = sys.argv[1]
    if cmd=='list':
        print('\n'.join(list_queue()))
    elif cmd=='show' and len(sys.argv)>2:
        show(sys.argv[2])
    else:
        print('Usage: python scripts/review_queue.py [list|show <file>]')

if __name__ == '__main__':
    main()

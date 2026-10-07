from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def load_config(path=None):
    return json.loads(Path(path or ROOT/'configs/baseline.json').read_text())

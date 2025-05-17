
import re
from typing import List, Dict

def load_draws(file_path: str) -> List[Dict]:
    """Read cleaned dataset (期號 + 5 號碼) and return list of dicts."""
    records = []
    with open(file_path, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 6:
                continue
            period, *nums = parts
            records.append({'period': period, 'nums': [int(n) for n in nums]})
    records.sort(key=lambda x: int(x['period']))  # ensure chronological
    return records

# ml_filter.py
import math
from pathlib import Path

FILE_TYPES = ['.py', '.json', '.env', '.txt', '.yaml', '.yml']

def calc_entropy(s):
    prob = [float(s.count(c)) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in prob if p > 0)

def extract_features(line, filepath, all_lines, index):
    # Context lines
    before = all_lines[index - 1] if index > 0 else ""
    after = all_lines[index + 1] if index + 1 < len(all_lines) else ""
    context = before + after

    file_ext = Path(filepath).suffix.lower()
    file_type_flags = [1 if ext == file_ext else 0 for ext in FILE_TYPES]

    return [
        len(line),
        calc_entropy(line),
        int(any(keyword in line.lower() for keyword in ["secret", "key", "auth", "token", "pass"])),
        int(line.strip().endswith("=")),
        sum(1 for w in ["secret", "key", "auth"] if w in context.lower()),
        *file_type_flags
    ]
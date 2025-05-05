import pickle, math, random, pathlib
from collections import Counter
from sklearn.ensemble import RandomForestClassifier

# ---------------- Feature helpers ---------------- #
def shannon_entropy(s: str) -> float:
    counts = Counter(s)
    probs  = [c / len(s) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def ends_with_eq(s: str) -> int:
    return int(s.strip().endswith("="))

def has_keyword(s: str) -> int:
    return int(any(k in s.lower() for k in ("key", "token", "secret", "aws")))

def context_hits(ctx: str) -> int:
    ctx = ctx.lower()
    return sum(word in ctx for word in ("aws", "slack", "token", "key"))

# ---------------- Build synthetic dataset -------- #
def make_sample(secret: str, fname: str, label: int):
    ctx = pathlib.Path(fname).suffix  # e.g. ".py"
    ft_flags = [int(ctx == ext) for ext in (".py", ".json", ".yaml", ".cfg", ".env")]
    features = [
        len(secret),
        shannon_entropy(secret),
        has_keyword(secret),
        ends_with_eq(secret),
        context_hits(secret),
        *ft_flags,                   # 5 file‑type one‑hots
        int(sum(ft_flags) == 0),     # "other" file
    ]
    return features, label

X, y = [], []

# 60 positive samples (AWS / Slack)
for _ in range(30):
    X.append(make_sample(f"AKIA{''.join(random.choices('A1B2C3D4E5F6G7H8', k=16))}",
                         "foo.py", 1)[0])
    X.append(make_sample(f"xoxb-123456789012-FAKETOKEN{random.randint(1000000,9999999)}",
                         "bar.json", 1)[0])
    y.extend([1, 1])

# 60 negative samples (noise)
for _ in range(60):
    noise = "".join(random.choices("abcdef123456", k=random.randint(15, 35)))
    X.append(make_sample(noise, "notes.txt", 0)[0])
    y.append(0)

print(f"[+] Dataset: {len(X)} rows  |  Pos={sum(y)} Neg={len(y)-sum(y)}")

clf = RandomForestClassifier(n_estimators=150, random_state=42)
clf.fit(X, y)
with open("ml_model.pkl", "wb") as fh:
    pickle.dump(clf, fh)

print("[✓] Model saved to ml_model.pkl")
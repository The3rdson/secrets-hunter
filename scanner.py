import os, re, argparse, json, math, pickle, pathlib
from collections import Counter, defaultdict
from datetime import datetime

# ---------------- Regex patterns ---------------- #
PATTERNS = {
    "AWS Access Key" : re.compile(r"AKIA[0-9A-Z]{16}"),
    "Slack Token"    : re.compile(r"xox[baprs]-[0-9]{12,}-[A-Za-z0-9\-]{10,}"),
}

# ---------------- Feature helpers (must match train_model.py) -------- #
def shannon_entropy(s: str) -> float:
    cnt = Counter(s)
    return -sum((c/len(s))*math.log2(c/len(s)) for c in cnt.values())

def ends_with_eq(s: str) -> int:
    return int(s.strip().endswith("="))

def has_keyword(s: str) -> int:
    low = s.lower()
    return int(any(k in low for k in ("key", "token", "secret", "aws")))

def context_hits(s: str) -> int:
    low = s.lower()
    return sum(word in low for word in ("aws", "slack", "token", "key"))

def build_feature_vec(secret: str, path: pathlib.Path):
    ft_flags = [int(path.suffix == ext) for ext in (".py", ".json", ".yaml", ".cfg", ".env")]
    other    = int(sum(ft_flags) == 0)
    return [
        len(secret),
        shannon_entropy(secret),
        has_keyword(secret),
        ends_with_eq(secret),
        context_hits(secret),
        *ft_flags,
        other,
    ]

# ---------------- Load ML model (optional) -------- #
try:
    with open("ml_model.pkl", "rb") as fh:
        MODEL = pickle.load(fh)
    THRESH = 0.80
    print("[+] ML model loaded.")
except FileNotFoundError:
    MODEL  = None
    THRESH = 0.0          # everything passes
    print("[!] ml_model.pkl not found — falling back to regex‑only mode.")

# ---------------- Core scan ---------------- #
def scan_file(path: pathlib.Path, findings):
    try:
        with path.open(errors="ignore") as fh:
            for idx, line in enumerate(fh, 1):
                for stype, regex in PATTERNS.items():
                    for m in regex.finditer(line):
                        secret = m.group(0)
                        if MODEL:
                            vec = build_feature_vec(secret, path)
                            proba = MODEL.predict_proba([vec])[0][1]
                            if proba < THRESH:
                                continue  # likely false positive
                        findings.append({
                            "file": str(path),
                            "line": idx,
                            "type": stype,
                            "secret": secret,
                        })
    except Exception as exc:
        print(f"[WARN] {path}: {exc}")

def walk_repo(root: pathlib.Path):
    findings = []
    for p in root.rglob("*"):
        if p.is_file() and not p.match("*.git/*"):
            scan_file(p, findings)
    return findings

# ---------------- CLI ---------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="Path to directory or Git repo")
    ap.add_argument("--report", action="store_true", help="Write scan_report.json")
    args = ap.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    print(f"[+] Scanning {repo} …")

    findings = walk_repo(repo)
    if not findings:
        print("✅  No secrets found.")
    else:
        for f in findings:
            print(f'{f["file"]} [Line {f["line"]}] - {f["type"]}: {f["secret"]}')
        print(f"\n⚠  {len(findings)} secret(s) found.")

    if args.report:
        out = {
            "scanned_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "root": str(repo),
            "findings": findings,
        }
        with open("scan_report.json", "w") as fh:
            json.dump(out, fh, indent=2)
        print("[✓] Results written to scan_report.json")

if __name__ == "__main__":
    main()
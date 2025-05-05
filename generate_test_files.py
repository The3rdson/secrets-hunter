#!/usr/bin/env python3
"""
Generate a realistic corpus of files (20 small + 1 giant) containing
*fake* AWS keys and Slack tokens for functional + performance tests.
"""

import os, random, textwrap, pathlib

OUT_DIR = pathlib.Path("test_files")
OUT_DIR.mkdir(exist_ok=True)

LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Vestibulum pulvinar massa sed justo ultricies, non lacinia ipsum tempor. "
)

def fake_aws_key() -> str:
    suffix = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16))
    return f"aws_access_key_id = \"AKIA{suffix}\""

def fake_slack_token() -> str:
    digits = random.randint(100000000000, 999999999999)  # 12 digits
    tail   = random.randint(100000000,   999999999)
    return f"slack_token: xoxb-{digits}-FAKETOKEN{tail}"

def random_noise_line() -> str:
    return textwrap.shorten(LOREM * random.randint(1, 3), 80)

def make_file(path: pathlib.Path, n_lines: int, inject_secret=True):
    with path.open("w") as f:
        secret_line = fake_aws_key() if random.random() < 0.5 else fake_slack_token()
        spot        = random.randint(0, n_lines - 1) if inject_secret else -1
        for i in range(n_lines):
            if i == spot:
                f.write(secret_line + "\n")
            else:
                f.write(random_noise_line() + "\n")

def main():
    print("[+] Creating small / medium files …")
    exts = [".py", ".json", ".yaml", ".cfg"]
    for idx in range(20):
        ext  = random.choice(exts)
        path = OUT_DIR / f"file_{idx}{ext}"
        make_file(path, n_lines=random.randint(80, 200))

    # One giant file for perf‑test
    print("[+] Creating giant_test_file.py (≈175 k lines) …")
    make_file(OUT_DIR / "giant_test_file.py", n_lines=175_000)

    print("[✓] Done — files (small fries and bigboy meal) in ./test_files")

if __name__ == "__main__":
    main()
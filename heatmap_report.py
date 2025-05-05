# heatmap_report.py
import json
from collections import Counter
import matplotlib.pyplot as plt
from pathlib import Path

def load_report(report_path="scan_report.json"):
    if not Path(report_path).exists():
        print(f"❗ Report not found: {report_path}")
        return []
    with open(report_path, "r") as f:
        return json.load(f)

def plot_secret_counts_by_file(findings):
    file_counts = Counter([f["file"] for f in findings])
    files = list(file_counts.keys())
    counts = list(file_counts.values())

    plt.figure(figsize=(10, 5))
    plt.barh(files, counts)
    plt.title("Secrets Detected per File")
    plt.xlabel("Number of Secrets")
    plt.tight_layout()
    plt.savefig("secrets_by_file.png")
    print("📊 Saved 'secrets_by_file.png'")

def plot_secret_types(findings):
    type_counts = Counter([f["type"] for f in findings])
    labels = list(type_counts.keys())
    sizes = list(type_counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Secret Types Distribution")
    plt.tight_layout()
    plt.savefig("secret_types_pie.png")
    print("📊 Saved 'secret_types_pie.png'")

if __name__ == "__main__":
    findings = load_report()
    if not findings:
        exit(1)

    plot_secret_counts_by_file(findings)
    plot_secret_types(findings)
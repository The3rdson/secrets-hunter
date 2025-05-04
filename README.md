# 🔐 Secrets-in-Code Hunter (with AI Filtering)

A Python-based pre-commit hook that scans for hardcoded secrets (API keys, tokens, private keys) and uses a machine learning model to reduce false positives.

## ✅ Features
- Detects common secrets using regex (AWS keys, Slack tokens, etc.)
- ML classifier filters out false positives based on entropy, length, and context
- Blocks Git commits that contain suspected secrets
- Easily extensible for other file types or patterns

## 📦 Setup

1. Clone the repo
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
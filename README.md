Secrets-in-Code Hunter (with AI Filtering)

This tool helps developers identify and prevent hardcoded secrets (like API keys, tokens, and private keys) from being committed to their codebase. It combines pattern matching with a machine learning model to reduce false positives.

 Features

- Detects common secrets using regular expressions (AWS keys, Slack tokens, etc.)
- Uses a machine learning classifier to reduce false positives based on entropy, length, and context
- Blocks Git commits that contain suspected secrets when used as a pre-commit hook
- Easy to extend for additional file types or secret patterns

 Setup

1. Clone this repository
2. Create and activate a virtual environment:
   python3 -m venv venv

   source venv/bin/activate
  
3. Install dependencies:
   pip install -r requirements.txt
   ```

 Testing Instructions

To test the scanner, create a folder named `test_files/` in the project root, and add the following example files:

- `test_files/app.py`
  ```python
  aws_key = "AKIAEXAMPLEKEY1234567890"
  token = "xoxb-123456789012-FAKETOKEN987654321"
  ```

- `test_files/config.yaml`
  ```yaml
  api_key: AKIAFAKEKEY1234567890
  ```

- `test_files/settings.cfg`
  ```ini
  api_key = AKIAFAKEKEY0987654321
  ```

Then run the scanner using:

python scanner.py --repo ./test_files --report

This will generate a `scan_report.json` file showing any detected secrets.

To visualize the results, you can also run:

python heatmap_report.py
```

This will create heatmap and pie chart images showing secret distribution across files and types.

**Note**: The `test_files/` folder is excluded from GitHub using `.gitignore` to prevent accidental upload of dummy secrets.
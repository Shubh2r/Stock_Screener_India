name: 📈 Run Stock Screener

on:
  workflow_dispatch:
  schedule:
    - cron: '30 4 * * 1'  # Every Monday 10AM IST

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run screener
        run: python main.py

      - name: Commit results
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add results/*.md
          git commit -m "📊 Screener results - $(date)"
          git push

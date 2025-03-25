# 🌍 Verra Registry Tracker

Automatically track changes to the [Verra Registry](https://registry.verra.org/app/search/VCS) project database! This tool helps monitor carbon credit projects and their updates.

## 🎯 What it does

- 📥 Downloads the complete Verra Registry dataset weekly
- 🔍 Detects changes between snapshots
- 📊 Archives historical data
- 📝 Posts updates to GitHub Issues
- 📈 Maintains a clean "latest" view

## 🤖 How it works

Every Wednesday at 9am UTC, this bot:
1. Visits the Verra Registry website
2. Downloads the complete project database
3. Compares it with the previous version
4. Archives the snapshot
5. Reports any changes to GitHub Issues

## 📁 Code Structure

```
verra_tracker/
├── data/
│   ├── archive/               # Historical CSVs (1 per week)
│   │   └── verra_2025-03-25.csv
│   └── latest.csv            # Most recent snapshot
├── logs/
│   ├── archive/              # Historical logs
│   │   └── verra_2025-03-25.log
│   └── latest.log           # Most recent run log
├── verra/
│   ├── downloader.py        # Headless browser automation 🌐
│   ├── differ.py           # Smart diff detection 🔄
│   ├── cleaner.py         # Data cleaning utilities 🧹
│   └── config.py          # Settings & paths ⚙️
├── scripts/
│   └── run_pipeline.py    # Main entry point 🚀
```

## 📊 Data Storage

- Each weekly snapshot: ~2MB
- 1 year of history: ~104MB
- 5 years of history: ~500MB

## 🔍 What We Track

The dataset includes key information about carbon projects:
- Project IDs and Names
- Proponents
- Methodologies
- Locations
- Emission Reduction Estimates
- Registration Dates
- Crediting Periods

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies: `uv sync`
3. Run manually: `uv run scripts/run_pipeline.py`
4. Check the logs in `logs/latest.log`

## 🤝 Contributing

Contributions welcome! Feel free to:
- 🐛 Report bugs
- ✨ Request features
- 🔧 Submit PRs

## 📝 License

MIT License
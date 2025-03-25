1 file/week × 52 weeks/year = ~104MB/year
5 years of history = ~500MB

```
verra_tracker/
├── data/
│   ├── archive/               # All timestamped historic CSVs
│   │   └── verra_2025-03-25.csv
│   └── latest.csv             # Always the most recent snapshot
├── verra/
│   ├── __init__.py
│   ├── downloader.py          # Handles headless scraping/download
│   ├── differ.py              # Compares CSVs, finds diffs
│   └── config.py              # Paths, constants, settings
├── scripts/
│   └── run_pipeline.py        # Entry point: download → diff → save
├── requirements.txt
└── README.md
```
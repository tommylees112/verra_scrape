from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ARCHIVE_DIR = DATA_DIR / "archive"
LOG_DIR = BASE_DIR / "logs"
LATEST_PATH = DATA_DIR / "latest.csv"
TODAY_PATH = ARCHIVE_DIR / f"verra_{date.today().isoformat()}.csv"
TODAY_LOG_PATH = LOG_DIR / f"verra_{date.today().isoformat()}.log"
LATEST_LOG_PATH = LOG_DIR / "latest_log.txt"

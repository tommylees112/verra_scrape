import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from loguru import logger

from verra.config import LATEST_PATH
from verra.differ import detect_changes
from verra.downloader import download_csv


def main():
    logger.info("📥 Downloading latest data...")
    new_df = download_csv()

    logger.info("🔍 Checking for changes...")
    diffs = detect_changes(new_df)

    if not diffs["new"].empty:
        logger.info(f"🆕 {len(diffs['new'])} new rows found.")

    if not diffs["removed"].empty:
        logger.info(f"❌ {len(diffs['removed'])} removed rows found.")

    new_df.to_csv(LATEST_PATH, index=False)
    logger.success("✅ Updated latest view.")


if __name__ == "__main__":
    main()

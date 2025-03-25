import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from loguru import logger

from verra.config import LATEST_LOG_PATH, LATEST_PATH, TODAY_LOG_PATH
from verra.differ import detect_changes
from verra.downloader import download_csv

# Configure loguru at the start
logger.add(TODAY_LOG_PATH, rotation="1 day", mode="w")

# overwrite the latest log file
logger.add(LATEST_LOG_PATH, rotation="1 day", mode="w")


def main():
    logger.info("\n\n📥 Downloading latest data...")
    new_df = download_csv()

    logger.info("\n\n🔍 Checking for changes...")
    diffs = detect_changes(new_df)

    if not diffs["new"].empty:
        logger.info(f"\n🆕 {len(diffs['new'])} new rows found.")

    if not diffs["removed"].empty:
        logger.info(f"\n❌ {len(diffs['removed'])} removed rows found.")

    new_df.to_csv(LATEST_PATH, index=False)
    logger.success("✅ Updated latest view.")


if __name__ == "__main__":
    main()

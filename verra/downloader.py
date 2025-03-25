from typing import Optional

import pandas as pd
from loguru import logger
from playwright.sync_api import sync_playwright

from verra.config import TODAY_PATH


def download_csv(return_df: bool = False) -> Optional[pd.DataFrame]:
    """Download CSV data from Verra Registry project search (synchronous version)."""
    url = "https://registry.verra.org/app/search/VCS/All%20Projects"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto(url)

        # Click the "Search" button
        page.click('button:has-text("Search")')

        # Wait for the first row of the results table to appear
        page.wait_for_selector("tr[kendogridlogicalrow]", timeout=15000)
        logger.info("Table loaded.")

        # Wait for table to load multiple rows
        logger.info("Waiting for table data to load...")
        page.wait_for_selector("td[kendogridcell] span", state="visible")

        # Check for multiple rows
        rows = page.locator("td[kendogridcell] span").count()
        logger.info(f"Found {rows} rows in the table")

        if rows <= 1:
            logger.warning("Table doesn't have enough data yet, waiting longer...")
            page.wait_for_timeout(5000)  # wait 5 more seconds
            rows = page.locator("td[kendogridcell] span").count()
            logger.info(f"After waiting, found {rows} rows in the table")

        if rows > 1:
            logger.info("Table is populated, proceeding with download...")
            with page.expect_download() as download_info:
                logger.info("Attempting to click download button...")
                page.click('button[title="Download CSV"]')

                download = download_info.value
                save_location = TODAY_PATH
                logger.info(f"Download started! Saving to: {save_location}")
                download.save_as(save_location)
        else:
            raise Exception("Table failed to load with sufficient data in time")

        logger.info(f"Downloaded file saved at: {save_location}")
        browser.close()

    try:
        df = pd.read_csv(TODAY_PATH)
        return df
    except Exception as e:
        logger.error(f"Failed to read downloaded CSV: {e}")
        return pd.DataFrame()  # Return empty DataFrame instead of None


if __name__ == "__main__":
    download_csv()

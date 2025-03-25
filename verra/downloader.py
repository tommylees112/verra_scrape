import asyncio
import sys
from pathlib import Path

from loguru import logger
from playwright.async_api import async_playwright

sys.path.append(str(Path(__file__).resolve().parent.parent))
from verra.config import TODAY_PATH


async def download_csv():
    """Download CSV data from Verra Registry project search.

    This function automates the process of downloading project data from the Verra Registry:
    1. Navigates to the Verra Registry project search page
    2. Triggers the search by clicking the 'Search' button
        `<button _ngcontent-jbu-c9="" class="btn btn-primary" type="submit">Search</button>`
    3. Waits for the results table to populate with data
        `tr[kendogridlogicalrow]`
    4. Downloads the results as a CSV file to the user's Downloads directory
        `<button _ngcontent-jbu-c14="" class="download text-light" title="Download CSV" type="button"><i _ngcontent-jbu-c14="" class="fas fa-file-csv fa-lg pr-2"></i></button>`

    The function includes checks to ensure the table is properly loaded with multiple rows
    before attempting the download.

    Returns:
        None

    Raises:
        Exception: If the table fails to load with sufficient data
        TimeoutError: If elements don't appear within specified timeouts
    """

    url = "https://registry.verra.org/app/search/VCS/All%20Projects"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        await page.goto(url)

        # Click the "Search" button
        await page.click('button:has-text("Search")')

        # Wait for the first row of the results table to appear
        await page.wait_for_selector("tr[kendogridlogicalrow]", timeout=15000)
        logger.info("Table loaded.")

        # Wait for table to load multiple rows
        logger.info("Waiting for table data to load...")
        await page.wait_for_selector("td[kendogridcell] span", state="visible")

        # Check for multiple rows
        rows = await page.locator("td[kendogridcell] span").count()
        logger.info(f"Found {rows} rows in the table")

        if rows <= 1:
            logger.warning("Table doesn't have enough data yet, waiting longer...")
            # Wait a bit more and check again, or you could add a retry mechanism
            await page.wait_for_timeout(5000)  # wait 5 more seconds
            rows = await page.locator("td[kendogridcell] span").count()
            logger.info(f"After waiting, found {rows} rows in the table")

        if rows > 1:
            logger.info("Table is populated, proceeding with download...")
            async with page.expect_download() as download_info:
                logger.info("Attempting to click download button...")

                # click the button!
                await page.click('button[title="Download CSV"]')

                logger.info("Waiting for download to start...")
                download = await download_info.value
                logger.info(
                    f"Download started! Saving to: {download.suggested_filename}"
                )

                # Specify custom save path using pathlib
                save_location = TODAY_PATH

                logger.info(f"Saving download to: {save_location}")
                await download.save_as(save_location)
        else:
            raise Exception("Table failed to load with sufficient data")

        logger.info(f"Downloaded file saved at: {save_location}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(download_csv())

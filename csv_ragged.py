import csv

import pandas as pd
from loguru import logger


def process_csv(filename):
    # Read the file first to determine the expected number of columns
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)  # Get the header row
        expected_columns = len(header)

        clean_rows = [header]  # Initialize with header
        ragged_rows = []

        # Process each row
        for row in csv_reader:
            if len(row) > expected_columns:  # Ragged row (too many columns)
                ragged_rows.append(row)
            elif len(row) == expected_columns:  # Clean row
                clean_rows.append(row)

    return clean_rows, ragged_rows


if __name__ == "__main__":
    # Use the function
    clean_rows, ragged_rows = process_csv("allprojects.csv")

    # Convert to pandas DataFrames for easier viewing (optional)
    clean_df = pd.DataFrame(clean_rows[1:], columns=clean_rows[0])
    ragged_df = pd.DataFrame(ragged_rows)

    # Print some information
    logger.info(f"Number of clean rows: {len(clean_rows) - 1}")  # Subtract 1 for header
    logger.info(f"Number of ragged rows: {len(ragged_rows)}")

    # Optional: View the first few rows of each
    logger.info("\nFirst few clean rows:")
    logger.info(clean_df.head())
    logger.info("\nFirst few ragged rows:")
    logger.info(ragged_df.head())

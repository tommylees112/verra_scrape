from pathlib import Path

import pandas as pd
from loguru import logger

from verra.utils import detailed_column_summary


def clean_csv(path: Path) -> pd.DataFrame:
    # fix ragged rows
    df = pd.read_csv(path)

    # Convert date columns to datetime
    date_columns = [col for col in df.columns if "Date" in col]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        logger.info(f"Converted {col} to datetime")

    # Convert Estimated Annual Emission Reductions to integer
    # Remove commas from numbers (1000 separator) before converting to int
    df["Estimated Annual Emission Reductions"] = (
        df["Estimated Annual Emission Reductions"]
        .astype(str)
        .str.replace(",", "")
        .fillna(0)
        .astype(int)
    )
    logger.info("Converted Estimated Annual Emission Reductions to integer")

    annual_reductions = df["Estimated Annual Emission Reductions"].sum()
    logger.info(f"Total estimated annual emission reductions: {annual_reductions:,.0f}")

    summary = detailed_column_summary(df)
    logger.info(f"Column summary:\n{summary}")

    # Find specific row matching criteria and display as JSON
    target_row = df[
        (df["Methodology"] == "VM0007")
        & (df["Crediting Period Start Date"] == "2009-01-01")
        & (df["Crediting Period End Date"] == "2046-12-31")
    ].copy()

    if not target_row.empty:
        logger.info("Found matching row:")
        # Format datetime objects as strings before JSON serialization
        for col in date_columns:
            target_row[col] = target_row[col].dt.strftime("%Y-%m-%d")
        logger.info(target_row.to_json(orient="records", indent=2))
    else:
        logger.warning("No matching row found with the specified criteria")

    return df


if __name__ == "__main__":
    path = Path("data/latest.csv")
    df = clean_csv(path)

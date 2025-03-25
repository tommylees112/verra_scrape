from pathlib import Path

import pandas as pd
from loguru import logger


def detailed_column_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = []
    for ix, col in enumerate(df.columns):
        unique_vals = df[col].unique()
        summary.append(
            {
                "column_index": ix,
                "column": col,
                "dtype": df[col].dtype,
                "n_unique": len(unique_vals),
                "n_null": df[col].isna().sum(),
                "memory_usage": df[col].memory_usage(deep=True) / 1024,  # KB
                "example_values": unique_vals[:5],
            }
        )

    summary_df = pd.DataFrame(summary)
    summary_df = summary_df.set_index(summary_df.columns[0])

    # Format memory usage
    summary_df["memory_usage"] = summary_df["memory_usage"].round(2).astype(str) + " KB"

    return summary_df


if __name__ == "__main__":
    path = Path("allprojects.csv")

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

    # save output
    df.to_csv(
        "cleaned.csv", index=False, encoding="utf-8", lineterminator="\n", quoting=1
    )
    logger.success("Saved cleaned data to cleaned.csv")

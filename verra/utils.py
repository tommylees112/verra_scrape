import pandas as pd


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

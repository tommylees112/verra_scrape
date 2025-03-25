from typing import Dict, List, Set, Union

import pandas as pd
from deepdiff import DeepDiff

from verra.config import LATEST_PATH


def get_deep_diffs(
    old_df: pd.DataFrame, new_df: pd.DataFrame, key: str = "Project ID"
) -> List[Dict]:
    diffs: List[Dict] = []
    common_keys: Set[str] = set(old_df[key]) & set(new_df[key])

    for k in common_keys:
        old_row = old_df[old_df[key] == k].to_dict(orient="records")[0]
        new_row = new_df[new_df[key] == k].to_dict(orient="records")[0]

        diff = DeepDiff(old_row, new_row, ignore_order=True)
        if diff:
            diffs.append({"Project ID": k, "diff": diff.to_dict()})

    return diffs


def flatten_deepdiff(diffs: List[Dict]) -> pd.DataFrame:
    records: List[Dict[str, Union[str, any]]] = []
    for item in diffs:
        pid = item["Project ID"]
        changes = item["diff"].get("values_changed", {})
        for path, change in changes.items():
            field = path.split("root['")[1].split("']")[0]
            records.append(
                {
                    "Project ID": pid,
                    "Field": field,
                    "Old Value": change["old_value"],
                    "New Value": change["new_value"],
                }
            )
    return pd.DataFrame(records)


def detect_changes(new_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    try:
        old_df = pd.read_csv(LATEST_PATH)
    except FileNotFoundError:
        return {
            "new": new_df,
            "changed": pd.DataFrame(),
            "removed": pd.DataFrame(),
        }

    df_merged = new_df.merge(old_df, how="outer", indicator=True)
    new_rows = df_merged[df_merged["_merge"] == "left_only"].drop(columns=["_merge"])
    removed_rows = df_merged[df_merged["_merge"] == "right_only"].drop(
        columns=["_merge"]
    )

    return {
        "new": new_rows,
        "removed": removed_rows,
        "changed": flatten_deepdiff(get_deep_diffs(old_df, new_df)),
    }

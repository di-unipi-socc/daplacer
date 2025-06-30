import json
from pathlib import Path

import pandas as pd
from eclypse.utils.constants import DEFAULT_SIM_PATH


def merge_ray_tune_results(root_dir: str, prefix: str = "daplacer_"):
    """
    Merges results from multiple Ray Tune grid search runs into a single DataFrame.

    Args:
        root_dir (str): Root directory containing subdirectories with Ray Tune results.
        output_file (str): Path to save the merged Parquet file.
    """
    root_path = Path(root_dir)
    experiment_dirs = [
        subdir
        for subdir in root_path.iterdir()
        if subdir.is_dir()  # and subdir.name.startswith(prefix)
    ]
    # print(experiment_dirs)

    all_data = []
    tot_processed = 0
    tot_skipped = 0
    total = len(experiment_dirs)
    for exp_dir in experiment_dirs:
        print("Processing experiment:", exp_dir, end="\n")

        app_csv_path = exp_dir / "output/csv/application.csv"
        params_path = exp_dir / "params.json"

        if not app_csv_path.exists():
            print(f"Skipping {exp_dir}: application.csv not found")
            tot_skipped += 1
            continue  # Skip if application.csv is missing (experiment not ended)

        df = pd.read_csv(app_csv_path)

        if params_path.exists():
            with open(params_path, "r", encoding="utf-8") as f:
                params = dict(json.load(f))
                for key, value in params.items():
                    df[key] = value

        all_data.append(df)
        tot_processed += 1
        print(
            f"Processed {tot_processed}/{total}",
            end=("\r" if tot_processed < total else "\n"),
            flush=True,
        )

    print(f"Processed: {tot_processed}, Skipped: {tot_skipped}")
    df = pd.concat(all_data, ignore_index=True)
    return df


def clean_and_dump(df: pd.DataFrame, output_file: str = "merged_results.parquet"):

    # Cast values to correct dtypes
    bool_columns = ["relaxed"]
    for col in bool_columns:
        df[col] = df[col].astype(bool)

    df.to_parquet(output_file, index=False)
    print(f"Successfully saved merged results to {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Merge Ray Tune results into a single Parquet file."
    )
    parser.add_argument(
        "--root_dir",
        type=str,
        default=DEFAULT_SIM_PATH,
        help="Root directory containing experiment subdirectories.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results.parquet",
        help="Output Parquet file path.",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="edgewise_",
        help="Prefix for experiment directories.",
    )

    args = parser.parse_args()

    df = merge_ray_tune_results(args.root_dir, args.prefix)
    if not df.empty:
        clean_and_dump(df, args.output)
    else:
        print(f"No results found in {args.root_dir}")

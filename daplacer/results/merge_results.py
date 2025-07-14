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

    all_app_data = []
    all_sim_data = []
    tot_processed = 0
    tot_skipped = 0
    total = len(experiment_dirs)
    for exp_dir in experiment_dirs:
        print("Processing experiment:", exp_dir, end="\n")

        output_dirs = [
            d for d in exp_dir.iterdir() if d.is_dir() and d.name.startswith("output")
        ]

        most_recent_output = max(output_dirs, key=lambda d: d.stat().st_mtime)

        if not output_dirs:
            print(f"  ❌ Nessuna cartella 'output*' trovata in: {exp_dir}")
            tot_skipped += 1
            continue

        app_csv_path = most_recent_output / "csv" / "application.csv"
        sim_csv_path = most_recent_output / "csv" / "simulation.csv"
        params_path = exp_dir / "params.json"

        if not app_csv_path.exists() or not sim_csv_path.exists():
            print(f"Skipping {exp_dir}: application.csv or simulation.csv not found")
            tot_skipped += 1
            continue  # Skip if csv files are missing (experiment not ended)
        try:
            df_app = pd.read_csv(app_csv_path)
        except pd.errors.EmptyDataError:
            print(f"Skipping {exp_dir}: Application CSV is empty")
            tot_skipped += 1
            continue

        try:
            df_sim = pd.read_csv(sim_csv_path)
        except pd.errors.EmptyDataError:
            print(f"Skipping {exp_dir}: Simulation CSV is empty")
            tot_skipped += 1
            continue

        if params_path.exists():
            with open(params_path, "r", encoding="utf-8") as f:
                params = dict(json.load(f))
                for key, value in params.items():
                    df_app[key] = value
                    df_sim[key] = value

        all_app_data.append(df_app)
        all_sim_data.append(df_sim)
        tot_processed += 1
        print(
            f"Processed {tot_processed}/{total}",
            end=("\r" if tot_processed < total else "\n"),
            flush=True,
        )

    print(f"Processed: {tot_processed}, Skipped: {tot_skipped}")
    df_app = pd.concat(all_app_data, ignore_index=True)
    df_sim = pd.concat(all_sim_data, ignore_index=True)
    return df_app, df_sim


def clean_and_dump(df_app: pd.DataFrame, df_sim: pd.DataFrame):

    # Cast values to correct dtypes
    bool_columns = ["relaxed"]
    for col in bool_columns:
        df_app[col] = df_app[col].astype(bool)

    df_app.rename(columns={"change_prob": "variation rate"}, inplace=True)
    df_app = df_app.astype(
        {col: str for col in df_app.select_dtypes(include="object").columns}
    )
    df_app.to_parquet("app_results.parquet", index=False)
    print(f"Application results saved to app_results.parquet")

    df_sim.rename(columns={"change_prob": "variation rate"}, inplace=True)
    df_sim.to_parquet("sim_results.parquet", index=False)
    print(f"Simulation results saved to sim_results.parquet")


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
        "-p",
        "--prefix",
        type=str,
        default="daplacer_",
        help="Prefix for experiment directories.",
    )

    args = parser.parse_args()

    df_app, df_sim = merge_ray_tune_results(args.root_dir, args.prefix)
    if not df_app.empty and not df_sim.empty:
        clean_and_dump(df_app, df_sim)
    else:
        print(f"No results found in {args.root_dir}")

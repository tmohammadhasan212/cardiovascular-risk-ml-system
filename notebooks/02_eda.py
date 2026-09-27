"""Stage 2: Exploratory Data Analysis (EDA).

Analyzes distributions, class balance, and correlation matrices.
"""

import pandas as pd
from src.data.loading import load_raw_dataset

def main():
    print("=" * 60)
    print("STAGE 2: EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 60)

    df = load_raw_dataset()

    print("\nTarget Class Distribution:")
    counts = df["target"].value_counts()
    percentages = df["target"].value_counts(normalize=True) * 100
    for cls in [0, 1]:
        print(f" Class {cls}: {counts[cls]} cases ({percentages[cls]:.2f}%)")

    print("\nDescriptive Summary of Continuous Features:")
    continuous_features = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    print(df[continuous_features].describe().round(2))

    print("\nBivariate Analysis (Mean values grouped by Target):")
    print(df.groupby("target")[continuous_features].mean().round(2))

    print("\nPearson Correlation with Target:")
    corr = df.corr()["target"].sort_values(ascending=False)
    print(corr.round(3))

if __name__ == "__main__":
    main()

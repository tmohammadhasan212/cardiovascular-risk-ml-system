"""Stage 1: Data Understanding & Acquisition.

Loads the raw dataset, documents attributes, data types, and validates integrity.
"""

from src.data.loading import load_raw_dataset, validate_dataset

def main():
    print("=" * 60)
    print("STAGE 1: DATA UNDERSTANDING & VALIDATION")
    print("=" * 60)

    df = load_raw_dataset()
    print(f"\nDataset Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nAttribute Types:")
    print(df.dtypes)

    validation = validate_dataset(df)
    print("\nData Validation Summary:")
    for k, v in validation.items():
        print(f" - {k}: {v}")

    print("\nFirst 5 Sample Records:")
    print(df.head())

if __name__ == "__main__":
    main()

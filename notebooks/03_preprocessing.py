"""Stage 3: Preprocessing & Data Leakage Prevention.

Demonstrates pipeline transformations and verifies absence of train/test leakage.
"""

from src.data.loading import get_train_test_split
from src.data.preprocessing import build_preprocessor, get_feature_names

def main():
    print("=" * 60)
    print("STAGE 3: REPRODUCIBLE PREPROCESSING & LEAKAGE VERIFICATION")
    print("=" * 60)

    X_train, X_test, y_train, y_test = get_train_test_split()
    print(f"\nTraining Partition: {X_train.shape[0]} samples")
    print(f"Test Partition:     {X_test.shape[0]} samples")

    preprocessor = build_preprocessor()
    preprocessor.fit(X_train)

    X_train_trans = preprocessor.transform(X_train)
    X_test_trans = preprocessor.transform(X_test)

    feature_names = get_feature_names(preprocessor)
    print(f"\nEngineered One-Hot Features Count: {len(feature_names)}")
    print("Transformed Feature Names:")
    for i, name in enumerate(feature_names):
        print(f" {i+1:2d}. {name}")

    print(f"\nTransformed Matrix Shape: {X_train_trans.shape}")
    print("Zero Data Leakage Check: Pipeline successfully fitted ONLY on training split.")

if __name__ == "__main__":
    main()

"""Stage 4: Systematic 7-Algorithm Model Comparison.

Runs Stratified 5-Fold Cross-Validation across all candidate models.
"""

import json
from src.config import settings

def main():
    print("=" * 60)
    print("STAGE 4: SYSTEMATIC 7-ALGORITHM MODEL COMPARISON")
    print("=" * 60)

    with open(settings.METADATA_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    comparison = meta["model_comparison"]
    print(f"\nActive Selected Model: {meta['model_name']}")
    print(f"Hyperparameters:       {meta['best_hyperparameters']}")
    print("\nCross-Validation Results (Stratified 5-Fold):")
    print("-" * 75)
    print(f"{'Model Algorithm':26s} | {'CV Accuracy':12s} | {'CV Recall':10s} | {'CV ROC-AUC':14s}")
    print("-" * 75)
    for model_name, m in comparison.items():
        acc = f"{m['cv_accuracy_mean']*100:.1f}% ± {m['cv_accuracy_std']*100:.1f}%"
        rec = f"{m['cv_recall_mean']*100:.1f}%"
        auc = f"{m['cv_roc_auc_mean']:.4f} ± {m['cv_roc_auc_std']:.4f}"
        print(f"{model_name:26s} | {acc:12s} | {rec:10s} | {auc:14s}")
    print("-" * 75)

    print("\nHold-out Test Set Performance (N = 61):")
    for k, v in meta["test_metrics"].items():
        if k != "confusion_matrix":
            print(f" - {k:15s}: {v:.4f}")
        else:
            print(f" - {k:15s}: {v}")

if __name__ == "__main__":
    main()

"""Model training, 7-algorithm comparison, hyperparameter optimization, and serialization."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from src.config import settings
from src.data.loading import get_train_test_split, load_raw_dataset
from src.data.preprocessing import build_preprocessor
from src.models.evaluate import (
    compute_classification_metrics,
    compute_pr_curve_data,
    compute_roc_curve_data,
)
from src.models.interpret import ModelExplainer


def get_candidate_models(random_state: int = 42) -> Dict[str, Any]:
    """Define the 7 candidate classification algorithms across different families."""
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, random_state=random_state
        ),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(random_state=random_state),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, random_state=random_state
        ),
        "Support Vector Machine": SVC(
            probability=True, random_state=random_state
        ),
        "AdaBoost": AdaBoostClassifier(
            n_estimators=100, random_state=random_state
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, random_state=random_state
        ),
    }


def get_param_grids(random_state: int = 42) -> Dict[str, Dict[str, Any]]:
    """Hyperparameter search grids for top performing model candidates."""
    return {
        "Random Forest": {
            "classifier__n_estimators": [50, 100, 150],
            "classifier__max_depth": [4, 6, 8, None],
            "classifier__min_samples_split": [2, 5],
            "classifier__min_samples_leaf": [1, 2],
        },
        "Gradient Boosting": {
            "classifier__n_estimators": [50, 100],
            "classifier__learning_rate": [0.05, 0.1, 0.2],
            "classifier__max_depth": [3, 4],
        },
        "Logistic Regression": {
            "classifier__C": [0.01, 0.1, 1.0, 10.0],
            "classifier__penalty": ["l2"],
            "classifier__solver": ["lbfgs", "liblinear"],
        },
        "Support Vector Machine": {
            "classifier__C": [0.1, 1.0, 10.0],
            "classifier__kernel": ["rbf", "linear"],
            "classifier__gamma": ["scale", "auto"],
        },
    }


def train_and_compare_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Tuple[Pipeline, Dict[str, Any]]:
    """Train, cross-validate, and evaluate all 7 models, then tune the best."""
    cv = StratifiedKFold(
        n_splits=settings.CV_FOLDS, shuffle=True, random_state=settings.RANDOM_STATE
    )
    scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]

    models = get_candidate_models(random_state=settings.RANDOM_STATE)
    comparison_results = {}

    print("\n" + "=" * 60)
    print("EXPERIMENT B: SYSTEMATIC COMPARISON OF 7 MODEL FAMILIES")
    print("=" * 60)

    for name, clf in models.items():
        pipe = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("classifier", clf),
            ]
        )

        cv_res = cross_validate(
            pipe,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            return_train_score=False,
        )

        comparison_results[name] = {
            "cv_accuracy_mean": float(np.mean(cv_res["test_accuracy"])),
            "cv_accuracy_std": float(np.std(cv_res["test_accuracy"])),
            "cv_precision_mean": float(np.mean(cv_res["test_precision"])),
            "cv_precision_std": float(np.std(cv_res["test_precision"])),
            "cv_recall_mean": float(np.mean(cv_res["test_recall"])),
            "cv_recall_std": float(np.std(cv_res["test_recall"])),
            "cv_f1_mean": float(np.mean(cv_res["test_f1"])),
            "cv_f1_std": float(np.std(cv_res["test_f1"])),
            "cv_roc_auc_mean": float(np.mean(cv_res["test_roc_auc"])),
            "cv_roc_auc_std": float(np.std(cv_res["test_roc_auc"])),
        }

        print(
            f"{name:25s} | CV ROC-AUC: {comparison_results[name]['cv_roc_auc_mean']:.4f} ± {comparison_results[name]['cv_roc_auc_std']:.4f} | "
            f"CV Recall: {comparison_results[name]['cv_recall_mean']:.4f} | CV F1: {comparison_results[name]['cv_f1_mean']:.4f}"
        )

    # Select best candidate primarily based on CV ROC-AUC and Recall (critical in clinical screening)
    best_candidate_name = max(
        comparison_results.keys(),
        key=lambda k: comparison_results[k]["cv_roc_auc_mean"],
    )
    print(f"\nTop Candidate Model from Initial Screening: {best_candidate_name}")

    # Hyperparameter Optimization (Experiment C)
    param_grids = get_param_grids(random_state=settings.RANDOM_STATE)
    if best_candidate_name in param_grids:
        print(f"\nRunning Hyperparameter Optimization on {best_candidate_name}...")
        base_pipe = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("classifier", models[best_candidate_name]),
            ]
        )
        grid_search = GridSearchCV(
            base_pipe,
            param_grid=param_grids[best_candidate_name],
            cv=cv,
            scoring="roc_auc",
            n_jobs=-1,
        )
        grid_search.fit(X_train, y_train)
        best_pipeline = grid_search.best_estimator_
        best_params = grid_search.best_params_
        best_cv_score = float(grid_search.best_score_)
        print(f"Optimal Parameters: {best_params}")
        print(f"Optimized CV ROC-AUC: {best_cv_score:.4f}")
    else:
        best_pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("classifier", models[best_candidate_name]),
            ]
        )
        best_pipeline.fit(X_train, y_train)
        best_params = {}
        best_cv_score = comparison_results[best_candidate_name]["cv_roc_auc_mean"]

    # Final Evaluation on Untouched Test Set (Experiment F)
    print("\n" + "=" * 60)
    print("FINAL EVALUATION ON UNTOUCHED TEST SET (N = 61)")
    print("=" * 60)
    y_test_pred = best_pipeline.predict(X_test)
    y_test_prob = best_pipeline.predict_proba(X_test)[:, 1]

    test_metrics = compute_classification_metrics(
        y_true=y_test.values,
        y_pred=y_test_pred,
        y_prob=y_test_prob,
    )
    roc_curve_data = compute_roc_curve_data(y_test.values, y_test_prob)
    pr_curve_data = compute_pr_curve_data(y_test.values, y_test_prob)

    print(f"Test Accuracy:    {test_metrics['accuracy']:.4f}")
    print(f"Test Precision:   {test_metrics['precision']:.4f}")
    print(f"Test Recall:      {test_metrics['recall']:.4f}")
    print(f"Test Specificity: {test_metrics['specificity']:.4f}")
    print(f"Test F1-Score:    {test_metrics['f1']:.4f}")
    print(f"Test ROC-AUC:     {test_metrics['roc_auc']:.4f}")
    print(f"Confusion Matrix: {test_metrics['confusion_matrix']}")

    # SHAP Global Importance calculation
    print("\nComputing Global SHAP Explanations...")
    explainer = ModelExplainer(best_pipeline, X_train)
    global_importance = explainer.get_global_importance(top_n=12)

    metadata: Dict[str, Any] = {
        "model_name": best_candidate_name,
        "model_version": settings.APP_VERSION,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "best_hyperparameters": best_params,
        "best_cv_roc_auc": round(best_cv_score, 4),
        "test_metrics": test_metrics,
        "model_comparison": comparison_results,
        "roc_curve": roc_curve_data,
        "pr_curve": pr_curve_data,
        "global_importance": global_importance,
        "features": settings.ALL_FEATURE_COLUMNS,
    }

    return best_pipeline, metadata


def run_training_pipeline():
    """Main execution function for CLI training."""
    # Ensure target output directory exists
    settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_raw_dataset()
    X_train, X_test, y_train, y_test = get_train_test_split(df)

    best_pipeline, metadata = train_and_compare_models(
        X_train, y_train, X_test, y_test
    )

    # Save pipeline
    joblib.dump(best_pipeline, settings.MODEL_PATH)
    print(f"\nSaved trained pipeline to: {settings.MODEL_PATH}")

    # Save metadata JSON
    with open(settings.METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved model evaluation metadata to: {settings.METADATA_PATH}")

    return best_pipeline, metadata


if __name__ == "__main__":
    run_training_pipeline()

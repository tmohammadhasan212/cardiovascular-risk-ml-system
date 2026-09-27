"""Stage 5: Model Interpretability & Explainable AI (XAI).

Calculates SHAP global feature importances and demonstrates local patient attribution.
"""

from src.models.predict import get_prediction_engine

def main():
    print("=" * 60)
    print("STAGE 5: MODEL INTERPRETABILITY & SHAP EXPLAINABILITY")
    print("=" * 60)

    engine = get_prediction_engine()

    # 1. Global Importance
    print("\n1. Top 10 Global Predictive Clinical Determinants (SHAP):")
    if engine.explainer:
        global_imp = engine.explainer.get_global_importance(top_n=10)
        for i, item in enumerate(global_imp):
            print(f" {i+1:2d}. {item['feature']:20s} (Mean |SHAP|: {item['importance']:.4f})")

    # 2. Local Patient Attribution Case Study
    sample_patient = {
        "age": 62,
        "sex": 1,
        "cp": 3,
        "trestbps": 150.0,
        "chol": 270.0,
        "fbs": 0,
        "restecg": 1,
        "thalach": 120.0,
        "exang": 1,
        "oldpeak": 2.5,
        "slope": 2,
        "ca": 2,
        "thal": 3,
    }

    print("\n2. Local Patient Attribution Case Study:")
    result = engine.predict_patient(sample_patient)
    print(f" - Predicted Probability: {result['probability']*100:.1f}%")
    print(f" - Assigned Risk Tier:    {result['risk_tier']}")
    print("\nTop Local SHAP Factor Attributions:")
    for attr in result["feature_attributions"]:
        sign = "+" if attr["direction"] == "increases_risk" else "-"
        print(
            f"   {attr['feature']:15s} (Val: {str(attr['patient_value']):>4s}) -> "
            f"{sign} {abs(attr['attribution']):.4f} log-odds impact ({attr['direction']})"
        )

if __name__ == "__main__":
    main()

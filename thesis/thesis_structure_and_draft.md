# Academic Bachelor's Thesis Blueprint & Research Report

**Working Title:** Design and Development of a Web-Based Machine Learning System for Cardiovascular Risk Prediction and Analysis  
**Alternative Title:** A Comparative Study of Machine Learning Methods for Cardiovascular Risk Prediction with a Web-Based Data-Intensive Implementation  
**Degree:** Bachelor of Science in Computer Engineering  
**Author:** Mohammad Hasan Talebi  

---

## Chapter 1: Introduction

### 1.1 Problem Statement & Clinical Relevance
Cardiovascular diseases (CVDs) constitute the leading etiology of non-communicable global mortality, accounting for an estimated 17.9 million fatalities annually according to the World Health Organization. While routine physiological parameters and non-invasive biomarkers (resting blood pressure, serum cholesterol, electrocardiographic alterations, and treadmill exercise performance) are routinely collected, identifying non-linear multivariate interactions remains challenging in clinical practice.

### 1.2 Motivation: The Dual Imperative
Deploying machine learning within clinical decision workflows requires fulfilling two co-equal requirements:
1. **Scientific Integrity & Discrimination:** Preprocessing pipelines must be mathematically sound, rigorously validated against data leakage, and systematically benchmarked across diverse algorithmic paradigms.
2. **Data-Intensive Software Engineering:** To transition from offline notebooks to operational utility, models must be embedded within scalable, decoupled web architectures offering persistent audit logging and Explainable AI (XAI).

### 1.3 Research Questions
- **Primary Research Question (RQ1):** *How do different machine learning approaches perform for cardiovascular risk prediction, and which patient features contribute most to the resulting predictions?*
- **Secondary Research Questions:**
  - **SRQ1:** How does leakage-free preprocessing compare against uncalibrated models?
  - **SRQ2:** How do linear, distance-based, rule-based, bagging, and boosting ensemble families compare in cross-validation stability?
  - **SRQ3:** Which clinical evaluation metrics (Recall vs. Precision vs. ROC-AUC) best reflect screening performance?
  - **SRQ4:** Which physiological biomarkers dominate global and local decision boundaries?
  - **SRQ5:** How can an explainable prediction pipeline be exposed via a REST API and relational persistence layer?

### 1.4 Tested Hypotheses
- **H1:** *Ensemble-based models (Random Forest, Gradient Boosting, AdaBoost) demonstrate different generalization behavior from a regularized linear baseline on the Cleveland benchmark.*
- **H2:** *Derived hemodynamic interaction features alter cross-validation discriminative capability compared to raw parameters.*
- **H3:** *Different model families produce distinct feature-importance hierarchies, yet share core clinical drivers (fluoroscopy vessel count, ST depression, maximum exercise heart rate).*

---

## Chapter 2: Background

### 2.1 Clinical Foundations of Cardiovascular Risk
Overview of cardiovascular risk etiology, the Framingham risk study traditions, resting versus stress electrocardiography, and the role of exercise stress testing (Bruce protocol).

### 2.2 Supervised Binary Classification in Healthcare
Theoretical foundation of binary classification $f: \mathcal{X} \to \{0, 1\}$. Logistic regression log-odds modeling, Support Vector Machine maximum margin hyperplanes, Decision Tree recursive binary splitting, Random Forest bagging decorrelation, and Gradient Boosting functional gradient descent.

### 2.3 Explainable Artificial Intelligence (XAI)
The trade-off between predictive complexity and interpretability. Game-theoretic Shapley values and SHAP (SHapley Additive exPlanations):
$$\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N| - |S| - 1)!}{|N|!} (v(S \cup \{i\}) - v(S))$$
Properties of local accuracy, missingness, and consistency.

---

## Chapter 3: Related Work

Critical synthesis of prior cardiovascular risk classification studies (e.g., Detrano et al., Janosi et al., modern deep learning vs. ensemble benchmarking). Analysis of common methodological deficiencies in literature:
1. Uncontrolled data leakage (imputing or scaling across full datasets prior to splitting).
2. Reporting sole accuracy metrics on imbalanced clinical cohorts without sensitivity/recall.
3. Lack of model interpretability resulting in "black box" barriers to clinical adoption.
4. Monolithic non-reproducible scripts without modular software engineering or automated testing.

---

## Chapter 4: Dataset & Exploratory Data Analysis

### 4.1 Cohort Provenance
- Benchmark: Cleveland Clinic Foundation ($N = 303$).
- Attributes: 13 physiological predictors + 1 binary target (`num` binarized to $>0$).
- Baseline prevalence: $54.13\%$ healthy (Class 0), $45.87\%$ significant disease (Class 1).

### 4.2 Exploratory Findings
- Pearson correlation identified `ca` ($r = 0.460$), `oldpeak` ($r = 0.425$), `cp` ($r = 0.414$), and inverse heart rate `thalach` ($r = -0.417$) as primary linear correlates.
- Missingness: `ca` (4 missing), `thal` (2 missing).

---

## Chapter 5: Methodology & Experimental Design

### 5.1 Leakage Prevention Architecture
Partitioning ($80\%$ train, $20\%$ hold-out test) precedes all feature transformations.

### 5.2 Preprocessing Pipeline
`ColumnTransformer`:
- Numerical: `SimpleImputer(strategy='median')` + `StandardScaler()`.
- Categorical: `SimpleImputer(strategy='most_frequent')` + `OneHotEncoder(handle_unknown='ignore')`.

### 5.3 Experimental Protocol (Experiments A to F)
- **Experiment A (Baseline):** Un-tuned Logistic Regression.
- **Experiment B (7-Model Benchmark):** Logistic Regression, KNN, Decision Tree, Random Forest, SVM, AdaBoost, Gradient Boosting.
- **Experiment C (Hyperparameter Tuning):** Grid search with Stratified 5-Fold Cross-Validation.
- **Experiment D (Feature Engineering):** Evaluating clinical derived ratios (`hr_max_ratio`, `bp_chol_product`, `exang_oldpeak_interaction`).
- **Experiment E (Explainability):** Global and local SHAP attributions.
- **Experiment F (Hold-out Test Validation):** Single evaluation on untouched $N = 61$ partition.

---

## Chapter 6: System Design & Implementation

### 6.1 Modular Software Architecture
- Layered separation: Data tier (`src/data`), Modeling tier (`src/models`), Backend API (`app/api`, `app/schemas`), Persistence (`app/database`), and Presentation (`app/templates`, `app/static`).
- Zero-downtime singleton pipeline preloading in FastAPI lifespan.

### 6.2 Database Schema & ER Design
`prediction_records` table storing all 13 clinical inputs, predicted probability, categorical risk tier, and JSON-serialized local SHAP attributions.

---

## Chapter 7: Experimental Results

### 7.1 Cross-Validation Benchmark (Experiment B & C)

| Algorithm | Model Family | CV Accuracy | CV Recall | CV ROC-AUC (Mean ± Std) |
|---|---|---|---|---|
| **Logistic Regression (Tuned)** | Linear | **84.7%** | **78.4%** | **0.9065 ± 0.0197** |
| Random Forest | Bagging Ensemble | 81.4% | 75.6% | 0.8858 ± 0.0411 |
| Support Vector Machine | Kernel | 83.1% | 76.5% | 0.8850 ± 0.0160 |
| K-Nearest Neighbors | Instance/Distance | 82.6% | 79.2% | 0.8729 ± 0.0551 |
| AdaBoost | Boosting Ensemble | 78.1% | 72.9% | 0.8668 ± 0.0330 |
| Gradient Boosting | Boosting Ensemble | 79.8% | 78.4% | 0.8555 ± 0.0175 |
| Decision Tree | Rule-Based | 70.2% | 67.5% | 0.7001 ± 0.0443 |

### 7.2 Hold-out Test Performance (Experiment F, $N = 61$)
- **Accuracy:** $88.52\%$
- **Precision:** $83.87\%$
- **Recall / Sensitivity:** $\mathbf{92.86\%}$ (26 / 28 true cardiac patients identified)
- **Specificity:** $84.85\%$ (28 / 33 non-diseased correctly cleared)
- **F1-Score:** $88.14\%$
- **ROC-AUC:** $\mathbf{0.9621}$
- **Confusion Matrix:** $TN = 28, FP = 5, FN = 2, TP = 26$

### 7.3 Global SHAP Determinants (Experiment E)
1. `ca` (Fluoroscopy vessel count): Mean $|SHAP| = 0.5848$
2. `thalach` (Max heart rate achieved): Mean $|SHAP| = 0.2567$
3. `thal_3.0` (Normal Thalassemia): Mean $|SHAP| = 0.2548$
4. `cp_4.0` (Asymptomatic angina): Mean $|SHAP| = 0.2544$
5. `oldpeak` (ST depression): Mean $|SHAP| = 0.1756$

---

## Chapter 8: Discussion

### 8.1 Hypothesis Evaluation
- **H1 Confirmed:** Linear regularized modeling outperformed complex tree ensembles on this sample size ($N=303$), demonstrating the bias-variance trade-off where flexible ensembles overfit small clinical feature spaces.
- **H2 Evaluated:** Feature engineering provided physiological clarity; however, regularized linear models already capture additive effects effectively.
- **H3 Confirmed:** Fluoroscopy vessel count (`ca`) and ST depression (`oldpeak`) proved globally dominant across both linear and ensemble explication.

### 8.2 Practical Implications
The system demonstrates that high recall ($92.86\%$) and explainability can be combined in lightweight web services responding in under 50 milliseconds.

---

## Chapter 9: Ethics, Dataset Limitations & Medical Safety

### 9.1 Academic Prototype Disclaimer
Explicit demarcation that this system is a scientific benchmark prototype and **must never** substitute for certified diagnostic clinical workflows or medical practitioner judgment.

### 9.2 Limitations
1. Sample size $N=303$ from a single historical cohort.
2. Demographic skew towards male subjects ($68\%$ male).
3. Evolving diagnostic biomarkers not captured in historical records (e.g. Troponin-I, Coronary Calcium Scoring).

---

## Chapter 10: Conclusion & Future Work

### 10.1 Summary of Contributions
1. Complete, leakage-free data science pipeline benchmarked across 7 algorithms.
2. Dual-level SHAP explainability embedded directly in client-side visualizations.
3. Modular FastAPI + SQLAlchemy web architecture with full persistence and CSV export.
4. $100\%$ automated test suite passing across 21 unit and integration tests with $74\%$ code coverage.
5. Dockerized container orchestration.

### 10.2 Future Extensions
Multi-center federated cohort validation, dynamic model calibration curves (Brier score optimization), and HL7/FHIR health interoperability protocols.

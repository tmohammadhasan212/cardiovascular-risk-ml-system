# Scientific Research Methodology Document

## 1. Primary Research Question & Hypotheses

### Primary Research Question
> **How do different machine-learning approaches perform for cardiovascular risk prediction, and which patient features contribute most to the resulting predictions?**

### Tested Scientific Hypotheses
- **H1 (Algorithm Superiority):** *Ensemble-based algorithms (Random Forest, Gradient Boosting, AdaBoost) demonstrate distinct generalization performance compared to a linear baseline on the Cleveland cardiovascular benchmark.*
- **H2 (Feature Engineering Impact):** *Clinically motivated derived features (e.g. hemodynamics-lipid product, heart rate reserve ratio) alter cross-validation discriminative capability compared to raw clinical features.*
- **H3 (Interpretability Alignment):** *Feature importance patterns derived from game-theoretic SHAP attributions align with established cardiovascular risk factors (fluoroscopy vessel count, chest pain category, ST depression).*

---

## 2. Benchmark Dataset & Quality Assurance

- **Cohort Source:** Cleveland Clinic Foundation (UCI Machine Learning Repository #45).
- **Sample Size:** $N = 303$ patient records, 14 attributes.
- **Target Distribution:**
  - Class 0 (No significant heart disease, $< 50\%$ vessel narrowing): 164 cases ($54.13\%$)
  - Class 1 (Significant disease present, $\ge 50\%$ vessel narrowing): 139 cases ($45.87\%$)
- **Missing Data Handling:**
  - `ca` (fluoroscopy vessels): 4 missing values ($1.32\%$).
  - `thal` (thalassemia defect scan): 2 missing values ($0.66\%$).
  - Missingness is handled strictly inside the scikit-learn training pipeline via median imputation for numerical features and most-frequent mode imputation for categorical features.

---

## 3. Data Leakage Prevention Protocol

Data leakage represents one of the most prevalent flaws in published clinical machine learning studies. The system enforces strict architectural safeguards:
1. **Partition Precedence:** The complete dataset ($N = 303$) is split into an $80\%$ Training Set ($N = 242$) and a $20\%$ Untouched Hold-out Test Set ($N = 61$) with target stratification before any imputation, scaling, or transformation.
2. **Encapsulated Transformers:** Scikit-learn `Pipeline` and `ColumnTransformer` learn statistical parameters (e.g. mean, standard deviation, imputer medians, one-hot category vocabularies) **exclusively on the training folds**.
3. **Cross-Validation Integrity:** Stratified 5-Fold Cross-Validation applies the unfitted pipeline separately to each fold's training split, preventing validation fold information from influencing feature scaling.
4. **Single Test Evaluation:** The hold-out test set is evaluated exactly once after model selection and hyperparameter optimization are finalized.

---

## 4. Evaluated Machine Learning Algorithms

The experimental study evaluates seven candidate model families:

1. **Logistic Regression (Linear Baseline):**
   - L2-regularized linear model optimizing log-odds.
   - Serves as the benchmark for interpretability and linear separability.
2. **K-Nearest Neighbors (KNN - Instance-Based):**
   - Non-parametric metric distance classifier ($k = 5$, Euclidean distance on standard-scaled features).
3. **Decision Tree (Rule-Based):**
   - CART implementation splitting on Gini impurity.
4. **Random Forest (Bagging Ensemble):**
   - Ensemble of 100 decorrelated decision trees reducing variance through bootstrap aggregation.
5. **Support Vector Machine (SVM - Kernel-Based):**
   - Maximum-margin hyperplane with Radial Basis Function (RBF) and Linear kernels.
6. **AdaBoost (Adaptive Boosting):**
   - Sequential boosting algorithm focusing subsequent weak learners on previously misclassified cases.
7. **Gradient Boosting (GBDT):**
   - Gradient-descent optimization in functional space building sequential shallow regression trees.

---

## 5. Evaluation Metrics & Clinical Significance

Rather than relying solely on accuracy, the evaluation incorporates metrics designed for clinical risk screening:

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$\text{Recall (Sensitivity)} = \frac{TP}{TP + FN}$$

$$\text{Specificity} = \frac{TN}{TN + FP}$$

$$\text{Precision} = \frac{TP}{TP + FP}$$

$$F_1\text{-Score} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

$$\text{ROC-AUC} = \int_{0}^{1} \text{TPR}(FPR^{-1}(t)) \, dt$$

**Clinical Implication:** In cardiovascular screening, **False Negatives (FN)** carry catastrophic clinical risk (a diseased patient is dismissed without treatment), whereas **False Positives (FP)** result in secondary non-invasive follow-up testing. Therefore, **Recall (Sensitivity)** and **ROC-AUC** are prioritized during model selection.

---

## 6. Experimental Results Summary

### 5-Fold Stratified Cross-Validation Comparison on Training Set ($N = 242$)

| Model Family | CV Accuracy | CV Precision | CV Recall (Sensitivity) | CV F1-Score | CV ROC-AUC (Mean ± Std) |
|---|---|---|---|---|---|
| **Logistic Regression (Tuned)** | **84.30%** | **83.87%** | **83.78%** | **83.35%** | **0.9117 ± 0.0210** |
| Support Vector Machine (RBF) | 83.05% | 85.34% | 76.52% | 80.41% | 0.8850 ± 0.0160 |
| AdaBoost | 78.50% | 78.43% | 72.92% | 75.22% | 0.8668 ± 0.0330 |
| Gradient Boosting | 80.17% | 78.49% | 78.38% | 77.92% | 0.8555 ± 0.0175 |
| Random Forest | 81.42% | 80.89% | 78.38% | 79.16% | 0.8943 ± 0.0280 |
| K-Nearest Neighbors | 82.23% | 83.79% | 75.65% | 79.27% | 0.8682 ± 0.0320 |
| Decision Tree | 73.55% | 70.97% | 72.07% | 71.30% | 0.7335 ± 0.0370 |

### Final Evaluation on Untouched Test Set ($N = 61$)

| Metric | Result | Clinical Interpretation |
|---|---|---|
| **Accuracy** | 88.52% | High general agreement across unseen cohort |
| **Precision** | 83.87% | 26 of 31 positive predictions were true disease cases |
| **Recall (Sensitivity)** | **92.86%** | Captured 26 of 28 true cardiac patients (only 2 false negatives) |
| **Specificity** | 84.85% | Correctly identified 28 of 33 disease-free individuals |
| **F1-Score** | 88.14% | Strong harmonic mean between precision and recall |
| **ROC-AUC** | **0.9621** | Outstanding discriminative power separating classes |

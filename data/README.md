# Cardiovascular Disease Dataset Documentation

## 1. Dataset Origin & Citation
- **Source**: UCI Machine Learning Repository — Heart Disease Dataset (Cleveland Clinic Foundation)
- **Creators / Principal Investigators**:
  - Hungarian Institute of Cardiology, Budapest: Andras Janosi, M.D.
  - University Hospital, Zurich, Switzerland: William Steinbrunn, M.D.
  - University Hospital, Basel, Switzerland: Matthias Pfisterer, M.D.
  - V.A. Medical Center, Long Beach and Cleveland Clinic Foundation: Robert Detrano, M.D., Ph.D.
- **URL**: [UCI Machine Learning Repository: Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease)
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

---

## 2. Dataset Overview
- **Number of Records**: 303 patient records
- **Number of Attributes**: 14 (13 clinical features + 1 binary target)
- **Target Variable**: `target` (0 = no presence of heart disease [< 50% diameter narrowing], 1 = presence of heart disease [> 50% diameter narrowing])
- **Class Balance**: 
  - Class 0 (No Heart Disease): 164 cases (~54.1%)
  - Class 1 (Heart Disease): 139 cases (~45.9%)
  - Relatively well-balanced binary classification setting.

---

## 3. Attribute Dictionary

| Attribute | Name | Type | Unit / Encoding | Clinical Description & Reference Range |
|---|---|---|---|---|
| 1 | `age` | Numerical (Integer) | Years | Patient age in completed years (29 to 77) |
| 2 | `sex` | Categorical / Binary | 1 = Male, 0 = Female | Biological sex |
| 3 | `cp` | Categorical (Nominal) | 0: Typical angina<br>1: Atypical angina<br>2: Non-anginal pain<br>3: Asymptomatic | Chest pain type experienced by patient |
| 4 | `trestbps` | Numerical (Integer) | mm Hg | Resting blood pressure on admission to hospital (Normal: < 120, Elevated: 120-129, Hypertensive: ≥ 130) |
| 5 | `chol` | Numerical (Integer) | mg/dl | Serum cholesterol in mg/dl (Desirable: < 200, Borderline: 200-239, High: ≥ 240) |
| 6 | `fbs` | Categorical / Binary | 1 = True (> 120 mg/dl)<br>0 = False | Fasting blood sugar level |
| 7 | `restecg` | Categorical (Nominal) | 0: Normal<br>1: ST-T wave abnormality<br>2: Probable/definite left ventricular hypertrophy | Resting electrocardiographic measurement results |
| 8 | `thalach` | Numerical (Integer) | bpm | Maximum heart rate achieved during exercise stress testing |
| 9 | `exang` | Categorical / Binary | 1 = Yes, 0 = No | Exercise-induced angina |
| 10 | `oldpeak` | Numerical (Float) | mm | ST depression induced by exercise relative to rest |
| 11 | `slope` | Categorical (Ordinal) | 0: Upsloping<br>1: Flat<br>2: Downsloping | Slope of peak exercise ST segment |
| 12 | `ca` | Numerical / Discrete | 0 to 3 vessels | Number of major vessels (0-3) colored by flourosopy |
| 13 | `thal` | Categorical (Nominal) | 1: Normal<br>2: Fixed defect<br>3: Reversible defect | Thalassemia blood condition scan |
| 14 | `target` | Binary Target | 0: Absence, 1: Presence | Cardiovascular disease diagnosis indicator |

---

## 4. Missing Values & Preprocessing Strategy
- In the raw Cleveland dataset, a tiny fraction of values are encoded as `?`:
  - `ca`: 4 missing values
  - `thal`: 2 missing values
- **Strict Leakage Prevention**:
  - Imputation statistics (median for numerical, most frequent for categorical) are computed **strictly on the training split** and applied to the validation/test splits.
  - Categorical variables (`cp`, `restecg`, `slope`, `thal`) are one-hot encoded with unknown handling.
  - Continuous numerical variables (`age`, `trestbps`, `chol`, `thalach`, `oldpeak`) are standardized (`StandardScaler`) based solely on training statistics.

---

## 5. Limitations & Bias
1. **Sample Size**: 303 observations is typical for classical clinical benchmarks, but limits generalization to broader heterogeneous populations. Cross-validation standard deviations must be transparently reported.
2. **Gender Imbalance**: The sample has a higher proportion of male patients, requiring careful fairness and subgroup considerations.
3. **Institutional Context**: Data collected from a single medical center cohort (Cleveland Clinic Foundation).
4. **Historical Benchmark**: Collected in the 1980s; treatment standards and diagnostic biomarkers (e.g. high-sensitivity troponin) have since evolved.
5. **Academic Disclaimer**: The dataset and derived models are solely intended for academic exploration and scientific methodology demonstration, **not** for medical diagnosis or clinical patient care.

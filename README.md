# 🏥 Nigerian Hospital Records Analysis

A healthcare data cleaning, medical statistics and visualization project using Python.

---

## 📋 Project Overview

This project involved cleaning and analyzing a complex Nigerian hospital records dataset
containing 370 patient records across 7 hospitals, 6 departments and 10 diagnoses.
Every column had serious quality issues — the goal was to clean everything from scratch,
compute medical statistics and extract healthcare insights through visualization.

---

## 🛠️ Tools & Libraries

- **Python**
- **Pandas** — data cleaning & analysis
- **NumPy** — numerical operations
- **Matplotlib** — data visualization

---

## 🧹 Data Quality Issues Handled

| Column | Problem | Solution |
|---|---|---|
| Age | Negatives, '25yrs' strings, outliers like 450 | Strip 'yrs', slice outliers, abs() |
| BloodPressure | 4 formats: '120/80', '120-80', '120 over 80', '120' | Unified separator, split into Systolic/Diastolic |
| BMI | Negatives, '24.5 kg/m2', outliers > 100 | Strip units, abs(), divide by 10 if > 100 |
| BloodGlucose | Negatives, '120 mg/dL', outliers > 1000 | Strip units, divide by 10 if > 1000 |
| TreatmentCost | 'NGN50,000', '50000 naira', negatives | Strip symbols, abs(), group fill |
| InsuranceProvider | 'nhis', 'AXA', 'NIL' mixed | Dictionary mapping |
| AdmissionDate | 4 date formats + 'N/A' values | pd.to_datetime(format='mixed') |
| Hospital | Abbreviations: 'AKTH', 'NHA', 'abuth' | Manual mapping to full names |
| Duplicates | 20 duplicate rows | drop_duplicates() |

---

## 📐 Medical Statistics Computed

| Metric | Formula |
|---|---|
| Pulse Pressure | Systolic - Diastolic |
| Mean Arterial Pressure (MAP) | Diastolic + (Pulse Pressure / 3) |

---

## 📊 Key Findings

- 🏥 **National Hospital Abuja** generates the highest total revenue
- 🦴 **Fractures** are the most expensive diagnosis — Avg ₦286,088
- 📈 Average MAP of **103.9 mmHg** — above hypertension threshold of 100
- ⚖️ Average BMI of **29.7** — borderline obese patient population
- 💊 Recovery rate: **60%** | Avg hospital stay: **15.1 days**

---

## 📁 Files

| File | Description |
|---|---|
| `project3_hospital_record_.py` | Full Python source code |
| `hospital_data_messy.csv` | Raw messy dataset |

---

## 🚀 How to Run

```bash
pip install pandas numpy matplotlib
python project3_hospital_record_.py
Self-taught Data Science project — part of my journey toward becoming a Machine Learning Engineer.

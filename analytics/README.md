# Titanic Analytics Pipeline

This module performs exploratory data analysis and predictive modeling on the Titanic dataset.

---

# Part A — Exploratory Data Analysis

## Data Profiling
The Titanic dataset was loaded using Seaborn and profiled using shape, info, descriptive statistics, and missing-value percentages.

## Missing Value Handling
- `embarked` and `embark_town`: missing values were below 5%, so the affected rows were dropped.
- `age`: missing values were approximately 19.87%, so they were imputed using the median.
- `deck`: approximately 77.22% of the values were missing, so the column was dropped because reliable imputation was not appropriate.

## Univariate Analysis
Age and fare were analyzed using histograms and box plots. Outliers were identified using the IQR method.

Fare showed a right-skewed distribution, with the mean greater than the median and mode.

## Bivariate Analysis
Survival rates were analyzed by sex, passenger class, and the combination of sex and passenger class.

The two strongest correlations were:
- `pclass` and `fare`: **-0.548**
- `sibsp` and `parch`: **0.415**

## Multivariate Data Story
Four visualizations were used to explore survival patterns based on sex, age, fare, and passenger class. Overall, female passengers had higher survival rates, and passenger class and fare were also associated with survival outcomes.

## Standardization Check
Age and fare were standardized using z-score standardization. After transformation, both features had approximately mean **0** and standard deviation **1**.

---

# Part B — Predictive Modeling

## Train-Test Split
The dataset was split into training and testing sets using a **stratified train-test split** because the target variable (`survived`) was moderately imbalanced. Stratification preserved the original class distribution in both the training and testing datasets.

## Data Preprocessing
A **ColumnTransformer** and **Pipeline** were used to ensure preprocessing was performed correctly.

- Numeric features (`age`, `sibsp`, `parch`, `fare`) were standardized using **StandardScaler**.
- Categorical features (`sex`, `embarked`) were encoded using **OneHotEncoder**.
- Missing values had already been handled during Part A, so no imputation step was required in the modeling pipeline.

## Classification Models
Three classification models were trained and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest

Each model was evaluated using:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix

The Decision Tree model was also visualized using `plot_tree()`.

## Imbalance Handling
Three imbalance handling strategies were compared using the Random Forest model:

1. Baseline (no imbalance handling)
2. `class_weight='balanced'`
3. SMOTE oversampling

The baseline Random Forest model achieved the best overall performance, indicating that the dataset's class imbalance was not severe enough to require additional balancing techniques.

## Hyperparameter Tuning
Random Forest hyperparameters were optimized using **GridSearchCV**.

Best Parameters:
- `n_estimators = 200`
- `max_depth = 5`
- `max_features = "sqrt"`

The tuned model achieved an **Out-of-Bag (OOB) Score of approximately 0.816**.

## Regression Analysis
A multivariate Linear Regression model was built to predict the **fare**.

Evaluation metrics included:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score
- Adjusted R²

The residual plot showed **heteroscedasticity**, indicating that prediction errors increased as the predicted fare increased. The model performed better for lower fare values than for higher fare values.

## Model Comparison
Classification and regression models were summarized in separate metric groups.

Among the classification models, **Random Forest** achieved the best overall performance with:
- Accuracy: **82.6%**
- Precision: **79.4%**
- Recall: **73.5%**
- F1 Score: **76.3%**
- ROC-AUC: **0.823**

Although Logistic Regression achieved a slightly higher ROC-AUC, Random Forest provided the best balance across all evaluation metrics.

## Model Persistence
The best-performing Random Forest pipeline, including preprocessing and the trained classifier, was saved using **Joblib**.

The saved pipeline was successfully reloaded and used to make predictions directly on raw, unprocessed passenger data, confirming that the pipeline performs preprocessing and prediction end-to-end.

---

## Files

```
analytics/
│
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── titanic.csv
├── clean_titanic.csv
├── best_random_forest_pipeline.pkl
└── README.md
```
# Titanic Analytics Pipeline

This module performs exploratory data analysis and predictive modeling on the Titanic dataset.

## Part A — Exploratory Data Analysis

### Data Profiling
The Titanic dataset was loaded using Seaborn and profiled using shape, info, descriptive statistics, and missing-value percentages.

### Missing Value Handling
- `embarked` and `embark_town`: missing values were below 5%, so the affected rows were dropped.
- `age`: missing values were approximately 19.87%, so they were imputed using the median.
- `deck`: approximately 77.22% of the values were missing, so the column was dropped because reliable imputation was not appropriate.

### Univariate Analysis
Age and fare were analyzed using histograms and box plots. Outliers were identified using the IQR method.

Fare showed a right-skewed distribution, with the mean greater than the median and mode.

### Bivariate Analysis
Survival rates were analyzed by sex, passenger class, and the combination of sex and passenger class.

The two strongest correlations were:
- `pclass` and `fare`: -0.548
- `sibsp` and `parch`: 0.415

### Multivariate Data Story
Four visualizations were used to explore survival patterns based on sex, age, fare, and passenger class. Overall, female passengers had higher survival rates, and passenger class and fare were also associated with survival outcomes.

### Standardization Check
Age and fare were standardized using z-score standardization. After transformation, both features had approximately mean 0 and standard deviation 1.

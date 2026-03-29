# House Price Prediction - Nepal

A machine learning project for predicting house prices in Nepal using various regression models and comprehensive data preprocessing.

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Features](#features)
- [Models](#models)
- [Installation](#installation)
- [Project Structure](#project-structure)

<a id ="problem-statement"></a>

## 🎯 Problem Statement

Predict house prices based on housing features such as land area, number of bedrooms, bathrooms, location, road access, and other property characteristics for the Nepali real estate market.
<a id ="dataset"></a>

## 📊 Dataset

- **Source**: [Kaggle - House Price Dataset Nepal](https://www.kaggle.com/datasets/nishanpokh/house-price-dataset-nepal)
- **Size**: Contains real estate listings from Nepal
- **Features**: Title, Location, Price, Land Area, Build Area, Road Access, Facing, Floor, Bedroom, Bathroom, Build Year, Parking, Amenities

### Data Preprocessing

- Price cleaning and standardization (handling different formats: Rs., lakhs, crores)
- Land area conversion to square feet (handling various units: aana, kattha, sq.m, etc.)
- Missing value handling
- Feature engineering (bath per bed ratio, area × road access, area x bedroom)
- Categorical encoding for location and facing direction
  <a id ="features"></a>

## ✨ Features

- Comprehensive exploratory data analysis (EDA)
- Advanced data preprocessing pipeline
- Multiple regression model comparison
- Feature importance analysis
- Model performance evaluation metrics
- Clean, modular code structure

<a id ="models"></a>

## 🤖 Models

The project compares multiple regression algorithms:

- **Linear Regression** - Baseline model
- **Lasso Regression** - L1 regularization
- **Ridge Regression** - L2 regularization
- **Random Forest Regressor** - Ensemble method
- **Gradient Boosting Regressor** - Boosting algorithm
- **AdaBoost Regressor** - Adaptive boosting
- **XGBoost Regressor** - Extreme gradient boosting
- **CatBoost Regressor** - Categorical boosting

### Best Model

- Random Forest Regressor
- Achieved R² ≈ 0.50 on test data

### Key Insights

- Tree-based models significantly outperformed linear models
- Housing price relationships are nonlinear and interaction-driven
- Feature engineering had a major impact on performance

### Evaluation Metrics

- R² Score
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

  <a id ="installation"></a>

## 🛠 Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd house-price-ml
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

<a id ="project-structure"></a>

## 📁 Project Structure

```
house-price-ml/
│
├── README.md
├── requirements.txt
│
├── app/                          # Streamlit application
│
├── data/
│   ├── raw/                      # Raw dataset
│   │   └── Nepali_house_dataset.csv
│   └── processed/                # Processed/cleaned data
│       └── clean_housing.csv
│
├── model/                        # Saved trained models
│
├── notebooks/
│   ├── 01_eda.ipynb             # Exploratory Data Analysis
│   ├── 02_preprocessing.ipynb   # Data preprocessing
│   ├── 03_model_training.ipynb  # Model training and evaluation
│
└── src/
    ├── preprocess.py            # Data preprocessing functions
    └── __pycache__/
```

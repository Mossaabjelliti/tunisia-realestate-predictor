# Tunisia Real Estate Predictor 🇹🇳

> An end-to-end machine learning project for estimating residential property prices in Tunisia from scraped real-estate listings.

This project explores the complete data-science workflow: collecting real-world property listings, cleaning and transforming noisy data, performing exploratory analysis, engineering predictive features, training regression models, and exposing predictions through an API.

## Project goals

The objective is not only to train a model, but to build a reproducible pipeline from raw web data to a usable prediction service.

```text
Property listings
       ↓
Data collection / scraping
       ↓
Cleaning & validation
       ↓
Exploratory data analysis
       ↓
Feature engineering
       ↓
Model training & evaluation
       ↓
Best model
       ↓
FastAPI prediction service
```

## What the project demonstrates

- Web scraping and data acquisition
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Feature engineering for tabular regression
- Machine-learning model comparison
- Model evaluation with regression metrics
- Model serialization and reuse
- FastAPI model serving
- Separation between data collection, ML logic, and API layers

## Project structure

```text
├── scraper/          # Property listing collection
├── data/             # Raw and processed datasets
├── notebooks/        # EDA and model development
├── src/              # Reusable preprocessing, features and training logic
├── api/              # FastAPI prediction service
├── app/              # Optional frontend / prediction interface
├── models/           # Serialized trained models
├── requirements.txt
└── README.md
```

## Data pipeline

### 1. Collection

Property listings are collected from real-estate listing sources and converted into structured records.

### 2. Cleaning

The pipeline handles typical web-data issues such as missing values, inconsistent representations, duplicated listings, and numerical fields embedded in text.

### 3. Feature engineering

Potential predictive variables include property characteristics and location-related information such as:

- property type
- surface area
- number of rooms
- bedrooms / bathrooms
- location
- floor
- parking and amenities
- listing price

The exact feature set is kept in the source pipeline so experiments remain reproducible.

### 4. Modeling

The project is designed around comparing regression approaches rather than assuming a single algorithm is optimal. Evaluation should be reported using metrics such as:

- MAE — Mean Absolute Error
- RMSE — Root Mean Squared Error
- R² — coefficient of determination

## Model evaluation

> Results below should be updated whenever the training pipeline changes.

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Baseline | — | — | — |
| Model 1 | — | — | — |
| Model 2 | — | — | — |

The goal is to select the model based on validation performance and practical prediction behavior, not simply the highest training score.

## API

The repository includes a FastAPI layer for serving trained models.

Typical workflow:

```text
Client
  ↓
FastAPI endpoint
  ↓
Input validation
  ↓
Feature preprocessing
  ↓
Trained model
  ↓
Predicted property price
```

API documentation can be explored through FastAPI's generated Swagger/OpenAPI interface when the service is running.

## Getting started

### Requirements

- Python 3.x
- pip
- Git

### Installation

```bash
git clone https://github.com/Mossaabjelliti/tunisia-realestate-predictor.git
cd tunisia-realestate-predictor

python -m venv venv
```

Windows:

```bash
.\venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the project

Explore the notebooks for EDA and model development, or start the API when a trained model is available:

```bash
uvicorn api.main:app --reload
```

The exact entry point may vary with the current API implementation; see the `api/` directory for the available routes.

## Reproducibility

Raw datasets are not necessarily committed to the repository. Data acquisition should be performed through the scraper/data pipeline before reproducing model experiments.

For a production-quality experiment, record:

- dataset version/date;
- number of observations;
- feature list;
- train/validation/test split;
- preprocessing configuration;
- model parameters;
- evaluation metrics.

## Limitations

Real-estate prices are highly dependent on location, property condition, market timing, and listing quality. A model trained on scraped listings should therefore be treated as an estimation tool rather than an authoritative valuation system.

Web-scraped datasets can also contain selection bias, duplicate listings, stale advertisements, and inconsistent seller-provided information.

## Roadmap

- [ ] Complete and document model benchmark results
- [ ] Add automated data-validation checks
- [ ] Add reproducible training scripts
- [ ] Add feature-importance / explainability analysis
- [ ] Add API tests
- [ ] Add prediction demo
- [ ] Add deployment documentation

## Author

**Mossaab Jelliti**

Portfolio project focused on data science, machine learning, and practical software engineering for the Tunisian market.

- GitHub: [@Mossaabjelliti](https://github.com/Mossaabjelliti)

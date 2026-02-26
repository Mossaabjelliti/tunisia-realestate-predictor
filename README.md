# Tunisia Real Estate Predictor

This project aims to predict real estate prices in Tunisia by scraping data from various property listing websites and training machine learning models.

## Project Structure

- `scraper/`: Web scraping scripts to collect data.
- `data/`: Raw and processed datasets.
- `notebooks/`: Jupyter notebooks for EDA and model development.
- `src/`: Core logic, feature engineering, and model training scripts.
- `api/`: FastAPI backend for model serving.
- `app/`: Frontend application (optional).
- `models/`: Serialized model files.

## Getting Started

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

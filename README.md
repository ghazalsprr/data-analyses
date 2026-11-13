# Data Analyses

A collection of exploratory data analysis projects in Python — each one starts from a real dataset and a few concrete questions, and ends with findings, charts and a reproducible notebook.

## Projects

| # | Project | Questions | Methods |
|---|---|---|---|
| 01 | [NYC Taxi Trips — March 2019](analyses/01-nyc-taxi-trips/) | When do people ride? What does a fare cost? Who tips? | Data cleaning, time-series patterns, linear regression, Mann–Whitney U test |

## Getting started

```bash
git clone https://github.com/ghazalsprr/data-analyses.git
cd data-analyses
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Then open the notebook inside any project's `notebooks/` folder and run all cells.

## Repository layout

Every analysis lives in its own folder under `analyses/` with the same structure:

```
analyses/NN-project-name/
├── README.md        # questions, key findings, figures
├── data/raw/        # original data (never edited)
├── data/processed/  # cleaned data produced by the code
├── notebooks/       # the analysis, top to bottom
├── src/             # reusable loading / cleaning / plotting code
└── figures/         # charts exported by the notebook
```

## Tools

Python · pandas · NumPy · matplotlib · SciPy · scikit-learn · Jupyter

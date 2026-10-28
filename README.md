# 🍎 AgriLoss Insight: Apple Supply Chain Loss Pattern Analyzer

BCA Data Mining project. Finds where and why apples are lost between orchard and mandi in Himachal Pradesh.

## Techniques
| Algorithm | Use |
|---|---|
| K-Means | Groups shipments into low / medium / high risk profiles |
| Decision Tree | Predicts loss level (Low/Medium/High) and ranks loss factors |
| Apriori | Finds rules like `Ambient + PoorRoad + LongHaul -> Loss_High` |

## Setup
```bash
pip install -r requirements.txt
python generate_data.py      # optional, app does it automatically
streamlit run app.py
```

## Files
- `generate_data.py` creates the synthetic dataset (1500 shipments)
- `mining.py` has K-Means, Decision Tree and Apriori logic
- `app.py` is the Streamlit dashboard (Overview, K-Means, Decision Tree, Apriori, Insights)
- `apple_supply_chain.csv` is the dataset

## Using real data
Upload a CSV with the same columns in the sidebar, or replace `apple_supply_chain.csv`.

## Note
Dataset is synthetic (simulated from known loss drivers) since shipment-level data is not public. Mention this in the report.

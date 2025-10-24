# UAE Open Finance Transaction Categorisation Engine

A rule-based, explainable categorisation system built for UAE-specific banking and open-finance data.

## Features
- 🇦🇪 Merchant Knowledge Base (300 UAE entities)
- 🔠 Arabic + English text normalisation
- 🧩 Deterministic + heuristic scoring (no black-box ML)
- 🧾 Full audit trail for compliance
- 📱 Streamlit demo (optional)

## How to run
```bash
pip install -r requirements.txt
python engine/normaliser_and_matcher.py data/bank_txn_sample.csv
python engine/heuristic_mapper.py data/txn_normalised_matched_v1.csv

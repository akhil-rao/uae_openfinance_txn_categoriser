# heuristic_mapper.py
# Step 2: Apply heuristic scoring + taxonomy mapping

import pandas as pd, json, re, numpy as np

def sigmoid(x): return 1 / (1 + np.exp(-x))

def run_mapper(txn_csv, mkb_csv, rationale_json, output_csv):
    mkb = pd.read_csv(mkb_csv, dtype=str).fillna("")
    tx = pd.read_csv(txn_csv, dtype=str).fillna("")
    rationale = json.load(open(rationale_json, encoding="utf-8"))
    out_rows = []
    def detect_keywords(text):
        kws = {
            "V.UTIL": ["dewa","sewa","fewa","فاتورة"],
            "V.TELC": ["etisalat","du","virgin","اتصالات"],
            "V.RETL": ["carrefour","spinneys","lulu","amazon","noon"],
            "V.FOOD": ["mcdonald","talabat","deliveroo","kfc"],
            "V.TRAV": ["emirates","etihad","uber","taxi"]
        }
        for k,v in kws.items():
            for w in v:
                if re.search(rf"\b{w}\b", text): return k
        return ""
    for _, row in tx.iterrows():
        desc = str(row["description_clean"])
        match = str(row["matched_merchant"])
        mkb_row = mkb.loc[mkb["canonical_name"]==match].head(1)
        rationale_fired = []
        cat = ""
        if not mkb_row.empty:
            cat = mkb_row.iloc[0]["l2_vertical"]
            rationale_fired.append("MKB_MATCH")
        if not cat:
            cat = detect_keywords(desc)
            if cat: rationale_fired.append("ARABIC_KEYWORD")
        score = sum(sig["weight"] for sig in rationale["signals"] if sig["code"] in rationale_fired)
        conf = sigmoid(score - 2)
        l0 = mkb_row.iloc[0]["l0_default"] if not mkb_row.empty else "L0.CARD"
        l1 = mkb_row.iloc[0]["l1_default"] if not mkb_row.empty else "L1.BUY"
        out_rows.append({
            "txn_id": row["txn_id"],
            "description_raw": row["description_raw"],
            "clean_text": desc,
            "matched_merchant": match,
            "match_type": row["match_type"],
            "l0_channel": l0,
            "l1_intent": l1,
            "l2_vertical": cat,
            "confidence": round(float(conf),2),
            "rationale_fired": "; ".join(rationale_fired)
        })
    pd.DataFrame(out_rows).to_csv(output_csv, index=False, encoding="utf-8-sig")

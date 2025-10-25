# normaliser_and_matcher.py
# Step 1: Clean + Match Engine for UAE Open Finance Transaction Categoriser

import pandas as pd, re, unicodedata
from rapidfuzz import process, fuzz

def normalize_text(text: str) -> str:
    if pd.isna(text): return ""
    txt = str(text)
    txt = re.sub(r"\bAED\s*\d+(\.\d+)?\b", " ", txt, flags=re.IGNORECASE)
    txt = re.sub(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", " ", txt)
    txt = re.sub(r"\d{2,}", " ", txt)
    txt = txt.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")
    txt = ''.join(ch for ch in unicodedata.normalize('NFKD', txt) if not unicodedata.combining(ch))
    txt = re.sub(r"[^\w\s\u0600-\u06FF]", " ", txt)
    return re.sub(r"\s+", " ", txt).strip().lower()

def detect_language(text: str) -> str:
    if re.search(r"[\u0600-\u06FF]", text): return "AR"
    if re.search(r"[a-zA-Z]", text): return "EN"
    return "UNK"

def mkb_match(description, mkb_df):
    for _, r in mkb_df.iterrows():
        for pattern in str(r["regex_signatures"]).split(";"):
            pattern = pattern.strip()
            try:
                if pattern and re.search(pattern, description, flags=re.IGNORECASE):
                    return r["canonical_name"], "regex", 1.0
            except re.error: continue
    candidates = list(mkb_df["canonical_name"].unique())
    if not candidates: return "", "none", 0.0
    match = process.extractOne(description, candidates, scorer=fuzz.token_sort_ratio)
    if match and match[1] > 85:
        return match[0], "fuzzy", match[1]/100
    return "", "none", 0.0

def run_normaliser(input_csv, mkb_csv, output_csv):
    mkb = pd.read_csv(mkb_csv, dtype=str).fillna("")
    tx = pd.read_csv(input_csv, dtype=str).fillna("")
    out = []
    for _, row in tx.iterrows():
        raw = row.get("description", "")
        cleaned = normalize_text(raw)
        lang = detect_language(cleaned)
        name, mtype, conf = mkb_match(cleaned, mkb)
        out.append({
            "txn_id": row.get("txn_id", ""),
            "description_raw": raw,
            "description_clean": cleaned,
            "language": lang,
            "matched_merchant": name,
            "match_type": mtype,
            "match_confidence": round(conf,2)
        })
    pd.DataFrame(out).to_csv(output_csv, index=False, encoding="utf-8-sig")

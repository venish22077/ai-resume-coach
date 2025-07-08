import re
from typing import List, Dict, Tuple

def clean_text(text: str) -> str:
    """
    Normalize and clean text for comparison
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-_/]", " ", text)
    return re.sub(r"\s+", " ", text)

def match_keywords(jd_keywords: Dict[str, List[str]], resume_text: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Compare JD keywords with resume content and categorize matches.
    Returns:
        {
            "skills_tools": {
                "matched": [...],
                "missing": [...]
            },
            "responsibilities": {
                "matched": [...],
                "missing": [...]
            }
        }
    """
    resume_text = clean_text(resume_text)

    results = {}
    for category, keywords in jd_keywords.items():
        matched = []
        missing = []

        for kw in keywords:
            kw_clean = kw.lower().strip()
            if len(kw_clean) < 3:
                continue
            # simple substring match
            if kw_clean in resume_text:
                matched.append(kw)
            else:
                missing.append(kw)

        results[category] = {
            "matched": sorted(matched),
            "missing": sorted(missing)
        }

    return results

def calculate_match_score(matched: int, total: int) -> float:
    """
    Calculates percentage match score.
    """
    return round((matched / total) * 100, 2) if total else 0.0
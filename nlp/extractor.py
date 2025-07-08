import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

def extract_keywords_from_jd(text: str) -> Dict[str, List[str]]:
    """
    Extract structured keywords from a job description.
    Categories: skills/tools, responsibilities
    """
    doc = nlp(text)
    skills = set()
    responsibilities = set()

    for chunk in doc.noun_chunks:
        if len(chunk.text) > 2 and not chunk.text.lower() in {"we", "you", "your", "our", "this"}:
            skills.add(chunk.text.strip().lower())

    for sent in doc.sents:
        for token in sent:
            if token.pos_ == "VERB" and token.dep_ in {"ROOT", "advcl"}:
                phrase = token.lemma_ + " " + " ".join([w.text for w in sent if w.dep_ in {"dobj", "pobj", "attr"}])
                if len(phrase.strip()) > 5:
                    responsibilities.add(phrase.strip().lower())

    return {
        "skills_tools": sorted(list(skills)),
        "responsibilities": sorted(list(responsibilities))
    }
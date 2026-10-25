"""TenderWise AI: explainable screening of IT procurement tenders.

Educational prototype:
- ranks tender text against a company capability profile using TF-IDF cosine similarity
- flags short deadlines and selected requirements for human review

Similarity is not a probability of winning or proof of compliance.
"""
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent
TENDERS_PATH = ROOT / "sample_tenders.csv"
PROFILE_PATH = ROOT / "company_profile.txt"
OUTPUT_PATH = ROOT / "tender_analysis.csv"

# Terms that should trigger a manual check. Customize for your own organization.
REVIEW_TERMS = [
    "ISO 27001",
    "OEM authorization",
    "24/7 support",
    "onsite support",
    "delivery within 7 days",
    "bank guarantee",
    "performance bond",
]

def main():
    tenders = pd.read_csv(TENDERS_PATH)
    profile = PROFILE_PATH.read_text(encoding="utf-8").strip()

    required_columns = {"tender_id", "title", "description", "deadline_days"}
    missing = required_columns - set(tenders.columns)
    if missing:
        raise ValueError(f"Missing required CSV columns: {', '.join(sorted(missing))}")

    tender_texts = (
        tenders["title"].fillna("") + " " + tenders["description"].fillna("")
    ).tolist()

    # Fit vectorizer on the profile and the tender texts so all texts share one feature space.
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([profile] + tender_texts)
    similarities = cosine_similarity(matrix[0:1], matrix[1:]).ravel()

    results = tenders.copy()
    results["similarity_score"] = (similarities * 100).round(1)
    results["deadline_warning"] = results["deadline_days"].apply(
        lambda days: "URGENT: 7 days or less" if pd.notna(days) and int(days) <= 7
        else ("Check deadline" if pd.notna(days) and int(days) <= 14 else "No short-deadline flag")
    )

    def requirement_flags(text):
        text = str(text).lower()
        matches = [term for term in REVIEW_TERMS if term.lower() in text]
        return "; ".join(matches) if matches else "No configured keyword found"

    results["requirements_to_review"] = results["description"].apply(requirement_flags)
    results["human_review_required"] = "Yes"
    results = results.sort_values("similarity_score", ascending=False)
    results.to_csv(OUTPUT_PATH, index=False)

    print("\nTENDERWISE AI — screening results")
    print("=" * 72)
    for _, row in results.iterrows():
        print(f"\n{row['tender_id']} | {row['title']}")
        print(f"  Similarity score: {row['similarity_score']:.1f}/100 (ranking aid, not probability)")
        print(f"  Deadline: {row['deadline_days']} days — {row['deadline_warning']}")
        print(f"  Requirements to review: {row['requirements_to_review']}")
        print("  Human verification: required")

    print(f"\nSaved detailed results to: {OUTPUT_PATH.name}")
    print("Reminder: read the original tender documents before making any bid decision.")

if __name__ == "__main__":
    main()

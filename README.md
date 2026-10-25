# TenderWise AI
### An explainable AI assistant for IT procurement and tender screening

**Building AI course project**

TenderWise AI helps IT suppliers screen procurement tenders before spending hours on manual review. It compares a tender's description with a company's capability profile, estimates semantic fit using text similarity, and flags practical risks such as short deadlines or requirements that may need human verification.

> **Important:** This is an educational prototype, not a bid/no-bid decision-maker. Similarity scores are not probabilities of winning, legal advice, or proof of technical compliance.

## Summary

TenderWise AI uses lightweight natural-language processing to rank IT tenders by how closely their descriptions match a supplier's capabilities. It also highlights deadlines and requirements that deserve a closer look, so a human team can prioritize its review.

## Background

IT tenders can contain long technical descriptions, delivery conditions, certifications, and administrative requirements. Small sales or presales teams may have limited time to review every opportunity consistently.

The project explores three practical questions:

- Which tenders appear most relevant to our current capabilities?
- Which tenders have deadlines that require urgent attention?
- Which requirements should be verified before a bid decision?

The aim is to support prioritization, not to automatically accept or reject a tender.

## How is it used?

1. Add tender records to `sample_tenders.csv` or replace them with your own authorized data.
2. Edit `company_profile.txt` to describe the supplier's products, services, certifications, and delivery capabilities.
3. Run the script.
4. Review the ranked output, similarity score, deadline warning, and requirement flags.
5. Have a technical and commercial specialist verify the original tender documents before making a decision.

### Example workflow

```text
Tender text + company capability profile
                  |
                  v
       Text preprocessing (TF-IDF)
                  |
                  v
       Cosine similarity score
                  |
                  v
 Deadline and requirement checks
                  |
                  v
 Ranked shortlist for human review
```

## Data sources and AI methods

### Data

The repository includes **fictional sample tenders** for demonstration. They are not real bids, customer records, or market data. A real deployment could use public tender notices or company documents only where access and reuse are permitted.

### AI methods

- **TF-IDF vectorization:** represents tender and capability text as weighted word features.
- **Cosine similarity:** estimates how closely each tender's text matches the capability profile.
- **Transparent rule-based checks:** flags short deadlines and selected terms that should be verified by a person.

The similarity score is a ranking aid, not a calibrated probability. Keyword checks can miss context, synonyms, negation, or requirements written in an unexpected way.

## Run the prototype

Python 3.10 or later is recommended.

```bash
pip install -r requirements.txt
python tenderwise.py
```

The script prints tenders ordered by similarity, with deadline and requirement-review flags. It also writes `tender_analysis.csv`.

## Challenges

- Tender language can be ambiguous, and similar wording does not guarantee technical compliance.
- The prototype does not parse PDFs, verify certificates, calculate a full bid price, or predict the probability of winning.
- Requirements may be implicit or expressed using synonyms that the simple rule checks do not recognize.
- Scores may be biased by the wording of the company profile and the tender text.
- Tender documents may contain confidential or personal information. Use only data you are authorized to process, and avoid uploading sensitive documents to public repositories.
- Final decisions must remain with qualified commercial, technical, and legal reviewers.

## What next?

- Add PDF/DOCX extraction with page-level evidence for each flagged requirement.
- Build a structured checklist for mandatory technical, commercial, and legal criteria.
- Evaluate rankings against historical tenders labelled by human reviewers.
- Compare TF-IDF with sentence embeddings and measure ranking quality on a held-out dataset.
- Add a small web interface and allow reviewers to mark false positives and missed requirements.
- Support multiple languages only after testing with representative tender documents.

## Acknowledgments

- Created as an original project idea for the **Building AI course**.
- Uses scikit-learn's open-source text vectorization and similarity tools.
- The bundled tender examples are fictional and were written for this demonstration.
- No third-party tender documents or customer data are included.

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE).

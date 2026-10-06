# Fraud Intelligence & Control Effectiveness Lab

An independent portfolio case by [Brandon Candela](https://brandoncandela.github.io/) using **Python, SQL, graph/link analysis and control-effectiveness metrics** to investigate synthetic fraud behavior.

## The business problem

A payments platform sees a possible fraud spike. Which accounts should enter the review queue? Which signals form a coherent incident pattern? How should the team change the control without overwhelming analysts or treating a single shared attribute as proof?

The browser demo lets a reviewer tune the risk threshold, observe changes in alert volume, precision and recall, inspect a shared-device cluster, review control health and export an incident recommendation.

## Technical work

- Python creates a deterministic synthetic dataset and reproducible SQLite database.
- SQL uses CTEs, joins, time windows and aggregations to engineer account-level features.
- The dashboard exposes threshold tradeoffs, a relationship graph, incident reconstruction and data-quality monitoring.
- Seven tests verify referential integrity, seeded scenarios, threshold tradeoffs and export consistency.

## Repository map

- `src/generate_lab.py` — synthetic data pipeline and dashboard export
- `sql/schema.sql` — relational model and indexes
- `sql/account_features.sql` — inspectable feature engineering
- `tests/test_lab.py` — pipeline and scenario validation
- `dist/` — public interactive work sample

## Run locally

```bash
python3 src/generate_lab.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --directory dist
```

Then open `http://localhost:8000`.

## Scope and limitations

All people, devices, transactions and outcomes are fictional. The scoring weights are illustrative and are not calibrated probabilities, proprietary logic or production controls. Shared devices, timing and concentration are leads rather than proof. Any real implementation would require mature outcome data, privacy and fairness review, segment testing, monitoring, governance and documented change approval.

Built with AI-assisted development. The analytical assumptions, evidence boundaries and intended business use are documented so reviewers can challenge them.

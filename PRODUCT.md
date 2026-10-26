# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The primary working user is a fraud strategy, financial crime, or risk operations professional reviewing a possible payments fraud spike. The public portfolio audience also includes recruiters, hiring managers, and consulting leaders evaluating Brandon Candela's ability to connect analytics with operational judgment.

## Product Purpose

Fraud Intelligence & Control Effectiveness Lab demonstrates how a reviewer can move from synthetic transaction and relationship data to a prioritized queue, test the effect of a risk threshold, inspect linked behavior, evaluate control health, and write an evidence-bounded recommendation. Success means a first-time reviewer can explain the workload, precision, recall, missed-case, capacity, linkage, and data-quality tradeoffs without mistaking the illustrative score for a calibrated fraud probability.

## Positioning

The product joins reproducible Python and SQL analysis with an interactive control decision: changing one threshold immediately changes alert workload, precision, recall, missed cases, and capacity, while the same workspace keeps link-analysis evidence, alternative explanations, data-quality context, and an exportable recommendation visible.

## Operating Context

The reviewer starts with a possible fraud spike, tunes an illustrative risk threshold, checks the resulting queue, examines a shared-device cluster and weekly control-health data, reconstructs the incident, and records a recommendation with a limitation and next validation step. The interface is a public work sample and must remain understandable without setup.

## Capabilities and Constraints

- Python creates a deterministic synthetic dataset and reproducible SQLite database.
- SQL uses CTEs, joins, time windows, and aggregations to engineer account-level features.
- The browser exposes threshold tradeoffs, a relationship view, incident reconstruction, data-quality monitoring, and Markdown brief export.
- All people, devices, transactions, outcomes, scoring weights, capacity assumptions, and scenarios are synthetic or illustrative.
- The score is not a calibrated probability, a production model, proprietary logic, or a finding of fraud.
- Shared devices, timing, velocity, and concentration are investigative leads that require alternative explanations and validation.
- The redesign must preserve calculations, generated data, exports, tests, static hosting, and methodology access.

## Brand Commitments

Keep the name Fraud Intelligence & Control Effectiveness Lab and Brandon Candela attribution. The voice must be direct, evidence-led, candid about limitations, and credible to senior banking, fintech, technology, and consulting audiences.

## Evidence on Hand

- `dist/data/dashboard.json`: generated synthetic dashboard evidence.
- `dist/data/account_features.csv`: downloadable account-level features.
- `sql/schema.sql` and `sql/account_features.sql`: relational model and feature engineering.
- `src/generate_lab.py`: deterministic generation pipeline.
- `tests/test_lab.py`: seven validation tests.
- `dist/methodology.html`: public methodology and assumptions.
- No real customer data, production outcomes, testimonials, or measured commercial impact are available and none may be fabricated.

## Product Principles

1. Make the control decision and its operational tradeoffs understandable before showing implementation detail.
2. Keep observed synthetic evidence, illustrative labels, analyst interpretation, and recommended action visibly distinct.
3. Treat linkages and scores as leads that support review, never as proof.
4. Show how data quality and review capacity constrain control changes.
5. Preserve enough technical evidence for a recruiter or practitioner to challenge the analysis.

## Accessibility & Inclusion

The public workspace must support keyboard navigation, visible focus, readable contrast, reduced-motion preferences, large touch targets, and usable desktop and mobile layouts. Color cannot be the only indicator of state.

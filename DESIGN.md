# Fraud Intelligence & Control Lab design system

## Design intent

This interface should feel like an incident command file used by a mature fintech risk team. It prioritizes the operating decision, preserves analytical caveats, and lets a recruiter understand the work sample before interacting.

## Foundations

- Public Sans is self-hosted for a clear, institutional voice.
- System monospace is reserved for case identifiers, scores, metrics, and control labels.
- Navy is the decision surface; teal signals active analysis; amber marks uncertainty or monitoring; red is limited to review-worthy labels and validation errors.
- Surfaces use square or nearly square geometry, visible dividers, and restrained shadows. Rounded card grids and decorative gradients are avoided.
- The primary reading width is 1,440px with fluid 5vw gutters and an 18px panel rhythm.

## Component rules

- Buttons are at least 44px tall and use one primary style and one outlined secondary style.
- Section labels are short monospace orientation cues, not decorative captions.
- Tables become labeled records on narrow mobile screens.
- Evidence always appears with a boundary statement so relationships are not presented as proof.
- Dynamic metrics use `aria-live`; account selectors expose `aria-pressed`; every interaction has a visible focus state.

## Signature interaction

The threshold decision corridor compares the current setting with a ten-point move in either direction. It reuses the existing scoring and outcome data and exposes the operational tradeoff between alert workload, recall, and benign lookalikes without changing the model.

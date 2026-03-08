# R1-020 summary

This layer preserves the book-cipher handoff receipts. The target CID `QmddMfUi8AgsRyqa8MdsWqoCLYmV6kVJ4PYm6uo3iQ7WCV` is stable across preserved candidate logs and extracted-CID history, but the current public repo does not yet make that CID fall out deterministically from the committed corpus with one bounded replay. Public canon therefore treats the CID as historically stable and receipt-backed, while marking the exact cleaned corpus / trim / offset / indexing recipe as still needing a fully public deterministic replay.

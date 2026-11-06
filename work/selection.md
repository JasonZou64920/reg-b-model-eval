# Selection of the final ten

## Pool

59 candidates were tested in Condition A. The first 30 (C01 to C31, without C19) were written before any model run. The other 29 (C32 to C64, with gaps) were written after seeing panel results: some to find hard complies cases, and some to repair cases the audit council flagged. 21 were missed by at least one model.

Eleven of the 21 could not be used:
- Contestable gold: C17 and C45 (`adjudication_log.md`).
- Removed by the audit council: C03 (counsel BLOCKER), C29 and C51 (skeptic).
- Replaced by a revised version: C05, C10, C11, C31 and C48 became C55, C56, C53, C57 and C59.
- C52 was not used. Opus's deciding fact on it (current delinquency) was a legitimate unstated fact.

That leaves exactly ten, and all ten are selected:

| # | Case | Gold | Seam | A misses (first try) | A2 misses (fresh draw) | C misses (full rulebook) |
|---|---|---|---|---|---|---|
| 1 | C53 | violates | S4 ECOA reasons vs FCRA key factors | 1 (Sonnet) | 1 | 1 |
| 2 | C47 | violates | S11 boundary of adverse action | 2 (Opus, Sonnet) | 2 | 0 |
| 3 | C24 | complies | S10 incomplete applications | 1 (Sonnet) | 0 | 0 |
| 4 | C25 | depends | S10 incomplete applications | 3 | 3 | 0 |
| 5 | C57 | violates | S12 third-party notices | 1 (Sonnet) | 0 | 0 |
| 6 | C55 | violates | S2 gray band | 3 | 2 | 0 |
| 7 | C59 | depends | S11 boundary of adverse action | 3 | 3 | 2 |
| 8 | C63 | depends | S11 boundary of adverse action | 3 | 3 | 0 |
| 9 | C56 | depends | S3 automatic denial | 3 | 3 | 3 |
| 10 | C58 | depends | S6 engineered features | 2 (Fable, Sonnet) | 3 | 2 |

The facts of every case are exactly the text the panel saw. The reasoning and deciding facts were revised after the audit, without changing their legal content. The document converts straight quotes to curly ones and adds non-breaking spaces; that is typography only.

## Order, cleanest to most subtle

1. **C53**: a score-only first-stage screen whose notice states "below our minimum requirement" plus FCRA key factors. Decided by the rule text and one comment.
2. **C47**: closure for a cured delinquency, with no notice. Decided by one comment on 2(c).
3. **C24**: incompleteness as the stated reason when the model cannot score without income.
4. **C25**: the same notice where the missing item (pay stubs) may or may not have been needed to decide.
5. **C57**: one notice for three banks with pooled reasons.
6. **C55**: gray-band decline where the notice gives only the underwriter's reason.
7. **C59**: closure for delinquency with a letter citing policy. Turns on whether the delinquency was current.
8. **C63**: closure after a move out of the service area with a letter citing policy. Turns on the card agreement.
9. **C56**: prior charge-off that the scorecard does not score. Turns on whether a knockout rule fired.
10. **C58**: stated-versus-estimated income feature. Turns on how the model used the two figures.

The order runs from cases decided by a single provision with every decisive fact stated, through cases that read two provisions together, to cases where the deciding fact sits inside the creditor's decision system.

## Rationale

- **Hardness is binding.** Every case was missed by at least one model on its first try in Condition A, and seven were missed by two or more. Five were missed by all three (C25, C55, C59, C63 and C56), and C58 was missed by all three in the fresh draw.
- **Seams.** The ten cover seven seams: S2, S3, S4, S6, S10, S11 and S12. S11 holds three cases (C47, C59, C63) and S10 holds two (C24, C25).
- **Scoring-model and ML context.** C53, C24, C25, C55, C59, C56 and C58 involve a scorecard, screen or decision model. C57 is an indirect auto-lending platform.
- **Weakest cases, disclosed.** C24 and C57 were each missed by one model on one draw, and both were labeled correctly in the fresh draw. C24 also carries the skeptic's objection that its facts state there was no merits decision (`audit_log.md`). C47 sends no notice, so its violation runs through 9(a)(2) rather than the wording of a 9(b)(2) statement.
- **Hardest cases.** C56 was missed by all three models in every condition, including with the full rulebook. Each model assumed that no automatic-denial rule fired, though the facts never say so. C59 was still missed by two models with the full rulebook. Both assumed the delinquency was still current at closure, which the facts leave open, and Sonnet named that assumption in its reasoning but still labeled the case "complies".

## Deviation from the requested label mix

- **Requested:** 3 complies, 4 violates, 3 depends, plus or minus 1. **Delivered:** 1 complies, 4 violates, 5 depends.
- **Why:** 24 complies candidates were tested. Only two were missed by any model (C24 and C45), and C45 was excluded because its gold label is contestable (`adjudication_log.md`, round 3). Several supplementary rounds wrote complies cases aimed at the patterns the panel does miss: over-reading specificity, comment 9(b)(2)-4, "credit policy" wording, sample-form language and the alternative notice paths. Every model labeled every one of them correctly.
- **Ruling:** the assignment defines hardness ("Cases that a current AI model labels correctly on its first try do not count as hard"). When that conflicted with the label mix, I kept hardness binding. Adding a complies case that every model got right would break the assignment's own test.
- **The deviation is a result in itself.** Of the 39 wrong labels in Condition A, 26 called a deficient or undecided notice compliant. The panel errs toward clearing notices. The finding line on the results strip says so, and the mix is listed as an open question.

## What would change the selection

- With provider API keys, rerun Condition A on GPT and Gemini flagships. A complies case missed by another provider would restore the requested mix, and per-provider results would replace the single-provider panel.
- If a reviewer rejects C24, the set has no complies case. The next eligible case would come from a new round, since every unused hard case is excluded above.

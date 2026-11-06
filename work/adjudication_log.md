# Blind adjudication log

**Reviewer**: an independent agent session (Claude Opus tier). It saw only the verbatim source files and the case facts (`work/blind/case_facts.json`), copied into an isolated folder. It never saw gold labels, reasoning or deciding facts.

**Result**: the reviewer agreed with the gold label on 29 of 30 cases. On all five "depends" cases where it also chose "depends", it named the same deciding fact as the gold. It disagreed on one case (C19). It also flagged a "defensible alternative" on six cases where it agreed with the gold, and each of those is reviewed below.

## Disagreement

### C19 (vehicle model year), gold "depends", reviewer "violates"
- Original facts: the notice listed "Value or type of collateral not sufficient" for a scorecard characteristic measuring vehicle model year. The gold deciding fact was which vehicle was scored: the collateral, so complies, or the applicant's current car, so violates.
- Reviewer: "violates" whichever vehicle was scored, because "Value or type of collateral" is the closest checklist line rather than the actual factor (appendix C, para. 4; comment 9(b)(2)-4). It noted "complies" as defensible if the vehicle is the collateral.
- Re-read of the sources: the reviewer is right that the collateral branch does not resolve cleanly. Comment 9(b)(2)-4 requires the actual factor ("age of automobile"), and appendix C, para. 4 rejects the closest identifiable factor. A model-year characteristic is arguably not the same factor as "value or type" of collateral. So stating the deciding fact did not decide the case, which breaks the depends-case rule.
- Resolution: **revised the facts** so the notice says "Age of collateral." Now the deciding fact resolves the case cleanly. If the scored vehicle is the collateral, the reason is accurate and the notice complies. If it is a vehicle the applicant already owns that does not secure the loan, the reason misdescribes the factor and the notice violates. The revised case went back to the same reviewer, blind; result below.

## Agreements where the reviewer noted a defensible alternative

| Case | Gold | Reviewer's alternative | Ruling |
|---|---|---|---|
| C03 max-points method | depends | violates on its face | Keep. Comment 9(b)(2)-5 makes "any other method that produces results substantially similar" acceptable. Whether a maximum-points ranking does so is empirical, so "violates on its face" assumes a fact the case does not state. |
| C06 passed score, judgmental decline, extra scorecard reasons | violates | complies, since the true reason is listed first | Keep "violates". Comment 9(b)(2)-7 says that when the application passes scoring and is denied judgmentally, "the reasons disclosed must relate to the factors reviewed judgmentally." Listing scorecard characteristics as reasons for the denial misstates the principal reasons (comment 9(b)(2)-2). Flagged for the audit council as a contested case. |
| C10 prior charge-off, scorecard reasons only | depends | complies, reading the facts as a score decline | Keep. The facts state a scorecard result, but they do not state whether a knockout also fired. That gap is the deciding fact, and it is the trap a model falls into. |
| C12 bureau-score-only lender lists key factors as ECOA reasons | complies | violates under a strict reading of comment 9(b)(2)-9 | Keep, marked contested. Comment 9(b)(2)-9 says that disclosing key factors "does not satisfy" ECOA. It does not say the same factors cannot be stated as ECOA reasons when the score is the sole basis. Not preferred for the final ten. |
| C16 24-month average utilization | complies | violates, since the averaging is omitted | Keep. Comment 9(b)(2)-3 says the creditor need not describe how or why a factor affected the applicant. The notice names the factor. |
| C17 stated versus estimated income | depends | violates, since the model never verifies anything | Keep. The reviewer's own deciding fact matches the gold. The alternative depends on whether a stated-versus-estimate discrepancy is a "verification" factor. I read it as one: the variable measures whether the stated income is corroborated. Noted as residual risk. |

## Label set after adjudication

13 violates, 11 complies, 6 depends. 30 cases across 12 seams, no seam with more than 4.

## Second round (same reviewer, blind)

- **Revised C19 ("Age of collateral")**: the reviewer labeled it "complies" with high confidence, reading "vehicle model year" in an auto-loan scorecard as the financed vehicle. That is a reasonable reading of the wording, so the unstated fact was an artifact of phrasing rather than of the law. A hardness skeptic would rightly call it sloppy facts. **Resolution: C19 dropped.**
- **Replacement C31 (dealer notice for three banks, pooled reasons)**: the reviewer labeled it "violates" (12 CFR 1002.9(g); comment 9(g)-1), which agrees with the gold, at high confidence. It noted that comment 9(g)-1 also requires each creditor's address, so I added "name and address" to the facts. The case now turns only on whether reasons are attributed to each creditor.

## Final candidate set going into the hardness test

30 cases (C01 to C18, C20 to C31): 14 violates, 11 complies, 5 depends, across 12 seams with no more than 4 per seam. The gold labels match the blind reviewer on all 30.

## Supplementary candidates, round 1 (C32 to C36, all gold "complies")

These were added after the first Condition A run turned up only one hard complies case (C24). The blind reviewer labeled all five "complies", which agrees with the gold. It noted one wording point on C32 and C34: each describes the right to reasons as applying "if requested within 60 days" but does not say the reasons will be provided within 30 days of a request, which 12 CFR 1002.9(a)(2)(ii) requires. Ruling: keep as drafted for testing, since the panel answered both correctly. If either case is selected, the facts will add "within 30 days of a request". None of the five was missed by any panel model in Condition A, so none is eligible for the final ten.

## Supplementary candidates, round 2 (C37, C39, C42, C44, all gold "complies")

These target two failure modes seen in round 1: over-reading the specificity requirement, and over-reading comment 9(b)(2)-4. The blind reviewer labeled all four "complies" at high confidence with no defensible alternative, which agrees with the gold. On C39 it noted that it took Brightline's reason-selection method as given. All three panel models labeled all four correctly in Condition A, so none is eligible.

## Supplementary candidates, round 3 (C45, C46, gold "complies")

- **C46 ("exceeds the 45% maximum set by our credit policy")**: the blind reviewer said "complies" at high confidence, and all three panel models agreed. Not eligible.
- **C45 (stated income divided by a bureau estimate, notice "Unable to verify income")**: the blind reviewer said "complies" at medium confidence. It named "violates" as a defensible alternative: the model never attempts verification, so the accurate reason is something like "stated income inconsistent with other information", and checking "Unable to verify income" is a closest-checklist-item choice of the kind appendix C, para. 4 rejects. Fable then labeled the case "violates" for exactly that reason.
  - Ruling: both readings are defensible on fully stated facts, and no single unstated fact would resolve them. Under the Phase 3 rule the case is **dropped** rather than counted as a hard complies case. Fable's miss is real, but it comes from a contested gold label, not from the interpretive trap the case was built to test.
  - **Knock-on ruling on C17**: C17 is the "depends" form of the same scenario. Its complies branch ("if the scored variable is the gap, 'Unable to verify income' describes it") rests on the same contested reading, so stating the deciding fact would not cleanly resolve it. That is the same defect that removed C19. **C17 is excluded from the final selection.** It stays in the candidate file and the results so the record is complete.

## Supplementary candidates, round 4 (C47 to C49)

These were added because the main set yielded only 9 hard cases, and round 3 lost C45 to a contested gold. They follow the pattern the panel actually misses: an exclusion, or the final decision-maker, makes a deficient notice look adequate. Blind reviewer results: C47 "violates", C48 "depends" (same deciding fact as the gold), C49 "violates". All three were high confidence with no alternative noted, and all agree with the gold.

## Supplementary candidates, round 5 (C50 to C52)
The blind reviewer labeled C50 "violates", C51 "depends" (same deciding fact as the gold) and C52 "violates", all at high confidence. This agrees with the gold on all three.

## Audit revisions, round 6 (C53 to C59, revising C11, C24, C05, C10, C31, C17 and C48)
The blind reviewer agreed with the gold on all seven. For every depends case it confirmed that stating the deciding fact resolves the case.

Notes it raised:
- **C58**: the single-reason notice means the complies branch must be read as "the gap was what the decline turned on". The deciding fact now says so.
- **C56**: the complies branch reads "largest shortfalls" as the principal reasons. This is residual risk, already noted in the audit log.
- **C53**: it named "complies" as a weaker alternative, on the theory that the score screen is an automatic-denial factor and naming the score is the required specific factor. It rejected that theory itself, because the commentary's automatic-denial examples are facts in the applicant's record, not a composite score. Ruling: keep "violates".

## Round 7 (C60, prequalification)
The blind reviewer said "violates" at high confidence, which agrees with the gold. All three panel models also labeled it correctly, so it is not eligible.

## Round 8 (C61, C62)
- **C61** (gold "complies"; notice of incompleteness, stubs arrived late). The blind reviewer agreed at medium confidence. It noted that the facts do not say what "day 25" is counted from, so the stubs might have arrived inside the 15-day period. No panel model missed C61, so it is not eligible and the ambiguity did not need a ruling.
- **C62** (gold "depends"; a $6,000 counteroffer on a $25,000 request, with a letter citing "our credit policy"). The blind reviewer agreed at high confidence, with the same deciding fact (whether the applicant used or accepted the card). Every panel model labeled it correctly, so it is not eligible.

## Round 9 (C63, closure after a move out of the service area)
The blind reviewer said "depends" at high confidence, with the same deciding fact as the gold (whether the agreement explicitly provided for termination on that ground). It agrees with the gold. All three models labeled C63 "violates" in Condition A, so it is eligible.

## Round 10 (C64, refused loan modification)
The blind reviewer said "violates" at high confidence, which agrees with the gold. No model missed C64 in Condition A, the fresh draw (A2) or the full rulebook (C), so it is not eligible.

## Totals
59 candidates were tested. 30 were written before any model run (C01 to C31, without C19). The other 29 (C32 to C64, with gaps) were written after seeing panel results, to find hard complies cases and to repair cases the audit council flagged. The blind reviewer disagreed with the gold on one candidate (see "Disagreement"). C19 was dropped before testing for ambiguous wording. C45 and C17 were tested and missed, but are excluded from selection because their gold labels are contestable.


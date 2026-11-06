# Audit council log

Four isolated auditors reviewed draft v1 of the deliverable (the ten cases C29, C11, C24, C25, C48, C51, C05, C10, C31, C03) against `sources/`. None saw another's findings.

**Council rules applied:**
- Counsel and spec-checker BLOCKERs are absolute.
- The skeptic yields to counsel on legal correctness.
- The prose editor wins on phrasing.
- Any fix that changes case facts sends the case back through the harness from a fresh first try.

## Findings and rulings

### Regulatory counsel
| Tag | Case | Finding | Ruling |
|---|---|---|---|
| BLOCKER | 10 (C03) | The draft reads the comment 9(b)(2)-5 safe harbor ("any other method that produces results substantially similar ... is also acceptable") as the only test, so the violates branch is unsupported. | **Accepted. C03 removed.** No deciding fact can make a non-matching method a violation without also deciding whether the listed reasons are the principal ones. |
| FIX | 1 (C29) | "owed a specific reason" leaves out the 9(a)(2)(ii) right-to-reasons alternative, and the "misstates" point cites no 9(b)(2) authority. | Accepted. C29 is removed for the skeptic's reasons (below), which moots this. |
| FIX | 2 (C11) | Drops "on the creditor's credit scoring system" for a bureau score, which leaves the Form C-2 analogy open. | Accepted. Revised as C53: the bureau score is the only basis for the decline, and the reasoning explains why it serves as the creditor's scoring system. |
| FIX | 4 (C25) | The facts do not say why Meridian declined. If the model passed the applicant and the stubs were the missing verification, "incomplete" holds, so the named deciding fact does not settle the case. | Accepted. The deciding fact is rewritten around the basis of the denial: a credit decision Meridian could make without the stubs, or a lack of the stubs it needed to decide. The facts are unchanged, so the recorded Condition A responses still apply. All three models labeled the case "complies", which is a miss under either deciding fact. |
| FIX | 4 (C25) | Drops comment 9(a)(1)-4's "(or notice of the right to receive the reasons)". | Accepted in the reasoning. |
| FIX | 5 (C48) | Drops "in default", and resolves the case without the comment's "generally". | Accepted. Revised as C59: the deciding fact says "delinquent or in default", and the reasoning keeps "generally". |
| FIX | 5, 6 (C48, C51) | No notice was sent, so 9(b)(2) is never engaged; the violation is under 9(a)(1)(iii) and (a)(2). | Accepted. C59 now sends a letter citing "our account-management policy", so the violates branch is a 9(b)(2) internal-policy failure. C51 is removed (see skeptic). |
| FIX | 7 (C05) | The facts do not say what the scorecard scores, and "Length of employment" could come from both components. | Accepted. Revised as C55: the facts state the scorecard's largest shortfalls (revolving utilization, recent inquiries). |
| FIX | 8 (C10) | Treats the top four as the principal reasons, and leaves "shortfall" unbenchmarked; the real question is whether the knockout rule fired. | Accepted. Revised as C56: the scorecard has no prior-account characteristic, and the deciding fact is whether a knockout rule declined this application because of the charge-off. |
| FIX | Results | Case 3 is missing from the "other provisions" list, and six cases are decided by text neither condition supplied. | Accepted. A new Condition C supplies the full rulebook. The legend no longer presents those cases as robust. |
| NIT | Method | "as amended effective July 21, 2026" implies the cited provisions were amended. | Accepted. Reworded. |

### Hardness skeptic
| Tag | Case | Finding | Ruling |
|---|---|---|---|
| BLOCKER | 3 (C24) | The facts state both elements of comment 9(a)(1)-3 as conclusions ("Meridian made no decision on the merits"). | Accepted. Revised as C54 with the conclusion removed: the facts say the model cannot score without income, and the income field was blank. |
| BLOCKER | 4 (C25) | A second decisive fact (same as counsel's point). | Accepted (see above). |
| BLOCKER | 6 (C51) | The facts and deciding fact restate comment 2(c)(1)(ii)-1 almost word for word, with no notice and no 9(b)(2) content. | **Accepted. C51 removed.** |
| BLOCKER | Measurement | "can stay hard there" presents a confound (governing text withheld) as robustness. | **Accepted.** Condition C (full rulebook) added for the final ten, and the legend rewritten to state the confound. |
| FIX | 1 (C29) | Hard through wording ("this product"), and the comment's own example ("length of maturity"). | **Accepted. C29 removed.** |
| FIX | 2 (C11) | A card issuer with a score-only criterion is unrealistic because of ability-to-pay rules. | Accepted. C53 moves the case to a first-stage personal-loan screen. |
| FIX | 5 (C48) | Off the assigned rule (no notice). | Accepted (C59 adds the letter). |
| FIX | 7 (C05) | Employment may also be a scored factor. | Accepted (C55). |
| FIX | 8 (C10) | "Shortfall against what?" | Partly accepted. C56 removes the prior account from the scorecard, so the case turns on the knockout. The complies branch still reads "largest shortfalls" as the principal reasons; that residual risk is noted. |
| FIX | 9 (C31) | Unstated premise that the banks' reasons differ. | Accepted. Revised as C57: the facts give each bank's reason. |
| FIX | 10 (C03) | Safe-harbor misreading (same as counsel). | Accepted (removed). |
| FIX | Measurement | "the ten below are the strongest" is contradicted by the data, and per-model miss rates are true by construction. | Accepted. "Strongest" cut. The strip now reports a fresh replication draw, and the per-model totals are relabeled as first-try results on selected cases. |
| FIX | Measurement | Single draws with no temperature control, and the cases were selected on those same draws. | Accepted. Replication draw (Condition A, run 2) added for the final ten and disclosed. |
| FIX | Measurement | "independent reviewer" reads as a human. | Accepted. Now "a separate model session that never saw the gold labels". |
| FIX | Measurement | The supplementary candidates were written after seeing panel results. | Accepted. Disclosed in the method note and `selection.md`. |
| FIX | Set | No ML-feature case. | Accepted. C58 (a revision of C17) is a stated-versus-estimated income feature with a reason that is clean on both branches. |
| NIT | Several | Grader of "f" misses not stated; bare relative paths; "deficient or undecided notice". | Accepted. Grading noted in results, harness line reworded, finding line reworded. |

### Spec checker
| Tag | Finding | Ruling |
|---|---|---|
| BLOCKER | Label mix 1/4/5 is outside 3/4/3 plus or minus 1. | **Not curable from this pool without breaking the assignment's own hardness test.** 22 complies candidates were tested and one was missed with a clean gold. The council keeps hardness binding and discloses the mix. The final mix is reported after the revision round. |
| BLOCKER | Results table text is 8 pt (spec 8.5 to 9.5). | Accepted. Set to 8.5 pt. |
| FIX | Notes under the strip are below body size. | Accepted. Legend and notes set to the body-adjacent size the spec allows for tables (8.5 to 9 pt) and treated as table notes. |
| FIX | Harness line has no URL. | Partly accepted. Reworded to say the folders accompany the sample. The code and results now live in this repository. |
| FIX | Method note does not name the models. | Accepted. |
| FIX | Six cases rest on provisions outside 9(b)(2). | Accepted. Addressed by the removals, by C59's 9(b)(2) hook, and by Condition C. |
| NIT | Straight quotes, citation line breaks, metadata, date formats, double space in labels, footer. | Accepted. Curly double quotes in notice text, non-breaking spaces inside citations, core properties set, one date format. |

### Prose editor
| Tag | Finding | Ruling |
|---|---|---|
| FIX | The method note is four sentences in substance and the subject shifts mid-sentence. | Accepted. Rewritten as three sentences of about 35 words each. |
| FIX | R1, R3, R5, R7, R9: pronoun and agreement slips. | Accepted in the revised reasoning. |
| FIX | R10 uses four names for one test. | Moot (C03 removed). |
| FIX | Citation placement is inconsistent (R3, R10). | Accepted. Every reasoning ends with a parenthetical, regulation first. |
| FIX | Deciding facts mix tenses and subjects, and DF4 refers to a model that case 4 never introduces. | Accepted. One template: "Whether X: if so, ...; if not, ...". DF4 no longer mentions a model. |
| FIX | Finding line carries two claims; the legend joins two sentences with a semicolon. | Accepted. |
| NIT | Terminology drift (customer/cardholder, model/engine/scorecard). | Accepted where the revised text touches it. |

## Revision round
The revised cases C53 to C59 were labeled blind by the same reviewer and run through Condition A from a fresh first try (prompt set `supp6`). The reviewer agreed with every gold label.

| Revised case | Replaces | Condition A misses | Outcome |
|---|---|---|---|
| C53 | C11 | 1 (Sonnet) | Selected |
| C54 | C24 | 0 | Not hard. The cured facts no longer qualify. |
| C55 | C05 | 3 | Selected |
| C56 | C10 | 3 | Selected |
| C57 | C31 | 1 (Sonnet) | Selected |
| C58 | C17 | 2 (Fable, Sonnet) | Selected |
| C59 | C48 | 3 | Selected |

Later candidates. C60 to C64 were written afterwards (`supp7` to `supp10`): C60 (prequalification), C61 (notice of incompleteness), C62 (counteroffer with a policy letter), C63 (closure after a move out of the service area) and C64 (refused loan modification). Only C63 was missed. All three models labeled it "violates" when the gold is "depends". It replaces the counsel-flagged C51 in the S11 slot, and like C59 it sends a letter that cites policy, so its violates branch is a 9(b)(2) failure.

### Rulings left open after the revision round
- **C24 and the skeptic's BLOCKER.** The cure (C54) removes "Meridian made no decision on the merits", and no model missed C54. Without C24 the set has no complies case. Under the council rules, only counsel and spec-checker BLOCKERs are absolute. **Ruling: C24 is kept with its tested text.** Its weakness is disclosed. The facts state the absence of a merits decision as a fact, one model missed it on one draw, and the miss did not recur in the fresh draw (A2) or with the full rulebook (C). It is the weakest case in the set.
- **C47 has no notice.** Counsel's point about C48 and C51 (no notice, so 9(b)(2) is never engaged) applies to C47 as well. **Ruling: kept, and disclosed.** The violation runs through 9(a)(2), which the 9(b)(2) text itself cross-references. Both models that missed it (Opus and Sonnet, in A and again in A2) called it "depends" on whether the closure was tied to the January delinquency. Comment 2(c)(2)(ii)-2 makes a closure based on a past delinquency adverse action as well, so both of their branches lead to a violation. C59 and C63 are the 9(b)(2) versions of the same boundary.
- **Label mix (spec BLOCKER).** The final mix is 1 complies, 4 violates, 5 depends, outside 3/4/3 plus or minus 1. Hardness stays binding (see the spec-checker ruling above). Disclosed as a judgment call and an open question.

## Measurement additions (skeptic BLOCKER and FIX)
These were run on the final ten, plus C64 as a control that no model had missed.
- **A2, a fresh draw.** The identical Condition A prompt was run in new sessions. Misses on the ten went from 22 of 30 to 20 of 30. C24 and C57 were answered correctly by every model, so their hardness rests on a single draw. C55 was missed by two models rather than three.
- **C, the full rulebook.** This adds every provision and comment in `sources/`. Misses fell to 8 of 30. C56 was still missed by all three models, C59 and C58 by two, and C53 by one (Fable said "complies", reading the 640 screen as an automatic-denial factor, which is the theory the blind reviewer considered and rejected). C25, C47, C55, C57 and C63 were answered correctly by every model once the governing commentary was present.
- **Reading.** Most of the difficulty in this set comes from authority outside the text of 9(b)(2): the 2(c) exclusions, 9(a)(1) incompleteness, 9(g) attribution, and the gray-band comment. The deliverable states this in its finding line. C56 and C59 remain hard with everything in hand.

## Final selection
C53, C47, C24, C25, C57, C55, C59, C63, C56, C58, in that order. The ordering and seam coverage are in `selection.md`. Every final citation was checked against `sources/` by `scripts/verify_deliverable.py`.

## Changes to the deliverable after the council
- The method note is three sentences. It names the models and the date, describes the blind reviewer as a separate model session, and discloses that the last 29 candidates were written after early results.
- The results table, legend and table notes are 8.5 pt. Notice text uses curly double quotes. Citations use non-breaking spaces, non-breaking hyphens and word joiners, so no citation splits across a line. Core properties are set (author Jason Zou). There is one date format, and the header uses single-spaced separators.
- The results strip shows each model's first try (A), then the A2 and C miss counts. Condition B is reported only in `results/`, because it ran only on the main set.

## Final pass (one fresh auditor, counsel and spec checker combined, on the rendered PDF)
**No BLOCKERs.** The auditor confirmed all ten gold labels against `sources/`, quoting the governing text for each, and confirmed that every strip cell and every figure in the finding line matches `scores.csv`.

| Tag | Element | Finding | Ruling |
|---|---|---|---|
| FIX | Method, strip | The batching, self-reported model IDs and lack of temperature control were not disclosed, and "given only the case" was inaccurate for batched sessions. | Accepted. The strip note now discloses all three, and the method note says "given only the fixed prompt, the case and the text". |
| FIX | Case 1 (C53) | "the FCRA key factors do not supply the ECOA reasons" overreaches. Comment 9(b)(2)-9 bars relying on the FCRA disclosure, not listing the same factors. | Accepted. The text now says the key factors in the FCRA disclosure "do not satisfy the ECOA duty to state specific reasons". |
| FIX | Case 4 (C25) deciding fact | The binary missed a creditor that had enough data and still cited incompleteness. | Accepted. The deciding fact is now framed on sufficient data, per comments 9(a)(1)-3 and -4. |
| FIX | Case 9 (C56) | "need not be disclosed" is supported by comment 9(b)(2)-4, not -8. | Accepted. The reasoning cites both, and the deciding fact now covers any role for the charge-off outside the scorecard. |
| FIX | Case 10 (C58) deciding fact | The "if not" branch covered only the payment-to-income scenario. | Accepted. The branch is now general, with payment-to-income as the example. |
| FIX | Finding line | The 22 of 30 figure comes from the selection draw, so A2 is the fair comparator. | Accepted. The line compares C (8 of 30) with A2 (20 of 30). |
| FIX | Method note | The "how built" element was thin. | Accepted. The note now says the cases sit where 9(b)(2) meets its interpretations and the definition of adverse action. |
| NIT | Case 2 (C47) | Add the base definition, 1002.2(c)(1)(ii). | Accepted. |
| NIT | Case 6 (C55) | Citation form is inconsistent. | Accepted. 12 CFR 1002.9(b)(2) added. |
| NIT | Finding line | Explain why only one complies case. | Accepted ("one later removed on audit"). |
| NIT | Type size | The prose lines under the strip were 9 pt. | Accepted. Now 9.5 pt. The legend stays at 8.5 pt as a table note. |
| NIT | Cases 7 and 8 | The violates branch assumes the letter gives no notice of the right to reasons. | Not changed. The facts present the policy wording as the stated reason. Noted as residual risk. |
| NIT | Case 9 | "Largest shortfalls" has no stated benchmark. | Not changed. This residual risk is already noted. |
| NIT | Font | The PDF embeds Carlito, the metric-compatible Calibri substitute, because Calibri is not installed in the build environment. The .docx specifies Calibri. | Open question: re-export the PDF from Word for a true Calibri PDF. |

None of these changes touch case facts, so no case was re-run. Deciding-fact edits keep the same decisive unknown, so the existing deciding-fact grades still apply (all models labeled C25, C56 and C58 something other than "depends" in Condition A). Page margins went from 0.7 in to 0.65 in, within the spec range, to keep the document at two pages.

## Later presentation edits (November 1 to 2, 2026)
After the audit, the two-page document was rewritten three times so it would be easier to read:
- first in plainer wording
- then as a memo instead of a table
- then with a clearer layout for each case

The case facts, labels, citations and test results did not change.

Six separate reviewer sessions checked the first two rewrites. Between them they covered the law, the numbers, the spec, clarity, tone and overclaims. Their fixes include:
- correcting which compliant candidate had been set aside (C45, for a contestable label)
- restoring the "if the notice lists reasons" condition from comment 9(g)-1 in case 5
- citing 12 CFR 1002.9(a)(1)(iii) for case 2
- disclosing the test's limits more fully, including that the final ten were chosen from the first draw and that cases 3 and 5 did not repeat on the rerun

# Interpretive seams in 12 CFR 1002.9(b)(2)

These are points where a careful reviewer with the rule and commentary in hand could hesitate. Each seam names the provisions that create the tension. All citations point to files in `sources/`.

## S1. Reason-selection method for scoring systems
- Comment 9(b)(2)-5 says no single method is required, describes two average-score methods (applicants at or slightly above the cutoff; all applicants), and accepts "any other method that produces results substantially similar."
- Tension: methods used in practice (maximum-points gaps, SHAP, global importance) are not named. Some reduce exactly to an approved method, some are an empirical question, and some cannot be applicant-specific at all.
- The comment also says the averages "could be calculated during the development or use of the system," which answers the stale-benchmark worry.

## S2. Combined scoring and judgmental systems, including the gray band
- Comment 9(b)(2)-7: reasons come from the component the applicant failed. Passing the score and failing judgmental review means judgmental reasons only. Falling in a gray band and then failing judgmental review means reasons from both components.
- Tension: the final human decision looks like the "real" reason; over-inclusive notices that add scorecard factors look harmless; the comment's own reference to "a combined total of four reasons" reads like a cap.

## S3. Automatic-denial factors
- Comment 9(b)(2)-8: when the denial is because of an automatic-denial factor, that specific factor must be disclosed. Appendix C, para. 4: checking the closest listed reason does not satisfy the requirement.
- Tension: a knockout factor overlaps a broader checklist item (bankruptcy versus delinquency); a score computed after a knockout looks like an omitted principal reason; a prior bad history with the creditor may be a knockout or merely a scored input.

## S4. ECOA reasons versus FCRA credit-score key factors
- Comment 9(b)(2)-9: disclosing that a report was used, or disclosing the FCRA key factors, does not satisfy the ECOA reasons requirement.
- Rule text: "failed to achieve a qualifying score on the creditor's credit scoring system" is insufficient.
- Tension: a lender whose only criterion is a bureau score. Saying "score too low" fails, but listing the factors that lowered the score as the ECOA reasons is a different act from relying on the FCRA disclosure. Models tend to over-read comment 9(b)(2)-9 in both directions.

## S5. Number of reasons
- Comment 9(b)(2)-1: no number is mandated; "more than four reasons is not likely to be helpful" is guidance, not a prohibition.
- Comment 9(b)(2)-4: no factor that was a principal reason may be excluded.
- Tension: six reasons can comply; one reason can violate when several shortfalls are of similar size.

## S6. Accurate description of factors actually scored (engineered ML features)
- Comment 9(b)(2)-2: reasons must relate to and accurately describe the factors actually considered or scored. Appendix C, para. 4: no closest-checklist-item substitution.
- Tension: engineered features (balance slopes, averaged utilization, stated-versus-estimated income) map imperfectly to Form C-1 checklist items. Some mappings are accurate descriptions that need not explain the computation (comment 9(b)(2)-3); others name a factor the model never used.

## S7. Counterintuitive scored factors
- Comment 9(b)(2)-4: the creditor must disclose the actual reason (for example, "age of automobile") even if its relationship to creditworthiness may not be clear to the applicant.
- Tension: odd but validated factors invite fair-lending commentary that is outside 9(b)(2); a friendlier proxy (collateral) may or may not describe the scored factor depending on what was measured.

## S8. Description without explaining how or why
- Comment 9(b)(2)-3: "length of residence" is enough; the creditor need not say "too short."
- Tension: the comment permits omitting direction and magnitude, not the identity of the factor. "Credit history" names no factor; comment 9(b)(2)-9's example requires "delinquent credit obligations."

## S9. The bar on "internal standards or policies" versus sample-form language
- Rule text: statements that the action was based on internal standards or policies are insufficient.
- Appendix C, para. 5 and Form C-2: "Your Income: is below our minimum requirement" is sample-form language whose proper use satisfies the requirement.
- Comment 2(c)(2)(v)-1: denial because the creditor does not offer the terms requested is adverse action, so the creditor needs a reason, which will usually be a policy limit.
- Tension: a reason that names the specific factor and the creditor's threshold is not the same as a bare reference to policy. Note: the current Form C-1 no longer contains "We do not grant credit to any applicant on the terms and conditions you request," so no case relies on it.

## S10. Incomplete applications
- Comment 9(a)(1)-3: if the applicant omits information it can provide and the creditor lacks sufficient data for a decision, the creditor may deny and give incompleteness as the reason.
- Comment 9(a)(1)-4: if the creditor has enough data to decide and denies, "incomplete application" cannot be the reason.
- Tension: whether the missing item was needed for the decision or only for later verification.

## S11. Boundary of adverse action (1002.2(c))
- 1002.2(c)(1)(i): a counteroffer that the applicant uses or expressly accepts is not adverse action.
- 1002.2(c)(1)(ii) and comment 2(c)(1)(ii)-2: an unfavorable change is adverse action unless it affects all or substantially all of a class; terminating only low-limit accounts is adverse action.
- 1002.2(c)(2)(v) and comment 2(c)(2)(v)-1: not offering a type of credit is excluded; not offering the terms requested is not.
- Tension: whether any 9(b)(2) statement was owed at all, and if so whether the creditor's wording invoked the wrong exclusion.

## S12. Reasons given on request
- 1002.9(a)(2)(ii) lets the creditor disclose a right to a "statement of specific reasons" instead of giving reasons up front. Comment 9(b)(2)-2 applies to reasons disclosed under 1002.9(a)(2) and (b)(2).
- Tension: 1002.9(b)(2) refers to the statement "required by paragraph (a)(2)(i)," so a reader of that paragraph alone may think specificity does not reach reasons given on request.

## S13. Alternative notice paths (added for the supplementary candidates)
- 1002.9(a)(2)(ii) lets a creditor disclose the right to a statement of reasons instead of the reasons. 1002.9(a)(3)(i) sets the business-credit rules for applicants with revenues of $1 million or less. 1002.9(d) lets a creditor with 150 or fewer applications in the preceding calendar year give oral notice.
- Tension: a notice that gives no written reasons can still comply if the creditor qualifies for one of these paths, so the absence of reasons is not itself a 9(b)(2) failure.

## S14. Counteroffers and notices for several creditors (added for the supplementary candidates)
- 1002.2(c)(1)(i): a counteroffer that the applicant uses or expressly accepts is not adverse action. 1002.9(a)(1)(iv) and comment 9(a)(1)-6 govern a combined counteroffer and adverse action notice.
- 1002.9(g) and comment 9(g)-1: one notice may cover several creditors, but it must show which reasons belong to which creditor.
- Tension: whether a notice was owed turns on what the applicant did with the counteroffer, and a combined notice can be sufficient only if it attributes each reason correctly.

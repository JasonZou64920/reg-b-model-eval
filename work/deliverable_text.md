# Deliverable text (source for the .docx; typography is applied by scripts/build_docx.py)

Jason Zou | Work Sample, Rules Track | Regulation B, 12 CFR 1002.9(b)(2) | jzou1@uchicago.edu

## Method

I wrote 59 candidate cases with AI help, mostly around the official commentary and the edges of “adverse action,” and had separate model sessions check every label against the regulation and commentary, one of them labeling each case blind. I had no API keys, so on October 31, 2026 I stress-tested all 59 on three Anthropic models run as agent sessions (claude-fable-5-1, claude-opus-5-5 and claude-sonnet-5-5), giving each only the task prompt, the case and 12 CFR 1002.9(b)(2). A case made the cut only if at least one model got the label, or the deciding fact, wrong on its first try.

## Ten cases, clearest first

**1. Score-only screen** (Violates)

Oakmont Bank screens personal-loan applications in two stages, and any applicant whose bureau credit score is below 640 is declined at the first stage before income or any other information is reviewed. An applicant scored 612, and the reasons section of the notice states 'Credit score below our minimum requirement,' followed by the FCRA credit score disclosure listing four key factors that adversely affected the score.

> Because the score alone decided, “below our minimum requirement” only says the applicant missed Oakmont’s qualifying score, which the rule calls insufficient, and the FCRA key factors do not meet the separate ECOA duty.
> (12 CFR 1002.9(b)(2); comment 9(b)(2)-9)

**2. Closing a cured account** (Violates)

Northgate's account-management model closed a credit card account in June. The cardholder had been 60 days past due in January, brought the account current in February, and has paid on time every month since. Northgate sent no notice of the closure.

> The account was current when Northgate closed it, so the delinquency exception does not apply, the closure is adverse action, and Northgate generally owed a notice but sent none.
> (12 CFR 1002.2(c)(1)(ii); 12 CFR 1002.2(c)(2)(ii); comment 2(c)(2)(ii)-2; 12 CFR 1002.9(a)(1)(iii))

**3. Blank income field** (Complies)

Meridian's personal-loan model cannot produce a score without stated annual income. An applicant left the income field blank, Meridian made no decision on the merits, and within 30 days it sent an adverse action notice listing 'Credit application incomplete.'

> Meridian’s model could not score the application without the income the applicant left blank, so Meridian could deny for incompleteness instead of first sending a notice of incompleteness.
> (12 CFR 1002.9(c)(1); comment 9(a)(1)-3)

**4. Missing pay stubs** (Depends)

Meridian's personal-loan application asks for two recent pay stubs. An applicant did not upload them, Meridian declined the application, and the notice lists 'Credit application incomplete.'

> It depends on whether Meridian needed the pay stubs to decide at all.
> If it did, the notice complies, because “incomplete” is a proper reason when a creditor cannot decide.
> If it could decide without them, the notice violates, because Meridian owed specific reasons or notice of the right to them.
> (12 CFR 1002.9(a)(2); comment 9(a)(1)-3; comment 9(a)(1)-4)

**5. One notice, three banks** (Violates)

An auto dealer's financing platform sent a buyer's credit application to three banks. Bank A declined because of the buyer's obligations relative to income, Banks B and C declined because of limited credit experience, and the buyer paid cash. The platform sent one adverse action notice on behalf of all three banks that gives each bank's name and address and lists two reasons: 'Excessive obligations in relation to income' and 'Limited credit experience.'

> A notice sent for several creditors that lists reasons has to show which reasons belong to which creditor, and this one does not tie either reason to a bank.
> (12 CFR 1002.9(g); comment 9(g)-1)

**6. Gray-band decline** (Violates)

Harbor Auto Finance approves auto loans automatically at scores of 700 and above, declines automatically below 620, and sends scores from 620 to 699 to an underwriter. An applicant scored 655, with the largest scorecard shortfalls on revolving utilization and recent inquiries, and the underwriter declined after seeing that the applicant had changed jobs two months earlier. The notice lists one reason: 'Length of employment.'

> When a gray-band application is denied after an underwriter’s review, the reasons must come from both the scorecard and the underwriter, but this notice gives only the underwriter’s.
> (12 CFR 1002.9(b)(2); comment 9(b)(2)-7)

**7. Closure over a delinquency** (Depends)

Northgate's account-management model flagged a credit card account for closure because of a 60-day delinquency on that account. Northgate closed the account and mailed the cardholder a letter saying it was closed 'under our account-management policy.'

> It depends on whether the account was still delinquent or in default when Northgate closed it.
> If it was, the letter complies, because closing a delinquent account is not adverse action.
> If not, the letter violates, because the closure is generally adverse action and “account-management policy” is not a specific reason.
> (12 CFR 1002.2(c)(2)(ii); comment 2(c)(2)(ii)-2; 12 CFR 1002.9(b)(2))

**8. Cardholder moves away** (Depends)

Northgate offers its credit card only to residents of Ohio, Indiana and Michigan. A cardholder moved to Arizona, and Northgate closed the account for that reason and mailed a letter saying it was closed 'in accordance with our account policies.'

> It depends on whether the card agreement explicitly provided for closure if the cardholder left the service area.
> If it did, the letter complies, because the closure is not adverse action.
> If not, the letter violates, because the closure is adverse action and “our account policies” is not a specific reason.
> (12 CFR 1002.2(c)(1)(ii); comment 2(c)(1)(ii)-1; 12 CFR 1002.9(b)(2))

**9. Old charge-off** (Depends)

An applicant to Pinecrest Card Services previously held a Pinecrest card that was charged off in 2023, and Pinecrest's scorecard has no characteristic for prior Pinecrest accounts. The new application scored below the cutoff, and the notice lists the four scorecard characteristics with the largest shortfalls.

> It depends on whether the 2023 charge-off was also a reason for the decline, for example through an automatic-denial rule.
> If the score alone decided, the notice complies, because its reasons must relate only to factors the scorecard actually scored.
> If the charge-off was a reason, the notice violates, because Pinecrest had to name it.
> (12 CFR 1002.9(b)(2); comment 9(b)(2)-4; comment 9(b)(2)-8)

**10. Two income figures** (Depends)

Fairway Lending's personal-loan model takes both the applicant's stated income and a bureau-derived income estimate as inputs. An applicant stated $85,000 against an estimate of $52,000, the application was declined, and the notice lists 'Income stated on application inconsistent with income estimated from credit report.'

> It depends on whether a scored gap between stated and estimated income drove the decline.
> If it did, the notice complies, because it accurately describes the factor actually scored.
> If something else drove it, such as the $52,000 estimate feeding a payment-to-income ratio, the notice violates, because it names the wrong factor.
> (12 CFR 1002.9(b)(2); comment 9(b)(2)-2)

## How the models did

| Case | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Missed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Fable (claude-fable-5-1) |   |   |   | X |   | X | X | X | X | X | 6 of 10 |
| Opus (claude-opus-5-5) |   | X |   | X |   | X | X | X | X |   | 6 of 10 |
| Sonnet (claude-sonnet-5-5) | X | X | X | X | X | X | X | X | X | X | 10 of 10 |
| Rerun, same prompt | 1 | 2 | 0 | 3 | 0 | 2 | 3 | 3 | 3 | 3 | 20 of 30 |
| With related rules added | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 | 2 | 8 of 30 |

All runs were on October 31, 2026. An X marks a first-try miss on the draw I picked the ten from. The last two rows count models that missed on a rerun of the same prompt, and with the rest of 1002.9, the definition of adverse action, their commentary and Appendix C added.

The harness, prompts, raw replies and scores come with this sample (harness/README.md explains how to rerun them), and scripts/verify_deliverable.py checks that every cited provision exists in the saved regulation text.

## What I noticed

On the five depends cases, 14 of 15 first-try answers picked a side, usually “complies,” without saying what fact was missing. That partly reflects how I chose them: on the seven depends candidates I left out, the models answered “depends” 14 of 21 times.

The models also leaned toward calling notices compliant. Across all 59 candidates, 26 of the 39 wrong labels were “complies,” and only 2 of the 24 compliant candidates drew any miss. I set one of those aside as debatable, so only one compliant case is here.

Most misses came from rules the models were not shown. With the related rules added, misses on these ten fell from 22 of 30 (20 on a rerun) to 8, and six cases drew none. Case 9 was missed by every model every time.

## Limits

All three models come from one provider, and the model IDs are the ones each session reported. I wrote 29 of the 59 candidates, including eight of these ten, after seeing early results. Each run was a single draw, some sessions answered up to five cases in one prompt, and I could not set temperature. Cases 3 and 5 are the weakest, each missed only once, by Sonnet.

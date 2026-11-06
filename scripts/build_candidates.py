"""Write work/candidates.json (gold) and work/blind/case_facts.json (facts only, for blind review and the model panel)."""
import json, os

C = []
def add(seam, facts, gold, reasoning, citation, why_hard, deciding_fact=None):
    C.append(dict(id=f"C{len(C)+1:02d}", seam=seam, facts=facts, gold_label=gold,
                  reasoning=reasoning, citation=citation,
                  deciding_fact=deciding_fact, why_hard=why_hard))

# S1 reason-selection method
add("S1 reason-selection method",
    "Summit Lending makes unsecured personal loans and decides them with a gradient-boosted tree model. Its adverse action notices list four reasons, which are the four features with the highest global importance in the model's validation report: 'Proportion of balances to credit limits,' 'Number of recent inquiries,' 'Length of credit history,' and 'Delinquent past or present credit obligations with others.' The same four reasons appear on every declined applicant's notice.",
    "violates",
    "Global importance ranks features across the whole portfolio rather than where this applicant fell short, so the notice does not state this applicant's principal reasons and the method is not substantially similar to either average-score method in comment 9(b)(2)-5.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-2, 9(b)(2)-5",
    "The reasons are real scored factors and comment 9(b)(2)-5 says no single method is required, which invites a 'complies' label.")
add("S1 reason-selection method",
    "Lakeview Credit Union decides auto loans with a points-based scorecard. For each declined applicant it ranks characteristics by how far the applicant's points fall below the average points on that characteristic among applicants who scored at or slightly above the cutoff, and the notice lists the top four. Those averages were computed when the scorecard was built in 2021 and have not been recalculated.",
    "complies",
    "This is the first method described in comment 9(b)(2)-5, which allows the average scores to be calculated during development of the system, so the age of the averages does not defeat compliance.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-5",
    "Five-year-old benchmark averages look like a model-risk defect, pulling models toward 'depends' or 'violates'.")
add("S1 reason-selection method",
    "Ridgeway Bank decides credit card applications with a points-based scorecard. Its reason logic ranks characteristics by how far the applicant's points fall below the maximum points available on each characteristic, and the notice lists the four largest gaps.",
    "depends",
    "Comment 9(b)(2)-5 approves two average-score methods and any other method that produces substantially similar results, so a maximum-points method is acceptable only if its output matches theirs.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-5",
    "Maximum-points ranking is intuitive and common, so models either approve it outright or reject it as unlisted instead of treating it as an empirical question.",
    "Whether, for the bank's applicant population, the maximum-points ranking produces substantially the same reasons as one of the two average-score methods: if it does, the notice complies; if the rankings materially diverge, it violates.")
add("S1 reason-selection method",
    "Brightline Finance decides credit card applications with a generalized additive model, so each feature contributes its own separate score component. The notice lists the four features with the most negative SHAP values, computed against a background sample of all applicants from the model's development period.",
    "complies",
    "In an additive model, a SHAP value computed against an all-applicant background equals the applicant's score on that feature minus the all-applicant average score on it, which is the second method in comment 9(b)(2)-5.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-5",
    "SHAP is not named in the commentary, so models tend to call it unapproved or 'depends' without checking that it reduces exactly to an approved method here.")

# S2 combined scoring and judgmental
add("S2 combined system / gray band",
    "Harbor Auto Finance approves auto loans automatically at scores of 700 and above, declines automatically below 620, and sends scores from 620 to 699 to an underwriter. An applicant scored 655, and the underwriter declined after seeing that the applicant had changed jobs two months earlier. The notice lists one reason: 'Length of employment.'",
    "violates",
    "A gray-band application declined after judgmental review must receive reasons from both the scoring and the judgmental components, and this notice gives only the underwriter's reason.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-7",
    "The underwriter made the final call, so the single judgmental reason looks like the complete explanation.")
add("S2 combined system / gray band",
    "Harbor Auto Finance sends every auto loan over $40,000 to an underwriter regardless of score. An applicant for $48,000 scored 742, above the 700 approval line, and the underwriter declined because the applicant's self-employment income could not be verified. The notice lists 'Unable to verify income' followed by the two scorecard characteristics on which the applicant scored lowest, 'Number of recent inquiries' and 'Length of credit history.'",
    "violates",
    "The application passed the scoring stage and was denied on judgmental review, so the reasons must relate to the factors the underwriter reviewed, and listing scorecard characteristics that did not cause the denial misstates the principal reasons.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-2, 9(b)(2)-7",
    "The correct reason is present and the extra reasons are real scored factors, so the notice looks over-inclusive rather than inaccurate.")
add("S2 combined system / gray band",
    "For Harbor's gray-band auto applications (scores 620 to 699), the decision engine returns the four scorecard characteristics with the largest shortfalls plus the underwriter's reason, 'Unable to verify income.' Because Harbor's notice template has four reason lines, the notice for a gray-band decline lists the four scorecard reasons and omits the underwriter's reason.",
    "violates",
    "Reasons for a gray-band denial must come from both components, and the statement that more than four combined reasons is 'not likely to be helpful' is guidance, not a cap that permits dropping the judgmental reason.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-1, 9(b)(2)-7",
    "Comment 9(b)(2)-7 itself mentions a combined total of four reasons, which reads like a ceiling that justifies the template.")

# S3 automatic denial
add("S3 automatic denial",
    "Pinecrest Card Services' decision engine declines any applicant with a bankruptcy discharged in the past 24 months before a score is computed. An applicant was declined under that rule, and the notice checks 'Delinquent past or present credit obligations with others.'",
    "violates",
    "When a creditor denies because of an automatic-denial factor it must disclose that specific factor, here bankruptcy, and checking the closest listed reason does not satisfy the notice requirement.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-8; appendix C, para. 4",
    "A bankruptcy usually involves delinquent obligations, so the checked reason seems substantively true.")
add("S3 automatic denial",
    "Pinecrest's engine applies knockout rules first, and an applicant with a vehicle repossession in the past 12 months is declined at that step. The engine still computes a score for portfolio monitoring, and this applicant's score was below the cutoff. The notice lists one reason: 'Foreclosure or repossession.'",
    "complies",
    "The denial rested on the automatic-denial factor, which the notice discloses, and the monitoring score played no part in the decision, so it supplies no principal reason that had to be listed.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-2, 9(b)(2)-8",
    "A failing score in the file looks like an omitted principal reason under comment 9(b)(2)-4.")
add("S3 automatic denial",
    "An applicant to Pinecrest previously held a Pinecrest card that was charged off in 2023. The new application scored below the cutoff, and the notice lists the four scorecard characteristics with the largest shortfalls, none of which refers to the prior Pinecrest account.",
    "depends",
    "An automatic-denial factor that causes the denial must be disclosed, while a scored factor must be disclosed only if it was a principal reason.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-4, 9(b)(2)-8",
    "Comment 9(b)(2)-8 uses prior bad history with the same creditor as its example, so models assume the factor must appear.",
    "Whether Pinecrest's engine treats a prior charge-off with Pinecrest as an automatic-denial factor (the notice violates by omitting it) or only as one scored characteristic that did not rank among the largest shortfalls (the notice complies).")

# S4 ECOA vs FCRA
add("S4 ECOA reasons vs FCRA key factors",
    "Oakmont Bank's only underwriting criterion for its unsecured credit card is a minimum bureau credit score of 640. An applicant scored 612, and the reasons section of the notice states 'Credit score below our minimum requirement,' followed by the FCRA credit score disclosure listing four key factors that adversely affected the score.",
    "violates",
    "A statement that the applicant did not reach a qualifying score is insufficient under 12 CFR 1002.9(b)(2), and disclosing the FCRA key factors does not satisfy the ECOA reasons requirement.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-9",
    "The notice as a whole tells the applicant what lowered the score, so the defect looks like formatting rather than substance.")
add("S4 ECOA reasons vs FCRA key factors",
    "Oakmont Bank's only underwriting criterion for its unsecured credit card is a minimum bureau credit score of 640. For an applicant who scored 612, the reasons section of the notice lists the four key factors returned with the score, worded as reasons for the denial (for example, 'Delinquent past or present credit obligations with others'), and the FCRA section repeats them as key factors.",
    "complies",
    "Because the score was the sole basis for denial, the factors that lowered it are the factors actually scored and the principal reasons, and stating them in the ECOA reasons section is a disclosure of specific reasons rather than reliance on the FCRA key-factor disclosure.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-4, 9(b)(2)-9",
    "Comment 9(b)(2)-9 says key factors do not satisfy ECOA, which models over-read as a bar on ever giving the same factors as ECOA reasons.")

# S5 number of reasons
add("S5 number of reasons",
    "Westfield Bank decides personal loans with a points-based scorecard and selects reasons by comparing the applicant's points with the average for applicants at or slightly above the cutoff. A declined applicant's notice lists six reasons in rank order, each a characteristic on which the applicant fell well below that average.",
    "complies",
    "No number of reasons is mandated and more than four is described only as 'not likely to be helpful,' so six accurate principal reasons comply.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-1",
    "The four-reason line in the commentary and the FCRA four-key-factor limit are often remembered as a hard cap.")
add("S5 number of reasons",
    "Westfield's reason logic for a declined personal-loan applicant shows four characteristics with point shortfalls of 22, 21, 19, and 18 points, and no other characteristic with a shortfall above 6. Westfield's notice policy is to disclose only the largest shortfall, so the notice lists one reason: 'Proportion of balances to credit limits.'",
    "violates",
    "Four characteristics with nearly equal shortfalls are each principal reasons, and a creditor using a scoring system may not exclude a principal reason from the notice.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-1, 9(b)(2)-4",
    "The rule says 'reason(s)' and the commentary mandates no number, so a one-reason policy looks permissible.")

# S6 accurate description of engineered features
add("S6 accurate description / engineered features",
    "Arcadia Card's gradient-boosted model has no income or debt-to-income input. Its largest negative feature for one declined applicant is the 24-month slope of total revolving balances, and the notice maps that feature to the checklist reason 'Excessive obligations in relation to income.'",
    "violates",
    "The reason must accurately describe a factor actually scored, and a reason about income misdescribes a balance-trend feature in a model that never considers income, which is the closest-checklist-item substitution appendix C says does not satisfy the requirement.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-2; appendix C, para. 4",
    "Mapping engineered features to the nearest sample-form reason is common practice, and rising balances do sound like excessive obligations.")
add("S6 accurate description / engineered features",
    "Arcadia's model includes a feature equal to the applicant's revolving utilization (balances divided by limits) averaged over the past 24 months of bureau history. For an applicant whose largest negative feature is that average, the notice states 'Proportion of balances to credit limits on revolving accounts.'",
    "complies",
    "The stated reason accurately describes the factor scored, and the creditor need not explain how the factor was computed or why it hurt the applicant.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-2, 9(b)(2)-3",
    "The notice omits the 24-month averaging, so models may demand the engineered feature's full definition.")
add("S6 accurate description / engineered features",
    "Fairway Lending's personal-loan model takes both the applicant's stated income and a bureau-derived income estimate as inputs. An applicant stated $85,000 and the estimate was $52,000; the application was declined, and the notice lists 'Unable to verify income.'",
    "depends",
    "The reason must accurately describe the factor actually scored, and the same income data can feed different factors.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-2; appendix C, para. 4",
    "'Unable to verify income' sounds like a fair summary of a large discrepancy whichever way the model used it.",
    "How the model used the two figures: if the scored variable is the gap between stated and estimated income, 'Unable to verify income' describes it and the notice complies; if the model put the $52,000 estimate into a payment-to-income ratio that drove the denial, the factor is income relative to the payment and the notice violates.")

# S7 counterintuitive scored factors
add("S7 counterintuitive scored factor",
    "Velo Auto Credit's validated auto-loan model includes a feature indicating whether the applicant's mobile number is a prepaid line. For one declined applicant this was the largest negative contribution, and the notice lists 'Type of mobile phone account' as the first of three reasons.",
    "complies",
    "A creditor must disclose the actual scored factor even when its relationship to creditworthiness may not be clear to the applicant, and this notice does so.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-4",
    "The factor looks like alternative data that may raise fairness concerns, so models fold issues outside 9(b)(2) into the label.")
add("S7 counterintuitive scored factor",
    "Granite Credit Union's auto-loan scorecard includes a characteristic for vehicle model year, and for one declined applicant it produced the largest shortfall. The notice lists 'Age of collateral' as the principal reason.",
    "depends",
    "The reason must accurately describe the factor actually scored, and 'Age of collateral' describes a model-year characteristic only if the vehicle measured is the collateral.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-2, 9(b)(2)-4",
    "In an auto loan, vehicle age reads naturally as a collateral attribute, so models accept the reason without asking which vehicle was scored.",
    "Which vehicle the characteristic measures: if it is the vehicle being financed and pledged as collateral, the reason is accurate and the notice complies; if it is a vehicle the applicant already owns that does not secure the loan, the scored factor is the age of the applicant's automobile, not the collateral, and the notice violates.")

# S8 how or why
add("S8 description without how or why",
    "Brookline Bank's personal-loan scorecard produced its largest shortfall for a declined applicant on the characteristic 'number of 60-day or worse delinquencies in the past 24 months.' The notice lists one reason: 'Credit history.'",
    "violates",
    "A creditor may omit how or why a factor hurt the applicant but must still identify the factor, and the commentary's own example requires disclosing delinquent credit obligations rather than a general reference to credit history.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-3, 9(b)(2)-9",
    "Comment 9(b)(2)-3 permits terse labels like 'length of residence,' so 'credit history' looks like an equally acceptable short label.")

# S9 internal standards bar vs sample-form language
add("S9 internal standards bar vs sample-form language",
    "Cedar Finance underwrites personal loans judgmentally and requires verified annual income of at least $30,000. An applicant verified $24,000, and Cedar's notice, built on the Form C-2 checklist, marks 'Your Income: is below our minimum requirement.'",
    "complies",
    "The reason identifies the specific factor that caused the denial, income, in language taken from sample Form C-2, whose proper use satisfies the specific-reasons requirement.",
    "12 CFR 1002.9(b)(2); appendix C, para. 5; Form C-2",
    "'Below our minimum requirement' sounds like the 'internal standards or policies' statement the rule calls insufficient.")
add("S9 internal standards bar vs sample-form language",
    "Granite Credit Union finances used vehicles for no more than 72 months when the vehicle is more than five years old. An applicant requested an 84-month loan on a seven-year-old truck and was declined with a notice stating: 'The requested term of 84 months exceeds the 72-month maximum we offer for vehicles more than five years old.'",
    "complies",
    "The notice names the specific term and collateral characteristic that caused the denial instead of citing an unidentified internal standard or policy, which is what 12 CFR 1002.9(b)(2) treats as insufficient.",
    "12 CFR 1002.9(b)(2); comment 2(c)(2)(v)-1",
    "The reason is literally a policy limit, so the rule's bar on 'internal standards or policies' seems to apply on its face.")

# S10 incomplete applications
add("S10 incomplete applications",
    "Meridian Bank asks personal-loan applicants to upload two recent pay stubs. An applicant never uploaded them; Meridian's model scored the application on bureau data and stated income, the score fell below the cutoff, and the notice lists 'Credit application incomplete.'",
    "violates",
    "When the creditor has enough information to make a credit decision and denies on that basis, it must give the specific reasons for the denial and may not cite missing information or an incomplete application.",
    "12 CFR 1002.9(b)(2); comment 9(a)(1)-4",
    "The application really was missing documents, and 'Credit application incomplete' is a Form C-1 checklist reason.")
add("S10 incomplete applications",
    "Meridian's personal-loan model cannot produce a score without stated annual income. An applicant left the income field blank, Meridian made no decision on the merits, and within 30 days it sent an adverse action notice listing 'Credit application incomplete.'",
    "complies",
    "When the applicant omits information it can provide and the creditor lacks sufficient data for a decision, the creditor may deny and give incompleteness as the reason instead of sending a notice of incompleteness.",
    "12 CFR 1002.9(b)(2); comment 9(a)(1)-3; 12 CFR 1002.9(c)(1)",
    "'Incomplete' looks like a non-reason, and models expect a notice of incompleteness under 1002.9(c) to be mandatory.")
add("S10 incomplete applications",
    "Meridian's personal-loan application asks for two recent pay stubs. An applicant did not upload them, Meridian declined the application, and the notice lists 'Credit application incomplete.'",
    "depends",
    "Incompleteness may be the stated reason only when the creditor lacks sufficient data for a credit decision.",
    "12 CFR 1002.9(b)(2); comments 9(a)(1)-3, 9(a)(1)-4",
    "Models treat any missing document as making the application incomplete without asking whether the decision depended on it.",
    "Whether Meridian could make a credit decision without the pay stubs: if its process requires them before any decision, the reason is permitted and the notice complies; if the model can score without them and the stubs only verify income for approved loans, the notice violates.")

# S11 boundary of adverse action
add("S11 boundary of adverse action",
    "An applicant applied to Northgate Bank for a credit card with a $25,000 limit. Northgate's model approved a $6,000 limit, Northgate mailed the card with a letter stating the limit and giving no reasons, and the applicant activated the card and has used it for three months.",
    "complies",
    "A refusal to grant the amount requested is not adverse action when the creditor counteroffers and the applicant uses the credit offered, so no statement of reasons was required.",
    "12 CFR 1002.2(c)(1)(i); 12 CFR 1002.9(b)(2)",
    "Approving a quarter of the requested limit feels like a partial denial that should carry reasons.")
add("S11 boundary of adverse action",
    "An applicant applied to Northgate Bank for a credit card with a $25,000 limit. Northgate approved a $6,000 limit and mailed the card with a letter stating the limit, with no reasons and no disclosure of a right to reasons. It is now 120 days later and Northgate has sent nothing further.",
    "depends",
    "A counteroffer becomes adverse action requiring a statement of reasons only if the applicant does not use or expressly accept the credit offered.",
    "12 CFR 1002.2(c)(1)(i); 12 CFR 1002.9(a)(1)(iv); 12 CFR 1002.9(b)(2)",
    "Models focus on the size of the cut or the missing reasons and miss that the applicant's response decides whether reasons were ever owed.",
    "Whether the applicant expressly accepted or used the card: if so, there was no adverse action and Northgate complies; if not, the counteroffer is adverse action and Northgate violated by sending no notice with reasons within 90 days.")
add("S11 boundary of adverse action",
    "Northgate's account-management model rescores card accounts monthly. In March, Northgate cut the credit limit by 30 percent on every account with a behavior score below 600, about 8 percent of the portfolio, and the affected cardholders received a letter saying the change was 'part of a portfolio-wide risk management review.'",
    "violates",
    "A limit cut aimed at accounts selected by their own risk scores is not a change affecting all or substantially all of a class of accounts, so it is adverse action and the letter's reference to an internal review is not a specific reason.",
    "12 CFR 1002.2(c)(1)(ii); comment 2(c)(1)(ii)-2; 12 CFR 1002.9(b)(2)",
    "The cut applied uniformly to a defined segment, which resembles the class-wide exception.")
add("S11 boundary of adverse action",
    "Granite Credit Union offers RV loans with terms of up to 10 years. A member applied for a 15-year loan on a used RV and received a notice stating 'We do not offer this product.'",
    "violates",
    "Declining because the creditor does not offer the term requested is adverse action, unlike declining a type of credit the creditor does not offer, and 'We do not offer this product' misstates the specific reason.",
    "12 CFR 1002.2(c)(2)(v); comment 2(c)(2)(v)-1; 12 CFR 1002.9(b)(2)",
    "The notice tracks the exclusion for credit the creditor does not offer, which models accept at face value.")

# S12 reasons given on request
add("S12 reasons given on request",
    "Harbor Auto Finance's decline notices give no reasons but disclose the right to request a statement of reasons within 60 days, with the required contact details. An applicant requested reasons on day 45, and within 30 days Harbor replied in writing: 'Your application did not meet our credit standards.'",
    "violates",
    "The right to request reasons is a right to a statement of specific reasons that must accurately describe the factors considered, and a reference to the creditor's credit standards is not specific.",
    "12 CFR 1002.9(a)(2)(ii); 12 CFR 1002.9(b)(2); comment 9(b)(2)-2",
    "12 CFR 1002.9(b)(2) speaks of the statement 'required by paragraph (a)(2)(i),' so a model reading only that paragraph may think the specificity rule does not reach reasons given on request.")

# Adjudication: C19 (vehicle model year) dropped; its ambiguity was in wording, not law. Replacement appended as C31.
C = [c for c in C if c["id"] != "C19"]
C.append(dict(id="C31", seam="S12 reasons given on request / third-party notices",
    facts="An auto dealer's financing platform submitted an applicant's credit application to three banks, all three declined, and the applicant bought the car with cash. The platform sent one adverse action notice on behalf of all three banks that gives each bank's name and address and lists two reasons: 'Excessive obligations in relation to income' and 'Limited credit experience.'",
    gold_label="violates",
    reasoning="A single notice given for several creditors that states reasons must clearly indicate which reasons relate to which creditor, and this notice pools them.",
    citation="12 CFR 1002.9(g); comment 9(g)-1; 12 CFR 1002.9(b)(2)",
    deciding_fact=None,
    why_hard="Both reasons are specific checklist reasons, so the notice looks compliant with 9(b)(2) unless the reader knows the multi-creditor attribution rule."))
for c in C:
    if c["seam"] == "S12 reasons given on request":
        c["seam"] = "S12 reasons given on request / third-party notices"
# Supplementary complies candidates, added after the first Condition A run produced only one hard complies case.
def supp(cid, seam, facts, reasoning, citation, why_hard):
    C.append(dict(id=cid, seam=seam, facts=facts, gold_label="complies", reasoning=reasoning,
                  citation=citation, deciding_fact=None, why_hard=why_hard, supplementary=True))
supp("C32", "S13 alternative notice paths",
    "Summit Lending's gradient-boosted model scored a personal-loan application below the cutoff. Within 30 days Summit mailed a notice that states the action taken, Summit's name and address, the ECOA notice with its federal regulator's name and address, and the applicant's right to a statement of specific reasons if requested within 60 days, naming the office that will provide it with its address and telephone number. The notice lists no reasons, and the applicant has not asked for them.",
    "A creditor may disclose the applicant's right to a statement of specific reasons instead of giving the reasons, and the specificity requirement applies to the statement once one is given.",
    "12 CFR 1002.9(a)(2)(ii); 12 CFR 1002.9(b)(2)",
    "A notice with no reasons at all looks like the plainest failure of a rule that demands specific reasons.")
supp("C33", "S13 alternative notice paths",
    "Prairie State Bank received 140 credit applications in the preceding calendar year. It declined a consumer's auto-loan application, and two weeks later the loan officer phoned the applicant and said the loan was declined because the applicant's monthly debt payments were too high relative to income. No written notice was sent.",
    "A creditor that received no more than 150 applications in the preceding calendar year satisfies the notice requirements, including the statement of specific reasons, orally, and the reason given is specific.",
    "12 CFR 1002.9(d); 12 CFR 1002.9(b)(2)",
    "The rule's notice requirements read as written requirements, so an oral-only reason looks deficient.")
supp("C34", "S13 alternative notice paths",
    "Oakmont Bank's online application for small-business credit discloses the right to request a statement of reasons within 60 days, with the responsible office's name, address and telephone number, and includes the ECOA notice. A bakery with $600,000 in revenue last year applied for a $50,000 line, Oakmont's model declined it, and a banker phoned the owner to say the line was declined. No written notice or reasons were given, and the owner has not requested them.",
    "For a business with revenues of $1 million or less, the creditor may state the action orally and may give the right-to-reasons disclosure at the time of application, so no statement of reasons was owed unless requested.",
    "12 CFR 1002.9(a)(3)(i)(A); 12 CFR 1002.9(a)(3)(i)(B); 12 CFR 1002.9(b)(2)",
    "A model decline with no written notice and no reasons looks deficient unless the reader knows the small-business notice rules.")
supp("C35", "S14 counteroffer and multi-creditor notices",
    "An applicant asked Northgate Bank for a credit card with a $25,000 limit. Northgate mailed a combined counteroffer and adverse action notice that offered a $6,000 limit, listed 'Excessive obligations in relation to income' and 'Limited credit experience' as the reasons it would not grant $25,000, and included the ECOA notice. The applicant never activated the card, and 120 days later Northgate has sent nothing further.",
    "A creditor that gives a combined counteroffer and adverse action notice that complies with 12 CFR 1002.9(a)(2) need not send a second notice when the applicant does not accept the counteroffer.",
    "comment 9(a)(1)-6; 12 CFR 1002.9(a)(1)(iv); 12 CFR 1002.9(b)(2)",
    "The 90-day counteroffer clock suggests a fresh adverse action notice was due once the offer went unused.")
supp("C36", "S14 counteroffer and multi-creditor notices",
    "An auto dealer submitted a buyer's credit application to four banks through its financing platform. Bank A approved, and the buyer signed a retail installment contract financed by Bank A; Banks B, C and D declined, and none of them sent the buyer an adverse action notice.",
    "When an application goes to several creditors through a third party and the applicant accepts or uses credit offered by one of them, the others need not notify the applicant of their action.",
    "12 CFR 1002.9(g); 12 CFR 1002.9(b)(2)",
    "Three banks declined and none gave reasons, which looks like three missed statements of reasons.")
# Second supplementary round (complies), targeting observed failure modes: over-reading specificity and comment 9(b)(2)-4.
supp("C37", "S3 automatic denial",
    "Pinecrest's decision engine declines, before any score is computed, every applicant who had a Pinecrest account charged off in the past five years. An applicant was declined under that rule, and the notice checks 'Poor credit performance with us.'",
    "The notice discloses the automatic-denial factor itself, the applicant's prior credit history with the creditor, using the sample-form reason that names it.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-8; Form C-1",
    "Models expect a knockout factor to be named in its own terms ('charge-off') and treat the checklist line as a closest-factor substitution.")
supp("C39", "S9 internal standards bar vs sample-form language",
    "Brightline Finance's notice to a declined card applicant reads: 'Your application was processed by a credit scoring system that assigns a numerical value to the various items of information we consider. The information you provided did not score a sufficient number of points for approval. The reasons you did not score well compared with other applicants were: proportion of balances to credit limits; number of recent inquiries; length of credit history.' The three reasons are the applicant's largest shortfalls under Brightline's reason-selection method.",
    "The notice follows sample Form C-3, whose proper use satisfies the requirement, and it states the specific scored factors rather than only that the applicant failed to reach a qualifying score.",
    "12 CFR 1002.9(b)(2); appendix C, para. 5; Form C-3",
    "The notice literally says the applicant did not score enough points, which the rule text calls insufficient.")
supp("C42", "S5 number of reasons",
    "Westfield's reason logic for a declined personal-loan applicant shows point shortfalls of 31 and 27 points on two characteristics and of 4, 3 and 2 points on three others. The notice lists the two characteristics with the large shortfalls.",
    "The rule requires the principal reasons and mandates no number, and the three characteristics with small shortfalls were not principal reasons for the denial.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-1, 9(b)(2)-4",
    "Comment 9(b)(2)-4 says no principal factor may be excluded, which models over-read as requiring every negative factor.")
supp("C44", "S2 combined system / gray band",
    "At Prairie State Bank a loan officer first reviews each auto-loan file and passes acceptable files to a scorecard. An applicant passed the officer's review, although the officer's notes flag a short time at the current address, and the scorecard then declined the application. The notice lists the scorecard's three largest shortfalls and does not mention residence.",
    "In a combined system the reasons come from the component the applicant failed, and the same rule applies when the judgmental component comes first, so the officer's note is not a reason that had to be disclosed.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-7",
    "A negative judgmental note sitting in the file looks like an omitted principal reason.")
# Third supplementary round (complies): stated-fact variant of C17 and a notice that cites "credit policy".
supp("C45", "S6 accurate description / engineered features",
    "Fairway Lending's personal-loan model includes a feature equal to the applicant's stated income divided by a bureau-derived income estimate. An applicant stated $85,000 against an estimate of $52,000, that feature was the largest negative contribution, and the notice lists 'Unable to verify income.'",
    "The scored factor measures whether the stated income is corroborated by an independent estimate, and 'Unable to verify income' accurately describes that factor without having to explain how it was computed.",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-2, 9(b)(2)-3",
    "The model never performs a verification step, so the reason can look like a description of something the lender did not do.")
supp("C46", "S9 internal standards bar vs sample-form language",
    "Cedar Finance underwrites personal loans judgmentally and declines any applicant whose debt payments exceed 45 percent of verified income. An applicant's ratio was 52 percent, and the notice states: 'Your debt-to-income ratio of 52% exceeds the 45% maximum set by our credit policy.'",
    "The notice identifies the specific factor that caused the denial, the applicant's debt relative to income, and the reference to the creditor's policy threshold does not turn that specific reason into a bare statement of internal standards.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-6; Form C-1",
    "The notice says outright that the denial follows 'our credit policy,' which the rule text calls insufficient.")
# Fourth supplementary round: violates/depends cases in the pattern the panel misses (an exception or the
# final decision-maker makes a deficient notice look adequate). Added because the main set had only 9 hard cases.
def supp_vd(cid, seam, facts, gold, reasoning, citation, why_hard, deciding_fact=None):
    C.append(dict(id=cid, seam=seam, facts=facts, gold_label=gold, reasoning=reasoning, citation=citation,
                  deciding_fact=deciding_fact, why_hard=why_hard, supplementary=True))
supp_vd("C47", "S11 boundary of adverse action",
    "Northgate's account-management model closed a credit card account in June. The cardholder had been 60 days past due in January, brought the account current in February, and has paid on time every month since. Northgate sent no notice of the closure.",
    "violates",
    "The exclusion for action taken in connection with delinquency covers an account that is currently delinquent, and closing an account because of a past delinquency is adverse action that requires a notice with specific reasons.",
    "12 CFR 1002.2(c)(2)(ii); comment 2(c)(2)(ii)-2; 12 CFR 1002.9(b)(2)",
    "The regulation excludes action taken in connection with delinquency, which seems to cover a closure prompted by a delinquency.")
supp_vd("C48", "S11 boundary of adverse action",
    "Northgate's account-management model flagged a credit card account for closure because of a 60-day delinquency on that account, and Northgate closed it in June without sending any notice.",
    "depends",
    "Closing an account that is currently delinquent is not adverse action, while closing it because of a past delinquency is adverse action that requires a notice with specific reasons.",
    "12 CFR 1002.2(c)(2)(ii); comment 2(c)(2)(ii)-2; 12 CFR 1002.9(b)(2)",
    "The delinquency exclusion looks dispositive, so models do not ask when the delinquency occurred.",
    "Whether the account was still delinquent when Northgate closed it: if it was, the closure is not adverse action and Northgate complies; if the cardholder had already brought it current, the closure is adverse action and Northgate violated by giving no notice with reasons.")
supp_vd("C49", "S2 combined system / gray band",
    "Harbor Auto Finance approves auto loans automatically at scores of 700 and above, declines automatically below 620, and sends 620 to 699 to an underwriter. An applicant scored 660, and the underwriter declined after finding that the applicant's income could not be verified. The notice lists the four scorecard characteristics with the largest shortfalls.",
    "violates",
    "A gray-band application declined after judgmental review must receive reasons from both components, and this notice omits the underwriter's reason.",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-7",
    "The score is what kept the applicant out of automatic approval, so the scorecard reasons look like a complete explanation.")
# Fifth supplementary round: more cases in the exception-misapplied pattern, each with a distinct scenario.
supp_vd("C50", "S11 boundary of adverse action",
    "A cardholder whose purchase was about to exceed her limit used Northgate's app to request a $2,000 credit limit increase, as the app's procedures allow. Northgate's model declined the request, the app displayed 'Purchase declined: over limit,' and Northgate sent no notice.",
    "violates",
    "A point-of-sale refusal is excluded from adverse action except when it is a denial of an application, made under the creditor's procedures, for an increase in available credit, which this was, so a notice with specific reasons was required.",
    "12 CFR 1002.2(c)(2)(iii); comment 2(c)(2)(iii)-2; 12 CFR 1002.2(c)(1)(iii); 12 CFR 1002.9(b)(2)",
    "The refusal happened at the point of sale and the limit was exceeded, which matches the listed point-of-sale exclusions.")
supp_vd("C51", "S11 boundary of adverse action",
    "Northgate offers its credit card only to residents of Ohio, Indiana and Michigan. A cardholder moved to Arizona, Northgate closed the account for that reason, and it sent no notice.",
    "depends",
    "Terminating an account because the customer moved out of the card issuer's service area is adverse action unless the credit agreement explicitly provided for termination on that ground.",
    "12 CFR 1002.2(c)(1)(ii); comment 2(c)(1)(ii)-1; 12 CFR 1002.9(b)(2)",
    "A closure for moving out of the service area has nothing to do with creditworthiness, so it looks outside the notice rules altogether.",
    "Whether the card agreement explicitly provided for termination if the cardholder moved out of the service area: if it did, the closure is not adverse action and Northgate complies; if it did not, the closure is adverse action and Northgate violated by giving no notice with reasons.")
supp_vd("C52", "S11 boundary of adverse action",
    "A borrower with an existing auto loan at Lakeview Credit Union applied, using Lakeview's online modification request form, to extend the loan's remaining term from 24 to 48 months. Lakeview's model declined the request, and Lakeview told the borrower by email that 'loan modifications are handled at our discretion and your request was not approved.'",
    "violates",
    "A refusal to refinance or extend the term of a loan is adverse action when the applicant applied under the creditor's procedures, and an email citing the creditor's discretion gives no specific reason.",
    "12 CFR 1002.2(c)(1)(i); comment 2(c)(1)(i)-1; 12 CFR 1002.9(b)(2)",
    "A modification of an existing loan looks like account servicing rather than a credit application.")
# Audit-council revisions (round 6). Each revises a selected case to remove a second unstated fact, put the
# violation on 9(b)(2) itself, or tighten wording. New ids keep the tested history intact.
def rev(cid, revises, seam, facts, gold, reasoning, citation, why_hard, deciding_fact=None):
    C.append(dict(id=cid, revises=revises, seam=seam, facts=facts, gold_label=gold, reasoning=reasoning,
                  citation=citation, deciding_fact=deciding_fact, why_hard=why_hard, supplementary=True))
rev("C53", "C11", "S4 ECOA reasons vs FCRA key factors",
    "Oakmont Bank screens personal-loan applications in two stages, and any applicant whose bureau credit score is below 640 is declined at the first stage before income or any other information is reviewed. An applicant scored 612, and the reasons section of the notice states 'Credit score below our minimum requirement,' followed by the FCRA credit score disclosure listing four key factors that adversely affected the score.",
    "violates",
    "Because the bureau score was the only basis for the decline, it served as Oakmont's credit scoring system, so the stated reason only says the applicant failed to achieve a qualifying score, which 12 CFR 1002.9(b)(2) calls insufficient, and the FCRA key factors do not supply the ECOA reasons (comment 9(b)(2)-9).",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-9",
    "The notice as a whole tells the applicant what lowered the score, and a bureau score can look like something other than the creditor's own scoring system.")
rev("C54", "C24", "S10 incomplete applications",
    "Meridian Bank's personal-loan model cannot produce a score without stated annual income. An applicant submitted an application with the income field blank, and within 30 days Meridian sent an adverse action notice listing 'Credit application incomplete.'",
    "complies",
    "Because Meridian's model could not score the application without the income the applicant could have provided, Meridian lacked sufficient data for a credit decision and could deny with incompleteness as the reason instead of sending a notice of incompleteness (12 CFR 1002.9(c)(1); comment 9(a)(1)-3).",
    "12 CFR 1002.9(c)(1); comment 9(a)(1)-3",
    "'Credit application incomplete' looks like a non-reason, and models expect a notice of incompleteness to be mandatory.")
rev("C55", "C05", "S2 combined system / gray band",
    "Harbor Auto Finance approves auto loans automatically at scores of 700 and above, declines automatically below 620, and sends scores from 620 to 699 to an underwriter. An applicant scored 655, with the largest scorecard shortfalls on revolving utilization and recent inquiries, and the underwriter declined after seeing that the applicant had changed jobs two months earlier. The notice lists one reason: 'Length of employment.'",
    "violates",
    "When an application in the gray band is denied after judgmental review, the reasons disclosed must come from both the scoring and the judgmental components, and this notice gives only the underwriter's reason (comment 9(b)(2)-7).",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-7",
    "The underwriter made the final call, so the single judgmental reason looks like the complete explanation.")
rev("C56", "C10", "S3 automatic denial",
    "An applicant to Pinecrest Card Services previously held a Pinecrest card that was charged off in 2023, and Pinecrest's scorecard has no characteristic for prior Pinecrest accounts. The new application scored below the cutoff, and the notice lists the four scorecard characteristics with the largest shortfalls.",
    "depends",
    "A creditor that denies because of an automatic-denial factor must disclose that specific factor, while a factor that played no part in the decision need not be disclosed (comment 9(b)(2)-8).",
    "12 CFR 1002.9(b)(2); comments 9(b)(2)-4 and 9(b)(2)-8",
    "Prior bad history with the same creditor is the commentary's own automatic-denial example, so models either demand it or ignore it without asking whether a knockout rule fired.",
    "Whether a Pinecrest automatic-denial rule declined this application because of the 2023 charge-off: if one did, the notice violates by omitting that factor; if none did, the charge-off played no part in the decision and the notice complies.")
rev("C57", "C31", "S12 reasons given on request / third-party notices",
    "An auto dealer's financing platform sent a buyer's credit application to three banks. Bank A declined because of the buyer's obligations relative to income, Banks B and C declined because of limited credit experience, and the buyer paid cash. The platform sent one adverse action notice on behalf of all three banks that gives each bank's name and address and lists two reasons: 'Excessive obligations in relation to income' and 'Limited credit experience.'",
    "violates",
    "A single notice that gives reasons on behalf of several creditors must clearly indicate which reasons relate to which creditor, and this notice lists both reasons without attributing them to any bank (12 CFR 1002.9(g); comment 9(g)-1).",
    "12 CFR 1002.9(g); comment 9(g)-1; 12 CFR 1002.9(b)(2)",
    "Both reasons are specific and accurate, so the notice looks compliant unless the reader knows the attribution rule for multi-creditor notices.")
rev("C58", "C17", "S6 accurate description / engineered features",
    "Fairway Lending's personal-loan model takes both the applicant's stated income and a bureau-derived income estimate as inputs. An applicant stated $85,000 against an estimate of $52,000, the application was declined, and the notice lists 'Income stated on application inconsistent with income estimated from credit report.'",
    "depends",
    "The stated reason must accurately describe the factor actually scored, and the same two income figures can feed different factors (comment 9(b)(2)-2).",
    "12 CFR 1002.9(b)(2); comment 9(b)(2)-2",
    "The reason is specific and matches the data, so models accept it without asking which factor the model actually scored.",
    "How the model used the two figures: if the decline turned on a scored gap between stated and estimated income, the reason describes it and the notice complies; if the model put the $52,000 estimate into a payment-to-income ratio that drove the decline, the factor actually scored is income relative to the payment and the notice violates.")
rev("C59", "C48", "S11 boundary of adverse action",
    "Northgate's account-management model flagged a credit card account for closure because of a 60-day delinquency on that account. Northgate closed the account and mailed the cardholder a letter saying it was closed 'under our account-management policy.'",
    "depends",
    "Closing an account whose holder is currently delinquent or in default is not adverse action, but closing an account because of a past delinquency generally is, and a statement that the action followed the creditor's policy is not a specific reason (12 CFR 1002.2(c)(2)(ii); comment 2(c)(2)(ii)-2; 12 CFR 1002.9(b)(2)).",
    "12 CFR 1002.2(c)(2)(ii); comment 2(c)(2)(ii)-2; 12 CFR 1002.9(b)(2)",
    "The delinquency exclusion looks dispositive, so models do not ask whether the delinquency was still current at closure.",
    "Whether the account was still delinquent or in default when Northgate closed it: if so, the closure is not adverse action and the letter owed no statement of reasons; if the cardholder had brought it current and was not in default, the closure was adverse action and the reference to policy is an insufficient statement of reasons.")
supp_vd("C60", "S11 boundary of adverse action",
    "Summit Lending's website lets consumers check their rate with a soft credit pull. A consumer entered her income and asked to borrow $10,000; Summit's model evaluated her bureau data, and the site displayed: 'Based on your information, we are unable to offer you a loan at this time because your profile does not meet our lending criteria.' Summit sent nothing further.",
    "violates",
    "A creditor that evaluates information about a consumer, decides it will not approve the request and tells the consumer so has denied an application, so a notice was owed, and 'does not meet our lending criteria' is the internal-standards statement 12 CFR 1002.9(b)(2) calls insufficient (comment 9-5).",
    "comment 9-5; 12 CFR 1002.9(b)(2)",
    "A soft-pull rate check looks like a prequalification inquiry rather than an application.")
supp("C61", "S10 incomplete applications",
    "Meridian Bank's personal-loan model cannot score an application without verified income. Within 30 days of receiving an application without pay stubs, Meridian sent a written notice listing the missing stubs, giving the applicant 15 days to provide them and stating that otherwise the application would receive no further consideration. The applicant uploaded the stubs on day 25, and Meridian replied by letter that the application had been closed because the information arrived after the deadline and invited the applicant to apply again.",
    "A creditor that sent a proper notice of incompleteness has no further obligation when the applicant does not respond within the designated period, and it may require a new application for information that arrives late, so no statement of reasons was owed (12 CFR 1002.9(c)(2); comment 9(c)(2)-1).",
    "12 CFR 1002.9(c)(2); comment 9(c)(2)-1; 12 CFR 1002.9(b)(2)",
    "The applicant did supply the information, and the closing letter gives no credit reason, which looks like a denial without specific reasons.")
supp_vd("C62", "S14 counteroffer and multi-creditor notices",
    "An applicant asked Northgate Bank for a credit card with a $25,000 limit. Northgate's model approved a $6,000 limit, and Northgate mailed the card with a letter saying, 'Based on our credit policy, we are able to offer you a limit of $6,000.' The letter gives no other reason, and 120 days have passed.",
    "depends",
    "A counteroffer is adverse action only if the applicant does not use or expressly accept the credit offered, and a notice that then rests on the creditor's credit policy does not state specific reasons (12 CFR 1002.2(c)(1)(i); 12 CFR 1002.9(b)(2)).",
    "12 CFR 1002.2(c)(1)(i); 12 CFR 1002.9(a)(1)(iv); 12 CFR 1002.9(b)(2)",
    "The policy language invites an immediate 'violates', and the counteroffer invites an immediate 'complies'; the applicant's response decides between them.",
    "Whether the applicant used or expressly accepted the card: if so, the counteroffer was not adverse action and no statement of reasons was owed; if not, it became adverse action and 'based on our credit policy' is an insufficient statement of reasons.")
rev("C63", "C51", "S11 boundary of adverse action",
    "Northgate offers its credit card only to residents of Ohio, Indiana and Michigan. A cardholder moved to Arizona, and Northgate closed the account for that reason and mailed a letter saying it was closed 'in accordance with our account policies.'",
    "depends",
    "Closing an account because the cardholder moved out of the issuer's service area is adverse action unless the credit agreement explicitly provided for termination on that ground, and a reference to the creditor's policies is not a specific reason (12 CFR 1002.2(c)(1)(ii); comment 2(c)(1)(ii)-1; 12 CFR 1002.9(b)(2)).",
    "12 CFR 1002.2(c)(1)(ii); comment 2(c)(1)(ii)-1; 12 CFR 1002.9(b)(2)",
    "A closure for moving away has nothing to do with creditworthiness, and the letter names the real cause, so models either excuse it or condemn the policy wording without asking what the agreement said.",
    "Whether the card agreement explicitly provided for termination if the cardholder moved out of the service area: if it did, the closure is not adverse action and the letter owed no statement of reasons; if it did not, the closure is adverse action and the reference to account policies is an insufficient statement of reasons.")
rev("C64", "C52", "S11 boundary of adverse action",
    "A borrower who has paid every installment on time asked Lakeview Credit Union, using its online modification request form, to extend her auto loan's remaining term from 24 to 48 months. Lakeview's model declined the request, and Lakeview emailed her that 'loan modifications are handled at our discretion and your request was not approved.'",
    "violates",
    "Refusing to extend a loan's term is adverse action when the borrower applied under the creditor's procedures, and an email that cites the creditor's discretion gives no specific reason (12 CFR 1002.2(c)(1)(i); comment 2(c)(1)(i)-1; 12 CFR 1002.9(b)(2)).",
    "12 CFR 1002.2(c)(1)(i); comment 2(c)(1)(i)-1; 12 CFR 1002.9(b)(2)",
    "A modification of an existing loan looks like account servicing rather than a credit application.")
assert len(C) == 59, len(C)
os.makedirs("work/blind", exist_ok=True)
json.dump(C, open("work/candidates.json", "w"), indent=2)
json.dump([{"id": c["id"], "facts": c["facts"]} for c in C], open("work/blind/case_facts.json", "w"), indent=2)
from collections import Counter
print(Counter(c["gold_label"] for c in C), Counter(c["seam"] for c in C).most_common(3), len(set(c["seam"] for c in C)))

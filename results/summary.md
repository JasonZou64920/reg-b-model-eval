# Hardness test results

Run date: 2026-10-31. Mode: subagent_panel.

## Panel

- `claude-fable-5-1` (fable)
- `claude-opus-5-5` (opus)
- `claude-sonnet-5-5` (sonnet)

## Accuracy by model and condition

| Condition | Model | Correct | Label misses | Fact misses | Parse misses |
|---|---|---|---|---|---|
| A | `claude-fable-5-1` | 46/59 | 13 | 0 | 0 |
| A | `claude-opus-5-5` | 48/59 | 11 | 0 | 0 |
| A | `claude-sonnet-5-5` | 43/59 | 15 | 1 | 0 |
| A2 | `claude-fable-5-1` | 6/11 | 5 | 0 | 0 |
| A2 | `claude-opus-5-5` | 4/11 | 7 | 0 | 0 |
| A2 | `claude-sonnet-5-5` | 3/11 | 8 | 0 | 0 |
| B | `claude-fable-5-1` | 27/32 | 5 | 0 | 0 |
| B | `claude-opus-5-5` | 28/32 | 4 | 0 | 0 |
| B | `claude-sonnet-5-5` | 26/32 | 5 | 1 | 0 |
| C | `claude-fable-5-1` | 7/11 | 4 | 0 | 0 |
| C | `claude-opus-5-5` | 10/11 | 1 | 0 | 0 |
| C | `claude-sonnet-5-5` | 8/11 | 3 | 0 | 0 |

## Condition A

- Missed by at least one model: 21 of 59 (C03, C05, C10, C11, C17, C24, C25, C29, C31, C45, C47, C48, C51, C52, C53, C55, C56, C57, C58, C59, C63)
- Missed by two or more: 11 (C05, C25, C31, C47, C48, C51, C55, C56, C58, C59, C63)
- Missed by every model: 8 (C05, C25, C31, C48, C55, C56, C59, C63)

## Condition A2

- Missed by at least one model: 8 of 11 (C25, C47, C53, C55, C56, C58, C59, C63)
- Missed by two or more: 7 (C25, C47, C55, C56, C58, C59, C63)
- Missed by every model: 5 (C25, C56, C58, C59, C63)

## Condition B

- Missed by at least one model: 7 of 32 (C10, C17, C25, C29, C31, C48, C51)
- Missed by two or more: 5 (C25, C29, C31, C48, C51)
- Missed by every model: 3 (C25, C31, C48)

## Condition C

- Missed by at least one model: 4 of 11 (C53, C56, C58, C59)
- Missed by two or more: 3 (C56, C58, C59)
- Missed by every model: 1 (C56)

## Citation flags (logged separately, not scored)

- A `claude-fable-5-1` C15: withdrawn (cited: 12 CFR 1002.9(b)(2); Official Interpretation comments 9(b)(2)-2, 9(b)(2)-4, appendix C-4; CFPB Circular 2022-03; CFPB Circular 2023-03)
- A `claude-fable-5-1` C17: withdrawn (cited: 12 CFR 1002.9(b)(2); Official Interpretation comment 9(b)(2)-3; CFPB Circular 2023-03)
- A `claude-fable-5-1` C29: missing:12 CFR 1002.2(c)(2)(vi) (cited: 12 CFR 1002.9(b)(2); Supplement I, comment 9(b)(2)-3; Appendix C, Form C-1; see also 12 CFR 1002.2(c)(2)(vi))
- A `claude-fable-5-1` C50: missing:12 CFR 1002.2(f) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(1) and (a)(2)(i); 12 CFR 1002.2(c)(1)(i) and (c)(2)(iii); 12 CFR 1002.2(f))
- A `claude-fable-5-1` C51: missing:comment 2(c)(1)-1 (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(1)(iii) and 1002.9(a)(2); 12 CFR 1002.2(c)(1)(ii) and 1002.2(c)(2)(i); Official Interpretation, Supplement I to Part 1002, comment 2(c)(1)-1 (move from service area))
- A `claude-fable-5-1` C52: missing:12 CFR 1002.2(e)|12 CFR 1002.2(f) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(c)(1)(i), 1002.2(e), 1002.2(f))
- A `claude-fable-5-1` C58: withdrawn (cited: 12 CFR 1002.9(b)(2); 12 CFR Part 1002, Supp. I, comments 9(b)(2)-2 and 9(b)(2)-9; CFPB Circular 2023-03)
- A `claude-fable-5-1` C60: missing:comment 2(f)-3 (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); comment 2(f)-3 (inquiry evaluated and declined is treated as an application))
- A `claude-fable-5-1` C64: missing:12 CFR 1002.2(f)|12 CFR 1002.2(q) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(c)(1)(i); 12 CFR 1002.2(c)(2)(ii); 12 CFR 1002.2(f); 12 CFR 1002.2(q))
- A `claude-opus-5-5` C18: withdrawn (cited: 12 CFR 1002.9(b)(2); Official Interpretation 9(b)(2)-4; CFPB Circular 2023-03)
- A `claude-opus-5-5` C52: missing:12 CFR 1002.2(f)|12 CFR 1002.2(q) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(c)(1) and (c)(2)(ii); 12 CFR 1002.2(f); 12 CFR 1002.2(q))
- A `claude-opus-5-5` C60: missing:12 CFR 1002.2(f) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(f) and Official Interpretation 2(f)-3 (prequalification requests))
- A `claude-opus-5-5` C64: missing:12 CFR 1002.2(f)|12 CFR 1002.2(q) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(c)(1)(i) and (c)(2)(ii); 12 CFR 1002.2(f); 12 CFR 1002.2(q))
- A `claude-sonnet-5-5` C52: missing:12 CFR 1002.2(f)|12 CFR 1002.2(q) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(c)(1)(i); 12 CFR 1002.2(f); 12 CFR 1002.2(q))
- A `claude-sonnet-5-5` C62: missing:12 CFR 1002.2(c)(1)(iv) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.2(c)(1)(iv); 12 CFR 1002.9(a)(1)(iv))
- A `claude-sonnet-5-5` C64: missing:12 CFR 1002.2(f) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(c)(1); 12 CFR 1002.2(f))
- A2 `claude-fable-5-1` C64: missing:12 CFR 1002.2(f)|12 CFR 1002.2(q) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(c)(1)(i), 1002.2(c)(2)(ii), 1002.2(f), 1002.2(q))
- A2 `claude-sonnet-5-5` C64: missing:12 CFR 1002.2(f) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.9(a)(2)(i); 12 CFR 1002.2(c)(1) and 1002.2(f))
- B `claude-fable-5-1` C24: missing:comment 9(c)(1)-2 (cited: 12 CFR 1002.9(b)(2); comment 9(b)(2)-2; 12 CFR 1002.9(c)(1)(i); comment 9(c)(1)-2; Appendix C, Form C-1)
- B `claude-fable-5-1` C29: missing:12 CFR 1002.2(c)(2)(vi) (cited: 12 CFR 1002.9(b)(2); 12 CFR 1002.2(c)(1)(i) and 1002.2(c)(2)(vi); Supplement I comment 9(b)(2)-2)
- B `claude-sonnet-5-5` C27: missing:12 CFR 1002.2(c)(1)(iv) (cited: 12 CFR 1002.9(a)(1)(i) and (iv), 1002.9(a)(2), 1002.9(b)(2); 12 CFR 1002.2(c)(1)(iv))

## Parse status other than first-try ok

- none

## Notes on this run

**Mode.** No provider API key (ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY) was set in the environment, so the API path in `harness/run.py` could not run. The panel ran through the fallback in `harness/panel.py`. Each panel member was a separate agent session running one Claude model, with access only to its own prompt file and one reply file. Model IDs are what each session reported from its system prompt: `claude-fable-5-1`, `claude-opus-5-5`, `claude-sonnet-5-5`. All three are Anthropic models, so this run has no cross-provider comparison. Temperature cannot be set for agent sessions.

**Prompt sets** (`results/panel/<set>/`).
- `main`: C01 to C31, excluding C19 (dropped before testing). These ran in six batches of five, dealt so that no batch held two cases from the same seam.
- `supp`, `supp2` to `supp10`: the supplementary cases C32 to C64, mostly one case per session, which is closer to the one-call-per-case API design. C53 to C59 (`supp6`) are the audit council's revisions.
- `final` and `final47`: the replication draw (A2) and the full-rulebook run (C) for the final ten, plus C64 as a control.
- Every case block is identical to the API prompt for its condition. See `prompt_sha` in `raw_responses.jsonl`.

**Conditions.**
- **A** (the hardness criterion): the fixed prompt, the case and the verbatim text of 12 CFR 1002.9(b)(2). All 59 candidates.
- **A2**: the identical Condition A prompt, run again in new sessions on the final ten and C64, so the selected cases are not judged only on the draw used to select them.
- **B**: Condition A plus comments 9(b)(2)-1 to -9. Run on the 30 main cases and on C48 and C51 (32 cases).
- **C**: Condition A plus every provision and comment in `sources/`. Run on the final ten and C64. Added after the audit, so a miss cannot come from missing authority.
- A blank in a `misses_<condition>` column of `scores.csv` means the case was not run under that condition.

**Excluded after testing.** C45 and C17 were missed in Condition A, but their gold labels are contestable (see `work/adjudication_log.md`). `scores.csv` still marks them hard_A on the raw outcome. C03, C29 and C51 were removed by the audit council, and C05, C10, C11, C31 and C48 were replaced by revised cases (see `work/audit_log.md`).

**Observations.**
- Condition A: 21 of 59 candidates were missed by at least one model, 11 by two or more, and 8 by all three. First-try accuracy was Fable 46/59, Opus 48/59 and Sonnet 43/59.
- The wrong labels skew toward "complies". Of 39 wrong labels in Condition A, 26 called a deficient or undecided notice compliant. Only 2 of the 24 complies candidates drew any miss.
- Final ten: misses were 22 of 30 in A, 20 of 30 in the fresh draw (A2) and 8 of 30 with the full rulebook (C). Most of the difficulty comes from authority outside 9(b)(2). C56 was missed by every model in every condition. With the full rulebook, C59 and C58 were still missed by two models and C53 by one.
- On C59 in Condition C, Sonnet's reasoning names the deciding fact ("assuming the delinquency was current rather than a cured past delinquency") but labels the case "complies". It is scored as a label miss.
- Withdrawn authority: models cited the withdrawn CFPB Circulars 2022-03 or 2023-03 four times in Condition A (Fable on C15, C17 and C58; Opus on C18). Fable's C58 citation is on a final case.
- Provisions that do not exist: Fable cited 12 CFR 1002.2(c)(2)(vi) on C29 (Conditions A and B), and Sonnet cited 12 CFR 1002.2(c)(1)(iv) on C62 (A) and C27 (B). The other "missing" citation flags point to real provisions outside `sources/`, such as 1002.2(f) (application) and 1002.2(q).
- On C29, Fable relied on the checklist reason "We do not grant credit to any applicant on the terms and conditions you request". That line is not in the current Appendix C.
- Deciding facts are graded in `deciding_fact_grades.csv`, with one note per row. The only fact misses are Sonnet on C51 in Conditions A and B.

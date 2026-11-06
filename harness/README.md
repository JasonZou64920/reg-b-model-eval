# Regulation B hardness harness

Tests whether current models label Regulation B adverse-action cases correctly on their first try. A case counts as hard if at least one panel model mislabels it in Condition A.

## What each model sees

- **Condition A (defines "hard")**: the fixed prompt, the verbatim text of 12 CFR 1002.9(b)(2), the case facts, and a JSON output instruction. Nothing else.
- **Condition A2 (replication)**: the identical Condition A prompt, run again in new sessions on the selected cases, so they are not judged only on the draw used to select them.
- **Condition B (secondary)**: the same, plus the verbatim official commentary to 9(b)(2) (comments 9(b)(2)-1 to -9).
- **Condition C (full rulebook)**: the same, plus every provision and comment in `../sources/` (1002.9, 1002.2(c), the comments to 9 and 2(c), and Appendix C). This shows whether a miss survives once the governing authority is in front of the model.
- Fixed prompt: "Label this case under 12 CFR 1002.9(b)(2) as complies, violates, or depends. If depends, name the deciding fact. Give one sentence of reasoning citing the specific provision."
- Required output: `{"label", "reasoning", "citation", "deciding_fact"}`.

All prompt text is built in `prompts.py` from `config.py` and the files in `../sources/`, so every model and both run modes get identical case text.

## Setup

Python 3.10+, standard library only. No packages to install.

```
export ANTHROPIC_API_KEY=...   # any subset of the three; missing providers are skipped and reported
export OPENAI_API_KEY=...
export GEMINI_API_KEY=...
```

## Reproduce

From the repository root (the folder that contains `harness/`, `sources/`, `work/`, `results/`):

```
python -m unittest discover -s harness/tests -t .      # offline tests of retry, parsing, prompts, citation index
python -m harness.run --condition A                     # one request per case per provider flagship
python -m harness.run --condition B
python -m harness.run --condition C --cases work/final_cases.json    # A2 and C were run on the final ten
python -m harness.score --template                      # adds depends/depends pairs to results/deciding_fact_grades.csv
#   ...grade the 'match' column (yes/no) by hand...
python -m harness.score                                 # writes results/scores.csv, scores_long.csv, summary.md
```

`run.py` queries each provider's model list endpoint and picks the newest model in the flagship tier (Anthropic: highest tier family; OpenAI: newest full `gpt-` model, excluding mini/nano/audio/realtime variants; Google: highest-version `gemini-*-pro`). It prints the pick; override with `--models anthropic=<id> openai=<id> google=<id>`.

## Call policy

- One request per case per model, temperature 0 where the model accepts it (if a model rejects the parameter, the request is resent without it and `temperature_unsupported` is logged).
- No retries on content.
- 429 and 5xx responses and connection errors are retried with exponential backoff and full jitter (base 2 s, cap 60 s, up to 8 retries, `Retry-After` honored). These transport retries are counted in each record and never count as attempts.
- If a reply cannot be parsed, the harness sends one format-only re-request that adds no content. If that is still unparseable, the case is scored as a miss and logged as `unparseable`.

## Scoring

- `hit`: label matches gold, and for gold "depends" the deciding fact names the same decisive unknown.
- `miss_label`, `miss_fact`, `miss_parse` as defined in `score.py`.
- Deciding-fact matches are graded by hand in `results/deciding_fact_grades.csv`, with a note per row.
- Citation problems (a cited provision that does not exist in `sources/`, a withdrawn CFPB circular, or no parseable citation) are logged separately and do not change the outcome.

## Fallback panel (used for the submitted run)

No provider API key was available in the environment where the submitted run was produced, so the panel was run with the fallback in `panel.py`: separate agent sessions, each running a different Claude model, with no tools and no file access.

```
python -m harness.panel export --condition A --batch-size 5     # writes results/panel/prompts/ and batches.json
#   ...each panel member answers each batch prompt; raw replies saved to results/panel/replies/<cond>/<alias>_batch<k>.txt
python -m harness.panel import --condition A --member <alias>=<model_id> ...
python -m harness.score
```

Differences from the API path, disclosed in the work sample:
- All panel members are Anthropic models. There is no cross-provider comparison in the submitted run.
- Each session answers a batch of five cases rather than one case per call. Batches are dealt so that no two cases from the same seam share a batch, and every case block is the exact API prompt.
- Temperature cannot be set for agent sessions.
- Model IDs are the identifiers each session reported from its own system prompt.

Run details (model IDs, run date, batch membership) are in `../results/summary.md` and `../results/panel/batches.json`.

### Submitted run

| Item | Value |
|---|---|
| Run date | 2026-10-31 |
| Panel | `claude-fable-5-1`, `claude-opus-5-5`, `claude-sonnet-5-5` (self-reported IDs; agent sessions selected by model tier) |
| Mode | `subagent_panel` (no API keys present; the API path exits with a message) |
| Condition A | 59 cases, all three models |
| Condition A2 | the final ten plus C64, all three models (set `final`; C47 in set `final47`) |
| Condition B | 32 cases (the 30 main cases plus C48 and C51), all three models |
| Condition C | the final ten plus C64, all three models (set `final`; C47 in set `final47`) |
| Prompt sets | `main` (results/panel/), and `supp`, `supp2` to `supp10`, `final`, `final47` (results/panel/<set>/) |

To rebuild the scores from the saved replies without rerunning any model:

```
rm results/raw_responses.jsonl
python -m harness.panel import --condition A --member fable=claude-fable-5-1 opus=claude-opus-5-5 sonnet=claude-sonnet-5-5
python -m harness.panel import --condition B --member fable=claude-fable-5-1 opus=claude-opus-5-5 sonnet=claude-sonnet-5-5
M="fable=claude-fable-5-1 opus=claude-opus-5-5 sonnet=claude-sonnet-5-5"
for s in supp supp2 supp3 supp4 supp5 supp6 supp7 supp8 supp9 supp10; do
  python -m harness.panel import --condition A --set $s --member $M
done
for s in supp4 supp5; do python -m harness.panel import --condition B --set $s --member $M; done
for s in final final47; do
  python -m harness.panel import --condition A2 --set $s --member $M
  python -m harness.panel import --condition C --set $s --member $M
done
python -m harness.score     # uses the hand grades already in results/deciding_fact_grades.csv
```

## Files

| File | Purpose |
|---|---|
| `config.py` | Fixed prompt, output contract, retry constants |
| `sources.py` | Loads verbatim rule and commentary text; builds the provision index used to check citations |
| `prompts.py` | Builds per-case prompts and panel batches |
| `providers.py` | Anthropic, OpenAI and Gemini clients, model listing, flagship pick, backoff |
| `parse.py` | Parses and validates model JSON |
| `run.py` | API run |
| `panel.py` | Fallback panel export and import |
| `score.py` | Scoring, `scores.csv`, `summary.md` |
| `tests/` | Offline unit tests |

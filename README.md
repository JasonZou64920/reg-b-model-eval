# Regulation B model evaluation

Jason Zou · [jzou1@uchicago.edu](mailto:jzou1@uchicago.edu)

This is the project behind my work sample for CTGT's AI Evaluation Research internship. The question was simple: can today's AI models apply a real lending rule correctly, and where do they go wrong?

## The rule

When a lender turns someone down for credit, Regulation B (12 CFR 1002.9(b)(2)) says it has to tell them the specific reasons. "You didn't meet our standards" isn't enough. The rule itself is only a few sentences long, but a lot of the real answers are in the official commentary and the sections around it.

## What I did

I wrote 59 short scenarios about lenders and the letters they sent. Each one has an answer: the letter complies with the rule, violates it, or it depends on a fact the scenario leaves out. I checked every answer against the regulation text, and a separate AI reviewer labeled each scenario without seeing my answers.

Then I gave the scenarios to three AI models and kept the ten that at least one of them got wrong. Those ten make up the work sample in `deliverable/`.

## What the harness does

The harness is the small Python program that ran the test. It gives every model the same question, keeps only its first answer, checks that answer against the answer key, and saves everything so anyone can check the grading.

It's built to call AI models directly, but I didn't have API keys when I ran it. So the three models (claude-fable-5-1, claude-opus-5-5 and claude-sonnet-5-5) answered in separate sessions instead, and the harness graded their replies the same way. There's more detail in `harness/README.md`.

## What I found

On the first try, the models missed 22 of 30 answers on the final ten. Running the same test again gave 20 of 30, so the misses mostly held up. When I also gave them the rest of the regulation and its commentary, the misses dropped to 8.

Two things came out of that. When a key fact was missing, the models usually just picked an answer, most often "complies", instead of saying it depends. And most of their mistakes came from missing context, not from the rule being hard to read.

## Running it yourself

You need Python 3.10 or later, and there's nothing to install.

```
python -m unittest discover -s harness/tests -t .
python -m harness.score
python scripts/verify_deliverable.py
```

The first command runs the harness's own checks, the second rebuilds the scores from the saved answers, and the third checks the work sample. To test models directly, set an API key (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY` or `GEMINI_API_KEY`) and run `python -m harness.run --condition A`.

## What's where

- `deliverable/` has the two-page work sample.
- `work/` has all 59 scenarios, their answers, and notes on how the final ten were picked.
- `harness/` has the test code.
- `results/` has every question, every answer and the scores.
- `sources/` has the regulation text I used.
- `scripts/` has helpers for downloading the law and for building and checking the document.

## Things to keep in mind

- All three models come from one company, so this isn't a comparison across providers.
- Each model answered once, plus one rerun on the final ten, so the numbers are small.
- I wrote about half of the scenarios after seeing the first results.
- I built this with help from AI (Claude), and I checked every answer and citation against the regulation text.

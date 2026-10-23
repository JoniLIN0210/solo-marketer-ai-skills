# Evals

A skill is only useful if the AI follows it when it matters. These evals check exactly that.

## How to run an eval

1. Start a fresh conversation with the skill installed.
2. Give the AI the **setup** and **prompt** from a case, plus the files it names.
3. Score the response against the **pass criteria**. Every criterion is pass or fail; partial credit hides problems.
4. Record the result in the table at the bottom of each file.
5. When a case fails, decide the cause (input data, skill instructions, model capability or task design), fix the skill, and run the whole file again, not just the failed case.

## What makes a good case

- It targets one rule that would be expensive to break.
- It is realistic: a request a busy person would actually type.
- It has an objective pass criterion that two people would score the same way.
- Some cases tempt the AI to break a rule (for example "just reuse last month's list"). Those matter most.

## Files

| File | Skill | Cases |
|---|---|---|
| [`email-list-builder.md`](email-list-builder.md) | email-list-builder | 6 |
| [`report-to-article.md`](report-to-article.md) | report-to-article | 6 |
| [`geo-publishing.md`](geo-publishing.md) | geo-publishing | 4 |

The email list script also has automated tests in [`../tests/`](../tests/).

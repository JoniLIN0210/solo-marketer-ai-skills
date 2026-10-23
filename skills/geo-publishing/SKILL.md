---
name: geo-publishing
description: Plan, write and track content that helps AI search engines and chat assistants find, describe and cite a brand accurately (generative engine optimisation, GEO). Use for question-led articles and answers on open platforms, brand fact pages, site files such as llms.txt and sitemaps, and re-testing how AI assistants describe the brand. Do not use for paid ads.
---

# GEO publishing

Goal: AI assistants and search engines can find the brand, describe it correctly, and cite sources you control.

## Why this matters

AI assistants answer from content they can crawl. If most of a brand's content sits inside closed apps, newsletters or PDFs, assistants either ignore the brand or describe it from third-party guesses. GEO puts accurate, well-sourced answers where crawlers and assistants can read them.

## Order of authority

1. The user's request in this task.
2. Approved public content and official brand facts.
3. The rules in this skill.
4. Past batches. Use them for de-duplication, not as a source of facts.

## Hard rules

- Source every post from content that is already approved for public release. Never publish gated or private information.
- One post answers one real question. Titles use the words people actually search or ask.
- Name the brand and the source report clearly in each post so the origin is machine-readable.
- No duplicate titles or near-duplicate posts across batches. The same evidence may serve different questions, but the angle and text must differ.
- Drafting, saving a platform draft, submitting and publishing are separate permissions. "Don't publish yet" means draft only.
- Record the real status from the platform's management page. "Submitted" is not "published".

## Workflow

1. **Baseline.** Before publishing, ask the target AI assistants a fixed set of questions about the brand and record the answers. Use [`references/answer-retest.md`](references/answer-retest.md).
2. **Fix the foundations.** Make sure the brand's own site has crawlable pages for its core facts, plus the files in [`references/site-checklist.md`](references/site-checklist.md).
3. **Plan questions.** List the questions buyers and journalists ask (what the company is, what it offers, category questions where it has real evidence). Map each question to an approved source.
4. **Write in batches.** Short, complete answers. One question per post. Check every title against the publishing log before writing.
5. **Publish within the granted permission.** Log every item in [`references/publish-log.md`](references/publish-log.md).
6. **Re-test on a schedule.** Ask the same questions every two weeks. Track whether the brand appears, whether it is described correctly, and which sources are cited.
7. **Move from "cited" to "cited correctly".** When assistants repeat wrong or exaggerated claims, find the source they rely on and publish a clearer, authoritative answer to that exact question.

## Definition of done

- Zero duplicate titles; zero empty posts.
- Every post maps to an approved source and names the brand.
- No gated or private information; no block-listed sources.
- Published counts, draft counts and platform totals reconcile; items under review are listed separately.

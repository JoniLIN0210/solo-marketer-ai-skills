# Solo Marketer AI Skills

Reusable AI skills and a short playbook for running B2B marketing as a team of one.

Most "AI for marketing" material is a list of prompts. Prompts are easy to write and hard to trust: they forget your rules, invent numbers, and quietly do things you never approved. This repository takes a different approach. Each skill writes down **how the work should be done**: which sources count, what must never be published, what "done" means, and which actions need a human. The AI can then do the work the same way every time, and you can check that it did.

Everything here comes from running marketing alone at a B2B data company, where one person covered content, lead generation, email, events and sales support. All company details have been removed, and every example uses a fictional company.

## What's inside

| Folder | What it is | Start here if you want to... |
|---|---|---|
| [`docs/`](docs/) | The method: how to pick tasks, write rules, add guardrails, check output and keep skills up to date | Understand the approach before building anything |
| [`skill-template/`](skill-template/) | A blank skill skeleton | Write a skill for your own workflow |
| [`skills/`](skills/) | Four worked skills | See complete, realistic examples |
| [`examples/`](examples/) | Fictional inputs and outputs for the skills | See what good output looks like |
| [`evals/`](evals/) | Test cases for each skill | Check whether a skill actually follows its rules |
| [`tests/`](tests/) | Automated tests for the list-building script | Run `python3 -m unittest` |
| [`tools/`](tools/) | A scanner that checks a folder for terms you must not publish | Clean up your own skills before sharing them |

### The four skills

| Skill | Job | The rule that matters most |
|---|---|---|
| [`report-to-article`](skills/report-to-article/) | Turn a paid research report into a public article | Every claim traces back to a page in the source; paid-only detail stays private |
| [`geo-publishing`](skills/geo-publishing/) | Publish content so AI search engines can find and cite your brand | One post answers one real question; publishing status is verified, not assumed |
| [`email-list-builder`](skills/email-list-builder/) | Build a campaign list from a contact database | Zero people who should not be emailed reach the send list |
| [`doc-localization`](skills/doc-localization/) | Translate decks and documents without breaking them | The glossary wins, and the file is opened and checked after translation |

## Quick start

1. **Pick one skill** that matches work you do every week.
2. **Install it.**
   - Claude Code: copy the skill folder into `.claude/skills/` in your project, or into `~/.claude/skills/` for all projects.
   - Claude apps: zip the skill folder and upload it as a custom skill.
   - Other AI tools: add a line to your `AGENTS.md` (or the tool's instruction file) such as `For email list tasks, follow skills/email-list-builder/SKILL.md.`
3. **Edit the parts marked `CONFIGURE`.** Each skill has a short configuration section for your banned sources, audience tiers, send limits and so on.
4. **Run the evals** in [`evals/`](evals/) before you rely on it for real work.

## Design principles

1. **Write the rules down once.** Anything you have explained to the AI twice belongs in a skill.
2. **Facts need a source.** A number without a traceable source is marked as missing, not filled in.
3. **Preparing is not publishing.** Drafting, saving a draft, submitting, publishing and changing live settings are separate permissions.
4. **"Generated" is not "done".** Files are opened and checked; lists are checked for leaks; platform status is read back.
5. **Fix the class, not the instance.** When one error is found, look for every error of the same kind.

The full reasoning is in [`docs/playbook.md`](docs/playbook.md).

## Running the tests

The email list skill includes a small, dependency-free Python script. To run its tests:

```bash
python3 -m unittest discover -s tests
```

To try it on the fictional sample data:

```bash
python3 skills/email-list-builder/scripts/build_list.py \
  --contacts examples/contacts.csv \
  --blocklist examples/blocklist.csv \
  --already-received examples/already_received.csv \
  --exclude-status customer,unsubscribed,bounced,do_not_contact \
  --segments brand,supplier,manufacturer \
  --batch-size 3 \
  --out /tmp/campaign
```

## Adapting this to your team

These skills were written for one person. To use them across a team:

1. Pilot one skill with one team for two weeks and record how long the task takes today.
2. Rewrite the `CONFIGURE` section with that team's own standards.
3. Teach it through a real task, not a prompt-writing workshop.
4. Collect failures every week and write the fix back into the skill.
5. Measure adoption, time, quality and business results ([`docs/measuring-impact.md`](docs/measuring-impact.md)).

## License

[MIT](LICENSE). Use it, change it, and share what you learn.

## About

Built by Joni Lin, a B2B marketer who builds AI workflows and small products. Feedback and issues are welcome. A Chinese version of this page is in [`README_zh.md`](README_zh.md).

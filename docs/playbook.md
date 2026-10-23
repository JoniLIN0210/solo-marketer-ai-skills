# Playbook: turning AI into a repeatable marketing system

This is the method behind every skill in this repository. It is written for one person, but each step also works for a small team.

## Step 1. Pick the right tasks

Start from the work you already do, not from what AI can do. List every task you repeated in the last two months, then score each one with four questions:

| Question | Good sign |
|---|---|
| How often do I do this? | Weekly or monthly |
| Can I write the rules down? | The rules fit into "always", "never" and "prefer" statements |
| Can the result be checked? | There is an objective test: numbers have sources, a list has zero leaks, a file opens |
| What happens if it goes wrong? | Mistakes are caught before anyone outside sees them |

Tasks that pass all four come first. Tasks that send, publish or commit to anything outside the company can still use AI, but only to prepare the work. A person does the final action.

A worksheet for this step is in [`task-selection.md`](task-selection.md).

## Step 2. Write the rules down as a skill

A skill is a short document the AI reads before it starts. Every skill in this repository uses the same structure:

1. **Order of authority.** What wins when instructions conflict. The default: the person's request in this task, then the project's own files and confirmed facts, then the skill's rules, then past examples. Past examples are snapshots and are checked again before reuse.
2. **Hard rules.** A few lines that are never broken, such as "every number needs a source; if there is none, mark it missing".
3. **Task router.** A table that maps each type of request to the workflow it needs, so the AI loads only the instructions that apply.
4. **Workflows.** For each task type: inputs, steps, default deliverables and common mistakes.
5. **Definition of done.** The checks that must pass before the work is handed over.

The blank version is in [`../skill-template/`](../skill-template/).

## Step 3. Add guardrails

Guardrails are rules that protect you from the AI's most expensive mistakes.

| Guardrail | What it means in practice |
|---|---|
| Traceable facts | Every number, quote and claim points to a page, a table or a URL. Calculated figures are labelled as calculated. |
| Source allow-list and block-list | Decide which sources are acceptable (official statistics, company filings, your own research) and which are never cited (for example, competitors' research). |
| Tiered disclosure | Decide in advance what is free to publish and what stays behind a form, a sale or an NDA. Judge the combination, not each number alone. |
| Separate permissions | Preparing a file, saving a draft, submitting for review, publishing or sending, and changing live settings are five separate permissions. "Help me prepare" grants only the first. |
| Secrets stay out | Passwords, API keys and tokens are never written into skills, project files or chat. |

## Step 4. Check instead of trusting

AI output often looks finished before it is correct. Each skill defines checks that replace "looks fine":

- **Content:** a verification table for every factual claim (statement, source, location, original scope, level of support, disclosure tier).
- **Lists:** zero leakage of anyone who must not be contacted, and zero duplicate addresses after normalisation.
- **Files:** documents, slides, spreadsheets and images are opened or rendered and inspected. A file that was generated successfully may still be broken.
- **Platforms:** status is read back from the platform. "Submitted" is not "published".
- **Corrections:** when one error is found, search for the whole class of errors, not just the one that was pointed out.

## Step 5. Maintain and migrate

- **Keep stable rules and changing facts apart.** Rules and workflows live in the skill. Facts that change (current projects, contact status, platform rules, file locations) live in a separate project-state file and are treated as snapshots.
- **Merge before you multiply.** When you have several small skills, combine them into one skill with a router. One place to maintain beats nine.
- **Make it portable.** Keep skills as plain Markdown files in a folder you control. When you change AI tools, a single instruction file (for example `AGENTS.md`) tells the new tool what to read first. Your knowledge moves with the files, not with an account.

## What to measure

See [`measuring-impact.md`](measuring-impact.md). Measure from the first week; a baseline recorded later is a guess.

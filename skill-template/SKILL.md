---
name: your-skill-name
description: One or two sentences saying what this skill does and when to use it. Name the triggers (for example "use when the user asks for a newsletter article from a report") and when not to use it.
---

# Skill name

Goal: one sentence describing the outcome this skill produces and for whom.

## Order of authority

When instructions conflict, follow them in this order:

1. The user's explicit request in the current task.
2. The project's own files, templates and confirmed facts.
3. The rules in this skill.
4. Past examples. Treat them as snapshots and re-check facts before reuse.

## Hard rules

<!-- CONFIGURE: keep this list short. Each rule should be something that is never broken. -->

- Every fact, number and quote must come from a source material or an approved source. If no source exists, mark it as missing. Never fill the gap.
- Never cite sources on the block-list in [`references/configuration.md`](references/configuration.md).
- Preparing, saving a draft, submitting, publishing or sending, and changing live settings are separate permissions. Do only what the current request authorises. See [`references/permissions.md`](references/permissions.md).
- When the user changes one part, change only that part. When the user points out one error, check for the same kind of error everywhere.
- Open or render every file before calling it done.

## Before each task

1. Read the project's current state file ([`references/project-state.md`](references/project-state.md)) and any files the user provided.
2. Use [`references/task-router.md`](references/task-router.md) to decide which workflow applies, and load only that workflow.
3. Ask a question only when the missing information would change the result, involves real identities, amounts, dates or permissions, or would cause an external action. Otherwise make a reasonable assumption and state it.

## Workflows

### Workflow A: <task type>

**Inputs:** ...

**Steps:**

1. ...
2. ...

**Deliverables:** ...

**Common mistakes:** ...

## Definition of done

Run [`references/qa-checklist.md`](references/qa-checklist.md) at a depth that matches the risk. Report what was delivered, where it is, what was checked, what is still unconfirmed, and the true status of any external action.

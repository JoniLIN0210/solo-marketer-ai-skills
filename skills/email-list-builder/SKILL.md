---
name: email-list-builder
description: Build a send list for a B2B email campaign from a master contact database, merging duplicate contacts, applying hard exclusions, choosing the right business segments and splitting the list into batches, with zero leakage of people who must not be emailed. Use for topic campaigns, report announcements and event invitations. Do not use for transactional email or for sending; this skill prepares lists only.
---

# Email list builder

Goal: a campaign list that reaches every relevant contact and nobody who should be left out, with an audit trail for every decision.

## Order of authority

1. The user's request in this task.
2. The current master contact file, the current block-list and the project's own list rules.
3. The rules in this skill and [`references/exclusion-rules.md`](references/exclusion-rules.md).
4. Previous send lists. Never use them as a starting point.

## Hard rules

- Always rebuild from the full, current master file. Never edit last campaign's list.
- One person is one normalised email address (trimmed, lower case). Merge every row for that address before deciding anything.
- Exclusion checks look at **all** history for a contact, not just the latest row.
- Never guess or "fix" an email address. List invalid addresses separately.
- The final list must have zero leaks (see "Definition of done"). If any check fails, the list is not delivered.
- This skill prepares lists. Sending is a separate permission and is done by a person.
- Never paste a full contact list into chat. Report counts and file locations.

## Workflow

1. **Collect inputs.** Master contact file (all sheets, including notes), current block-list, the list of people who already received this content, the campaign topic and the target business segments.
2. **Normalise and merge.** Normalise every address and group all rows by address.
3. **Apply hard exclusions.** Use [`references/exclusion-rules.md`](references/exclusion-rules.md). Record every reason.
4. **Identify what each company actually does.** Use, in order: the company or product name, well-known facts about the brand, the topics the contact has shown interest in, then job title and department. Generic names ("Technology", "Global", "Group") are not enough. Mark unclear companies "needs review" instead of guessing.
5. **Select and order segments.** Contacts in core segments come first, then directly related suppliers, then adjacent segments. Engagement signals (replies, demos, meetings) raise a contact's order within a segment; they are not entry requirements.
6. **Batch.** Split the list using the batch size and pacing your email service and domain can handle (see configuration).
7. **Check.** Run the script below, or the same checks by hand.
8. **Report.** Total recommended, change versus the last version, count per segment, number excluded per reason, result of every leak check.

## The script

[`scripts/build_list.py`](scripts/build_list.py) does steps 2, 3, 6 and 7 for a CSV export. Python 3.9+, no extra packages.

```bash
python3 scripts/build_list.py \
  --contacts contacts.csv \
  --blocklist blocklist.csv \
  --already-received already_received.csv \
  --exclude-status customer,unsubscribed,bounced,do_not_contact \
  --segments "brand,supplier,manufacturer" \
  --batch-size 100 \
  --out ./campaign
```

It writes `send_list.csv`, `excluded.csv`, `batches.csv` and `report.md`, and exits with an error if any leak check fails.

## Configuration

<!-- CONFIGURE -->

- Batch size: <limit per batch for your email service>
- Pacing: <maximum batches per day and minimum gap between batches>
- Status values that always exclude: <e.g. customer, unsubscribed, bounced, do_not_contact>
- Target segments for this campaign, in priority order: <...>

## Definition of done

All of these are zero:

- Addresses on the block-list.
- Current customers or contacts owned by another team, if your rules exclude them.
- Unsubscribed, bounced, invalid or do-not-contact addresses.
- People who already received this content.
- Duplicate addresses after normalisation.

And:

- The send list and the batch file contain exactly the same addresses.
- Every batch is within the size limit.
- Every company the user named has been checked individually, with its result recorded.

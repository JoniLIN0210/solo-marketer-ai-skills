# Exclusion rules

A contact is excluded if **any** row in their history matches **any** rule below.

| # | Rule | Typical evidence |
|---|---|---|
| 1 | On the block-list | Address appears in the current block-list |
| 2 | Already received this content | Address in the "already received" file for this report, event or campaign |
| 3 | Unsubscribed or asked not to be contacted | Status or notes say unsubscribe, do not contact, stop sending |
| 4 | Invalid or bounced | Address fails format check or has bounced |
| 5 | Current customer, or owned by another team | Status, owner field or notes say so (if your rules exclude them) |
| 6 | Clearly no need | Notes record that they will not buy, have no budget, or declined and use an alternative |
| 7 | Outside the campaign's scope | Company type or role is outside the target segments (for example students or media, if not targeted) |

## Things that are **not** exclusion reasons on their own

- Using a competitor's product, unless the contact also declined.
- "No need right now, keep in touch". This is a pause, not a permanent exclusion.
- Low engagement. It lowers priority; it does not remove the contact.

## When the user points out a missed or wrong contact

Check every contact at that company, then every company in the same segment, then the rule that caused the error. Fix the rule, not just the row.

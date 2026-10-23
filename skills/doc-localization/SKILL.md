---
name: doc-localization
description: Translate slide decks, Word documents, spreadsheets and recurring reports between languages while keeping the structure, numbers, terminology and layout intact. Use for monthly report translations, bilingual documents, deck localisation and database or spreadsheet translation. Do not use for creative copywriting where a rewrite is wanted.
---

# Document localisation

Goal: a translated file that says exactly what the original says, uses the agreed terms, and opens and looks right.

## Order of authority

1. The user's request in this task.
2. The project glossary, previous translations in the same series and fixed product or report names.
3. The rules in this skill.
4. General translation judgment.

## Hard rules

- Translation is not rewriting. Keep the original's structure, numbers, units, ranges, chart labels and the link between text and images.
- The glossary wins. Any deliberate departure from it is listed in the delivery notes.
- Names with no settled translation (brands, products, legal names) stay in the original language; explain them on first use if needed.
- Text inside images, charts and tables is in scope unless the user says otherwise. "It could not be extracted" is not a reason to skip it.
- Open or render the finished file and inspect every page. A translated file that was saved successfully may still be broken.
- Flag source errors (typos, impossible values) with a note. Do not silently correct them.

## Workflow

1. **Gather references.** Glossary ([`references/glossary-template.csv`](references/glossary-template.csv)), earlier files in the same series, fixed names.
2. **Inventory the file.** Pages or slides, text boxes, tables, charts, images with text, notes, headers and footers.
3. **Translate.** Use the glossary first. Write the way a professional in the target market writes, without expanding the meaning.
4. **Rebuild the layout.** Languages differ in length; adjust line breaks, font size and spacing instead of only swapping strings. For bilingual documents, keep paragraphs paired one-to-one.
5. **Check.** Run [`references/layout-checks.md`](references/layout-checks.md).
6. **Deliver.** The translated file plus a short note: glossary departures, flagged source issues, anything left untranslated on purpose.

## Spreadsheets and databases

- Translate headers and categorical values; keep IDs, URLs and free-text brand fields in the original unless asked.
- Split multi-value cells on their separators, translate each token, and rejoin consistently.
- Preserve formulas: read values without overwriting formula cells.

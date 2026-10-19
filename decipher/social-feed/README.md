# Decipher social feed

[Try the native component](https://sw2.decipherinc.com/survey/selfserve/57d/2610180)

Five feeds of 30 synthetic posts. Participants scroll and Like posts, or double-click/double-tap an image. Likes can be undone; zero likes is valid. The component uses native Decipher answers and a real server-loaded design file.

![The native social-feed question](screenshot.jpg)

## Use in Decipher

Upload [`social-design.dat`](social-design.dat) to the survey's **root/system files**, then upload or paste [`survey.xml`](survey.xml) into a new testing survey. Both are required. Original copy and SVG illustrations are embedded in XML; there are no external assets or personal posts.

The survey opens directly on feed one after an automatic initialization submission preserves its assignment. Each feed ends with neutral Continue. There is no branded header, footer, intro, byline, or promotional shell.

To change counts or content, edit `config.json`, `build.py` and `src/`, then run:

```sh
python3 build.py
python3 build-template.py
```

Upload the regenerated XML and `.dat` together. Defaults are five feeds, 30 items and eight versions. Other configurations require native verification. The generator supports 1–12 feeds, 1–60 items and 1–99 versions; more than 30 items repeats copy levels.

## Questra fine-tuning template

Import [`questra-template.json`](questra-template.json) in Fine tuning. It contains:

- A shared base with one CSS/JavaScript pair, server-side design loader, copy/image resources and persistent assignment.
- A reusable `SocialFeed` XML component. Its only input is `task`, a required string enum `"1"`–`"5"`.
- The exact `.dat` file as a bundled system asset.

Render each task once, in order, in the `main` slot. For example, `SocialFeed` with `{"task":"1"}` renders feed one. Each instance includes offer metadata, its native response matrix and a page break. Keep one instance per page; do not mix other visible questions into these pages. Regenerate the export for different counts or designs. Upload the bundled `.dat` before native compilation.

The export passes Questra's transfer schema and component renderer. Rendering tasks 1–5 into its base reproduces the deployed XML byte-for-byte; the bundled design bytes also match. Invalid/missing task values are rejected. The export format is `questra-fine-tuning-template` version 1, with a version-2 base and XML-output component using `@{task}` interpolation.

## Design and answer schema

The tab-delimited `.dat` has a header and 1,200 records:

| Column | Meaning |
| --- | --- |
| Version | Assigned native `DesignVersion`, 1–8 |
| Task | Feed number, 1–5 |
| Concept | Display position, 1–30 |
| Copy / Image | Resource levels, 1–30 / 1–10 |
| Order | Explicit display position, matching Concept |
| Item | Unique feed/position identity, 1–150 |

The server loads the file from `gv.survey.path` during `exec when="init"` and resolves `(version, task, concept)`. The browser does no offer randomization. Version assignment is independent random allocation, not quota balancing; this reproducible synthetic design is not a statistically optimized conjoint design.

`Feed2r7` stores feed 2, position 7. Its native metadata fields are `Offer2r7task`, `Offer2r7item`, `Offer2r7order`, `Offer2r7copy` and `Offer2r7image`.

| Export code | State |
| --- | --- |
| 1 | Not exposed under the rule; not liked |
| 2 | Exposed, currently not liked |
| 3 | Currently liked |
| Missing | Feed not submitted; never interpret as zero likes |

Exposure requires at least 50% of a card's area within the viewport continuously for one second in a visible document, or an explicit Like. This records a display opportunity, **not attention or reading**. Fast scrolling alone does not establish exposure. Undo returns a liked post to code 2. Generated radio input values are zero-based; declared export codes are 1/2/3.

Native page submission saves each feed. A same-tab `sessionStorage` cache restores unfinished selections on reload; it does not provide cross-device or closed-tab recovery. Buttons support keyboard activation and `aria-pressed`; double-clicks share a duplicate-toggle guard. Continue locks before invoking the existing native button once. A stalled request requires reloading rather than automatic retries. A new clean URL may start another response in testing mode.

Forsta documents the [DCM design-file loading pattern](https://forstasurveys.zendesk.com/hc/en-us/articles/4409469905307-Creating-a-Discrete-Choice-Model-DCM-Question), [native single-select matrices](https://forstasurveys.zendesk.com/hc/en-us/articles/4409476975899-Single-Select-Question-XML) and [XML style system](https://forstasurveys.zendesk.com/hc/en-us/articles/4409461374491-XML-Style-System).

## Verification

Native checks covered all five feeds, design/display/export matching, multiple and zero likes, undo, double-click guards, keyboard controls, reload persistence and completion. The cleaned revision's completed response matched all 150 answer states and 750 offer metadata cells. The 390 px native layout had no horizontal overflow. Published XML and design match exact native readback.

Physical phone gestures, Safari, Firefox, screen readers, storage-disabled recovery and network failures remain unverified. The public folder contains no credentials, response exports or QA logs.

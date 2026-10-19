# Decipher swipe cards

A reusable swipe-card question for Decipher / Forsta Surveys, built on a native single-select radio matrix. Each row becomes a card with **Dislike**, **Skip**, and **Like** answers. The sample uses four synthetic weekend activities and original CSS artwork; it needs no external images or JavaScript libraries beyond the survey platform.

Cards follow horizontal gestures, rotate and fade toward the edge, snap back below the threshold, and reveal the next card behind them. Visible buttons and keyboard controls provide alternative input paths.

After the final choice is written to its native radio, the animation finishes, the deck disappears, and the component clicks Decipher's existing Continue button once. Native validation and submission handlers remain intact.

## Install the sample

1. Create an isolated test survey in Decipher / Forsta Surveys.
2. Upload [`survey.xml`](survey.xml) using your normal survey-source workflow. It includes the question, JavaScript and CSS; no separate assets are needed.
3. Open the normal respondent preview and answer the cards. The final selection should lead to the platform's completion page without a manual Continue click.
4. Validate the component in your own theme and survey configuration before using it with respondents.

The sample targets `compat="144"`, `fir="on"` and `ss:enableNavigation="0"`. It supports one native question per page. On an unsupported page or incompatible markup, the native matrix and Continue remain available.

To use the component in another survey, insert [`component.xml`](component.xml), followed by `<suspend/>`, on its own page. Give the question a unique label. Use static rows and the fixed three columns below.

## Files

| File | Purpose |
| --- | --- |
| `survey.xml` | Complete synthetic demo survey, ready to upload |
| `component.xml` | Standalone question with bundled styles and script |
| `src/question.xml` | Editable demo question and row copy |
| `src/swipe.js`, `src/swipe.css` | Component behavior and presentation |
| `src/survey-shell.xml` | Minimal survey shell |
| `questra-template.json` | Importable Questra fine-tuning template, including the component |
| `component.template.xml` | Parameterized component used by that template |
| `example-input.json` | Example variable question label, title and row data |
| `questra-questionnaire.md` | Sample questionnaire for a Questra programming run |
| `docs/TESTING.md` | Verification summary and known limitations |

## Customize and rebuild

Edit `src/question.xml` for the fixed demo's title and rows. Edit `src/swipe.js` or `src/swipe.css` to change the interaction or appearance. Then run with Node.js (verified with Node 24):

```sh
node build.mjs
```

There are no build dependencies. This regenerates the complete survey, bundled component, parameterized component, Questra export and example input. The generated XML escapes CSS `@media` as `\@media` for Decipher's style parser; keep normal `@media` in the standalone CSS.

## Answer mapping

| Meaning | XML column | Export code | Observed native radio value |
| --- | --- | --- | --- |
| Dislike | `c1` | `1` | `0` |
| Skip | `c2` | `2` | `1` |
| Like | `c3` | `3` | `2` |
| Unanswered | none selected | missing | no checked input |

The sample exports native row fields `QSwiper1` through `QSwiper4`. **Skip is an explicit answer, distinct from missing data.** Every row is required.

The script discovers existing radio groups and maps columns from native table-cell `headers` attributes. It selects the corresponding native input through `.click()`, retaining the platform's answer model and events. It does not manufacture field names, create duplicate answer fields, or call `form.submit()`.

## Controls and completion

- Swipe left for Dislike or right for Like. Release below 27% of the card width (bounded to 65–120px) to cancel.
- Use the Dislike, Skip and Like buttons, or focus the card and press Left Arrow, S or Right Arrow. Buttons also support normal Tab/Enter/Space activation.
- Repeated input is ignored while a card commits or snaps back. Direction and row stay fixed after commitment.
- Vertical touch movement is reserved for scrolling. Reduced-motion handling removes transforms and animated delays.
- Continue is hidden only after successful enhancement. The last answer triggers it once after the animation. A short “Saving your answers…” state replaces the deck.
- A validation redisplay with restored answers or saved-page re-entry reveals the native matrix and Continue without automatically resubmitting. A 12-second watchdog restores those controls if a submission stalls while the original document remains loaded. A browser error that replaces the document uses the browser's recovery controls.

The normal view has no Back/Undo, review page, debug display, visible progress or fallback toggle. Screen-reader instructions and status remain available. The component hides two specifically matched platform testing notices on its enhanced question page; it does not suppress validation errors or other warnings.

No independent draft cache is added. Reload persistence follows Decipher's survey configuration. If setup fails, the native question remains available. Disabling all browser JavaScript can still encounter the platform's own JavaScript-required completion gate.

## Use the Questra fine-tuning template

1. In Questra's **Fine tuning** area, use **Import template** and choose [`questra-template.json`](questra-template.json).
2. Select the imported template for a survey programming run or template test.
3. Supply [`questra-questionnaire.md`](questra-questionnaire.md), or another single-question static matrix specification.
4. Review the generated XML and verify native answer storage in a test survey.

The export uses the supported `questra-fine-tuning-template` version-1 transfer format. It includes a survey skeleton with a `main` slot, programming instructions, and the `SwipeCards` component with its JavaScript and CSS. No external files or template URLs are required.

The component accepts a unique question `label`, plain-text `title` and fallback `instructions`, and `rows` containing unique `label` and plain-text `text` values. See `example-input.json`. It uses Questra's `@{property}` interpolation and `@{#each rows as row}` loop with XML output escaping.

Example programming instruction:

> Create one required matrix using SwipeCards and the supplied questionnaire. Preserve Dislike/Skip/Like codes 1/2/3, the bundled swipe interaction, and guarded native completion after the final card. Use one question per page. Do not add Back/Undo, extra questions, debug displays or demo explanations.

Keep the three columns/codes fixed. Use a small set of uniquely labeled plain-text rows (1–20 is the authoring recommendation). Identifier validity, uniqueness and row-count constraints require review; do not assume every JSON Schema constraint is enforced by the template importer.

## Compatibility and testing

Do not add conditional/randomized rows, open-ended cells, row groups, translated columns, external media or another dynamic-question style without adapting and retesting the native adapter. Controls and decorative artwork are fixed in this example.

Native automatic completion and stored codes were verified on four-row and three-row examples, including rapid final double-clicks. A native validation rejection preserved the answers and restored a usable Continue path. See [testing details and limitations](docs/TESTING.md), including the outstanding touch-gesture verification limitation.

## License

No license has been selected or added.

## Platform references

- [Forsta XML Style System](https://forstasurveys.zendesk.com/hc/en-us/articles/4409461374491-XML-Style-System)
- [Forsta Survey Style Attributes](https://forstasurveys.zendesk.com/hc/en-us/articles/4409461364123-Survey-Style-Attributes)

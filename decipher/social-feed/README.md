# Decipher Facebook-style feed

Current shared-theme testing survey (October 21): [Open in Decipher](https://sw2.decipherinc.com/survey/selfserve/57d/2610210). Verified on desktop and mobile with synthetic completed responses; remains in testing mode. Older links/screenshots below are historical.

This example now uses the [shared Questra theme](../theme/README.md) for its page shell and common controls. That integration supersedes earlier notes below about retaining the default wrapper. See the shared guide for build commands, local previews, loading/fallback behavior, and current verification limits. Existing live links/screenshots show the earlier deployed version.

[Try the native survey](https://sw2.decipherinc.com/survey/selfserve/57d/2610180)

Five feeds of 20 posts, each with four sponsored ads interspersed among 16 organic posts (20% ads). Participants scroll and Like posts, or double-click/double-tap an image. Likes can be undone; zero likes is valid.

Captured data includes assigned ad creatives, Likes and **per-ad time in view**, saved in native Decipher fields for analysis. Separate cumulative millisecond measures record when at least 1% or 50% of each full ad card is visible, with visibility and focus gates excluding background time. Stable creative and placement IDs let analysts compare exposure alongside Likes. Time in view measures an opportunity to see an ad, not attention; the measurement definitions and validation limits are documented below.

![A respondent likes a post, scrolls the feed and likes a second post.](media/demo.gif)

[Download the MP4 demo](media/demo.mp4) · [Open the current Decipher test survey](https://sw2.decipherinc.com/survey/selfserve/57d/2610210)

[Earlier static screenshot](screenshot.jpg)

The UI follows the feed card conventions shown in [Meta’s October 2026 Facebook demo](https://about.fb.com/news/2026/10/introducing-your-algorithm-facebook/), inspected in an actual browser: circular avatars, bold name/timestamp rows, short copy, large photo media, Sponsored labels, subtle gray separators and a blue thumb Like state. Cards sit in a locally scoped column up to 590 px wide and shrink within the native survey margins on mobile. The existing Decipher frame, page background, progress indicator, other questions and native Continue are preserved. There is no Facebook logo, account login, fake composer, comment/share control or inactive shopping button.

[`content.json`](content.json) contains 30 natural first-person organic posts attributed to ten fictional people, plus 12 sponsored copy/offer variants for Aster Trail, Kettle & Kind and Leafline Studio. Names, posts, offers and brands are synthetic; no real person is represented as endorsing anything. Ads cover an everyday backpack, coffee and ceramic planters, with concrete prices, discounts and delivery offers. Their `.example` domains are reserved example labels, not external links.

Sixteen original photo-style images were made with the built-in image-generation tool: ten everyday scenes and six product images. Scenic avatar thumbnails are derived from those images. [`assets/manifest.json`](assets/manifest.json) records each full generation prompt, file and SHA-256 hash; [`assets/images/`](assets/images/) contains the JPEG deliverables. Only resizing/JPEG conversion was applied. No personal posts, customer data or third-party campaign imagery were used. Photos and small avatars are survey-owned static JPEG files. XML resources contain lightweight `[rel filename]` references; hidden native answer rows use `data-src` so they do not eagerly fetch media. Only visible enhanced cards receive image sources. The first two cards load eagerly and the remaining cards use browser lazy loading, reusing cached URLs. No external image hosting is required.

## Use in Decipher

Upload [`social-design.dat`](social-design.dat) as a **root/system file**, all 26 JPEGs from `assets/images/` to the survey’s **static/public folder**, then upload or paste [`survey.xml`](survey.xml) into a testing survey. All are required. The template bundles these exact files with their private/public visibility. The demo remains in testing mode.

An automatic initialization submission saves assignment before feed one. Each feed uses the unmodified native Continue and native validation/submission; there is no replacement navigation button. Keep one feed per page. Existing native questions can coexist on the page; do not add questions to this demo without authorization. Do not change an experiment's design or schema during data collection.

To regenerate:

```sh
python3 build.py
python3 build-template.py
node tests/timing.cjs
```

`config.json` controls feeds, items and versions: defaults 5 × 20 and eight versions. Supported generator ranges are 1–12 feeds, 1–60 items and 1–99 versions; changed configurations need native verification. There is one sponsored position in each group of up to five items. More than 30 organic positions repeats copy levels. Edit `content.json` for author, timestamp, organic text and ad-offer changes. Image levels and copy levels remain controlled by the design; regenerate both outputs after editing sources.

## Design and native identifiers

The genuine tab-delimited `.dat` contains 800 version/task/concept records. The server loads it from `gv.survey.path` during `exec when="init"`. Every copy/image combination and placement comes from this file; the browser does no offer randomization. This reproducible synthetic design is not an optimized conjoint or balanced allocation design.

| Design column | Meaning / native field for feed 2, item 7 |
| --- | --- |
| Version | Assigned `DesignVersion` (1–8) |
| Task | Feed number / `Offer2r7task` |
| Concept | Display position, 1–20 / row `r7` |
| Copy | Copy resource level, organic 1–30 or ad 31–42 / `Offer2r7copy` |
| Image | Original image level, organic 1–10 or ad 11–16 / `Offer2r7image` |
| Order | Explicit display order / `Offer2r7order` |
| Item | Stable feed/position ID, 1–100 / `Offer2r7item` |
| Kind | 0 organic, 1 sponsored / `Offer2r7kind` |
| Creative | Ad combination ID: `10000 + Copy*100 + Image`; 0 organic / `Offer2r7creative` |
| Campaign | 1 Aster Trail, 2 Kettle & Kind, 3 Leafline Studio; 0 organic / `Offer2r7campaign` |
| Context | Feed context ID, 1–5 / `Offer2r7context` |

There are 12 ad copy levels and two compatible image levels per campaign, producing 24 distinct ad creatives. All occur in the design. Each version/task selects four and varies their positions. Organic topics include food, outdoors, gardening, reading, art, neighborhood walks and cycling.

Use `(DesignRevision, DesignVersion, Task, Item)` to identify an assigned offer, and `(DesignRevision, DesignVersion, Context)` to identify its complete feed context. This revision writes `DesignRevision=5`. Revision 5 regenerates the genuine design for 20 items per feed, four ads and 16 organic posts, with item IDs 1–100. Copy levels, photos, frame containment, progressive loading, Like codes and the revision-4 exposure/timing rule are preserved. Do not merge offer identities across revisions: assigned combinations, placements and IDs changed. Earlier revision-1 records use a different design and exposure definition. Compare creative meanings within their revision. `SessionKey` is an anonymous same-response cache key, not a person identifier.

## Likes and qualifying visible time

`Feed2r7` is a native single-select answer:

| Export code | Meaning |
| --- | --- |
| 1 | Not liked; no qualifying visible time observed |
| 2 | Not liked; positive qualifying visible time observed |
| 3 | Currently liked, independently of time |
| Missing | Feed not submitted; never treat as zero likes |

Unlike returns to 1 or 2 according to measured time. A Like does **not** manufacture exposure time. Generated radio HTML values are zero-based; native export codes are 1/2/3.

`Time2r7ms` and `Time2r7state` are native **number-question cells**, not a JSON payload or text log. Decipher's JSON response API serializes their numeric values as strings; the questionnaire/export schema remains numeric.

The exact timing rule is:

1. The enhanced card must exist in the rendered component and its photo must have loaded successfully (`complete` and positive `naturalWidth`). The card must intersect the viewport, as reported by `IntersectionObserver`, and the document must be visible and focused. An image error marks its timing as an incomplete lower bound.
2. Compute the card's rectangle intersection with the viewport, including horizontal clipping. Its area must be at least **50% of `min(card width, viewport width) × min(card height, viewport height)`**. Thus a tall card can qualify while only its viewport-sized portion is visible.
3. Sample with `requestAnimationFrame` and monotonic `performance.now()`. Add elapsed milliseconds only when both adjacent samples qualify and their gap is at most 250 ms. Boundary frames are conservatively omitted. A longer qualifying gap adds no time and marks the item as an incomplete lower bound.
4. Accumulate across separate visits to the same item. Pause on loss of focus, hidden document, viewport exit and navigation. Flush on Continue, native form submission, page hide and before unload. Floor the cumulative total once when writing integer milliseconds.

| `Time…state` | `Time…ms` | Interpretation |
| --- | --- | --- |
| 0 | -1 | Timing has not initialized; uninstrumented/unobserved |
| 1 | 0 | Instrumented, no qualifying time measured |
| 2 | ≥1 | Positive qualifying time measured |
| 3 | ≥0 | Incomplete lower bound: a long qualifying sampling gap, lost cache on reload, unavailable storage, or an image load error |
| 4 | -1 | Required timing/browser APIs unavailable |
| Missing | Missing | No submitted measurement for this feed |

Zero milliseconds means no **qualifying** exposure measured, not proof the item was never partly displayed. State 3 is not a complete zero even when its value is zero. Geometry, focus and visibility record a display opportunity, **not attention, reading, ad recall or viewability certification**. Basic intersection checks cannot establish that another window, overlay or CSS opacity did not obscure content.

The same-tab `sessionStorage` cache saves Likes and cumulative timing every 250 ms and at lifecycle boundaries. A reload starts a fresh monotonic baseline, so elapsed reload/background time is not added. Native submissions persist completed feeds. There is no cross-device/closed-tab recovery guarantee; abrupt process termination can lose the last unsaved interval. A missing cache on a detected reload is explicitly marked incomplete. The component flushes on native Continue and submit without disabling or hiding native controls. Decipher owns navigation, validation and duplicate-submit handling. Failed validation does not leave the component locked. Double-clicked native Continue and completion reload produced one completed record in the native test.

Like buttons support keyboard activation and `aria-pressed`. A button’s additional clicks within 420 ms of the first click in a multi-click sequence are ignored; the guard is tracked per button, and distinct keyboard activations can toggle rapidly. Image double-clicks and paired touch taps share a 420 ms duplicate guard. Touch pairs must be within 340 ms and 25 pixels; canceled pointers clear the pair.

## Questra reusable template

Import [`questra-template.json`](questra-template.json) in Fine tuning. It has one shared base containing CSS/JS, the timing engine, photo/avatar references and content resources, server-side design loader, persistent assignment and initialization. The reusable `SocialFeed` component owns offer metadata, numeric timing fields, the Like matrix and its page break. Its only input is `task`, a required string enum `"1"`–`"5"`.

Render each task once, in order, in the `main` slot; for example `SocialFeed` with `{"task":"1"}`. Upload the bundled `.dat` as a system file and all 26 JPEGs as public/static files before compilation. Rendering tasks 1–5 reproduces `survey.xml` byte-for-byte with one shared CSS/JS pair; the bundled design bytes/hash match. The export passes Questra's transfer schema and actual component renderer, including invalid/missing task rejection. Regenerate for different counts or designs.

## Loading and frame boundaries

Revision 4 removes the old body class and every override of the survey body, frame width, progress, footer, unrelated questions and native navigation. Component CSS selectors are scoped to `.question.cf-feed`, its own `.question.cf-timing` storage question, or `.cf-init`. The native feed title and instructions remain in the same position before and after enhancement. Initialization and pre-enhancement use a still local card placeholder; photos have a fixed 4:3 media area and a local loading label. Cards do not wait for all images before becoming usable. There are no full-page overlays or forced native frame changes.

Revision 4 reduced the generated XML from approximately 3.4 MB to 78,439 bytes; revision 5 also reduces the native row count to 20 per feed. The old feed DOM contained about 12.9 MB of duplicated embedded image URLs; the new feed has small, cacheable native-static URLs. These are payload measurements, not a controlled network-speed benchmark. The initialization round trip remains necessary to save assignment before the first feed and is not eliminated.

## Verification and limits

Revision-5 verification completed all five native rounds with exactly 20 posts each: 16 organic and four Sponsored ads. All 40 design version/task groups meet those counts (800 design rows). The completed response matched all 100 rendered copy/image assignments, 900 native offer metadata cells, 100 Like states and 200 numeric timing/quality cells. Zero-Like rounds, multiple Likes, button/image double-clicks, keyboard undo, assignment/Like persistence after reload, double-clicked final Continue and completion reload passed; there was one completed record for the session. The genuine `.dat` and native XML readback matched exactly. The fine-tuning template passed the actual schema/renderer, reconstructing the exact XML with 20-row matrices and all 26 assets unchanged. Revision-4 frame/loading/responsive implementation is unchanged except for the revision-specific cache namespace.

Revision-4 live native checks covered initial entry, all five transitions, zero and multiple Likes, keyboard undo/repeated toggles on desktop, button/image double-clicks, reload persistence, visible native progress/navigation, double-clicked Continue and completion reload. A completed response matched all 150 Like states, 1,350 offer metadata cells, 300 timing/quality cells and 150 copy/author/offer/photo assignments. The 390 px native iframe retained its native margins, progress and Continue with no horizontal overflow. Photos not yet loaded remain unexposed under the rule.

A local fixture using the native component markup delayed photo responses by 15 seconds. It verified zero timing before photo readiness, positive timing after readiness, and identical card/media heights before and after loading. Ordinary fields before and after the component stayed visible, and the preceding field remained editable. This is a local fixture, not a live native validation test. Automatic approval review denied temporarily adding an ordinary required question to the testing survey because earlier instructions prohibited extra substantive questions; that variant was never uploaded. Native coexistence/validation with an additional ordinary question therefore remains untested.

Revision-3 checks additionally covered scroll exit/re-entry, a tall-card viewport, and a completed all-zero response; revision-4 focus and all-zero results are recorded in the local evidence package. Full browser evidence and raw exports stay local and are excluded from the reusable template/public-ready folder.

Ten deterministic tests cover partial/tall/horizontal intersections, zero-size/offscreen cards, repeated samples, disjoint visits, pause/re-entry, reload baselines, long gaps and timing states. Run `node tests/timing.cjs`.

A real background-tab transition remains a manual check: the automation browser reports owned tabs as visible/focused. The visibility gate is implemented; live focus and scroll pauses were verified. Physical touch gestures, Safari/Firefox, screen readers, blocked-storage recovery and network failures remain unverified. The public folder contains no credentials, response exports or private QA logs.

Implementation references: Forsta’s [static files and relative image references](https://forstasurveys.zendesk.com/hc/en-us/articles/4409476945947-Including-Static-Files-Images-JavaScript-CSS), [DCM design-file loading](https://forstasurveys.zendesk.com/hc/en-us/articles/4409469905307-Creating-a-Discrete-Choice-Model-DCM-Question), [single-select XML](https://forstasurveys.zendesk.com/hc/en-us/articles/4409476975899-Single-Select-Question-XML) and [style system](https://forstasurveys.zendesk.com/hc/en-us/articles/4409461374491-XML-Style-System); MDN's [Intersection Observer](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API), [Page Visibility](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API) and [monotonic performance clock](https://developer.mozilla.org/en-US/docs/Web/API/Performance/now).

## Full-card exposure measurement (ExposureRevision 1)

The existing TEST survey 2610210 additionally records two cumulative exposure durations, without changing the design assignment, Like codes, legacy `ms`/`state` fields, or visual interaction. These are display opportunities, **not attention**. No third-party tracking is used.

| Native numeric field (feed 2, position 7 example) | Definition |
| --- | --- |
| `ExposureRevision` | `1`: full-card geometry measurement schema. `DesignRevision` stays 5; creative identities are unchanged. |
| `Time2r7anyms` | Integer cumulative milliseconds with **at least 1% of the full card area** visible. “Any” excludes sub-1% edge slivers; it is not literally a single visible pixel. |
| `Time2r7halfms` | Integer cumulative milliseconds with **at least 50% of the full card area** visible. Unlike legacy `ms`, the denominator is not capped to viewport size. |
| `Time2r7exposurestate` | 0 = not initialized; 1 = instrumented zero; 2 = positive 1%-threshold time; 3 = incomplete lower bound; 4 = unsupported browser APIs. Uninitialized/unsupported durations are -1. Missing cells mean the feed was not submitted. |

Fields exist for organic posts as well as ads. Filter `Offer2r7kind=1` for sponsored ads. Join the same feed/row to `Offer2r7item` (stable assigned placement ID), `Offer2r7creative` (stable copy/image creative ID), `Offer2r7campaign`, `DesignRevision`, and `DesignVersion`. Aggregate a repeated creative across placements deliberately; distinct placements remain separate records.

The visible area intersects the card with the visual viewport and each ancestor's overflow clipping rectangle, independently by axis. Photo readiness, a visible document, and document focus are required. Two independent monotonic `performance.now()` meters sample on animation frames. An interval is counted only if both endpoints qualify and the gap is at most 250 ms; duplicate same-time samples add zero. Long qualifying gaps are omitted and flagged incomplete. Threshold crossings omit their boundary interval conservatively. Tall cards may never reach 50% in a small viewport; the 1% measure remains available. Milliseconds are floored only on native-field writes, so halfms never exceeds anyms.

Time accumulates across scroll exits and repeat exposures. Hidden tabs and blur pause both meters; pagehide, beforeunload, native Continue and form submit flush values. Resuming establishes a new baseline and never charges elapsed background time. Same-response, feed/version-specific sessionStorage retains totals every 250 ms. Reload/back navigation resumes the maximum of native and cached cumulative totals, rather than adding totals again; BFCache restoration resets the monotonic baseline. Missing cache on detected reload/back navigation, unavailable storage, image errors and long sampling gaps mark an incomplete lower bound. Storage and native submissions preserve numeric totals; no browser-only analytics payload is required. Abrupt process termination can lose the final unsaved interval.

CSS opacity, covering overlays/windows and cross-origin embedding occlusion are not measured. Frame sampling is an estimate rather than a certified viewability measurement. Physical phones and cross-browser behavior need separate validation.

ExposureRevision 1 verification (October 22, 2026): synthetic 1280×844 and 390×844 runs each completed all five feeds. At 25% visible, anyms increased while halfms stayed zero; both increased above 50%; both stopped offscreen and resumed on repeat exposure. Reload retained totals. Each completed native export contained all 300 new numeric exposure/quality cells, valid legacy Like codes and `ExposureRevision=1`; halfms never exceeded anyms. Example sponsored creative 13513 at placement 3 exported 7904/6162 ms (desktop) and 7965/6239 ms (mobile) for anyms/halfms. These are QA measurements, not research results. Exact deployed XML readback was verified. Fifteen deterministic tests cover legacy timing, strict full-card thresholds, nested-axis clipping, repeat exposure and lifecycle duplicate samples.

Automated headless and headed Chromium both reported owned tabs as visible/focused even after switching tabs. A real background-tab transition therefore remains an explicit manual validation limitation; it is not claimed as passed. The visibility lifecycle gate is separately exercised with a simulated hidden/visible document and verified to stop and resume accumulation. The actual native test exports and screenshots remain private in the local evidence folder, outside this repository.

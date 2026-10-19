# Verification and limitations

This is a synthetic example component, not a certification across browsers, devices or Decipher themes. Verification was performed against native test surveys; storage was read from the native response export, not a local mock or response-insertion API. Raw respondent exports, session data, internal tooling and browser captures are intentionally excluded from this repository.

## Latest completion revision

- Four-row and three-row native surveys compiled successfully.
- Native Continue remained in the original form with its normal click handler, but was hidden after successful enhancement.
- Intermediate choices stayed on the question page. Each choice selected its native radio before the animation completed.
- Rapid double-clicks on the final Like choice completed both surveys automatically, without manually clicking Continue.
- The deck was hidden before native Continue was invoked. The platform then displayed its completion page.
- Native exports contained exactly one completed record per test marker. Stored row codes were `[1,2,3,3]` for the four-row example and `[1,2,3]` for the three-row example.
- A temporary native server-validation rejection preserved all selected values and displayed the original editable matrix, enabled Continue and a review message. The deck stayed hidden and the component did not automatically resubmit. The temporary validation rule was removed afterward.
- Browser Back from the completed three-row survey returned to a fresh unanswered session without automatic submission. This does not establish saved-answer persistence.

The automatic-attempt latch, repeated-input guards, native invalid-event handler, saved-page re-entry handling and 12-second recovery watchdog were reviewed in source. The actual stalled-network and HTML-invalid recovery branches were not deliberately induced. JavaScript cannot restore a document that the browser has replaced with a network-error page.

## Gesture and fallback checks

Before the completion-only change, desktop Chrome checks verified below-threshold cancellation, left/right committed swipes, keyboard input, buttons and rapid duplicate-input protection. The gesture code did not change in the completion revision.

The 393×852 Chrome iPhone-emulated layout and keyboard activation of its answer buttons were verified. **Touch dragging of the polished gesture revision remains unverified.** Automated drag commands timed out; the same timeout occurred on ordinary question text outside the component. This identified an automation/emulation limitation, not a demonstrated component failure or a touch pass.

An earlier deliberate failure at component setup left the native matrix usable through completion. Fully disabling browser JavaScript encountered the platform's own JavaScript-required completion gate. Setup-failure fallback was not rerun for the latest completion-only change.

Physical iOS/Android devices, Safari, Firefox, screen-reader software and live reduced-motion emulation were not tested. Reduced-motion styling and accessible names, real buttons, status announcements and scoped shortcuts are implemented, but this is not an accessibility audit.

## Template checks

The Questra export passed the actual transfer-schema, component normalization/rendering, skeleton compilation and Decipher static checks. A variable three-row rendering also compiled natively. The current completion source and instructions were saved into an imported template.

An earlier AI template test produced and uploaded a native survey but failed its final automated assessment. The later presentation and completion updates were not rerun through the full AI pipeline. Do not interpret the native component verification as an all-green AI-workflow result.

## Suggested checks in your environment

1. Confirm every native row has exactly one radio selected, and Skip exports code 2 rather than missing data.
2. Exercise cancellation, left/right gestures, all three buttons and keyboard input on desktop and physical touch devices.
3. Confirm the last animation removes the deck and advances once through native handlers, including rapid repeated input.
4. Test native validation, saved-page re-entry and failed/stalled submission recovery.
5. Check your theme's markup and the native fallback. Keep this component alone on its page.

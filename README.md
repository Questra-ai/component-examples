# Component Examples Repository

Reusable survey component examples from Questra, organized by platform and component. Each example includes its own setup instructions, source files, and verification notes.

## Available examples

| Platform | Component | Description |
| --- | --- | --- |
| Decipher | [Swipe cards](decipher/swipe-cards/) | A native radio matrix presented as swipe cards, with Dislike, Skip and Like responses, shared CSS/JavaScript, and an importable Questra fine-tuning template. |
| Decipher | [Outfit selection](decipher/outfit-studio/) | Five native design-file tasks with clothing selection, optional hats, drag/snap interaction, and an importable Questra fine-tuning template. |

The swipe-card example includes [live synthetic demos](decipher/swipe-cards/#decipher-swipe-cards), [paste-ready survey XML](decipher/swipe-cards/survey.xml), a [Questra template export](decipher/swipe-cards/questra-template.json), and a screenshot. Read its verification notes before adapting it to a survey.

## Repository structure

Examples use lowercase platform folders and a separate folder for each component:

```text
<platform>/<component>/
```

Implemented examples are listed above. Future examples can use `decipher/`, `confirmit/`, `qualtrics/`, or another platform folder. Confirmit and Qualtrics examples are planned; none are implemented here yet. Platform folders are added when their first example is ready.

Link directly to an example's folder when sharing it:

https://github.com/Questra-ai/component-examples/tree/main/decipher/swipe-cards

This repository was renamed from `Questra-ai/decipher-swipe-cards` to keep the examples together while preserving its Git history. The original repository URL redirects here.

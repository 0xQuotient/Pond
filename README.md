# Pond

Hands-on social engineering labs, in the spirit of Hack The Box.

A social-engineering training range, modeled on HackTheBox but for people. You talk, persuade and pretext your way past AI-played targets instead of exploiting code.

## Modes

| Mode | What you do |
| --- | --- |
| Vishing | Live simulated phone call against one target. Get the secret before the timer or the target's suspicion runs out. |
| Spear phishing | Read a generated OSINT dossier, then write targeted emails to one person. |
| Mass phishing | Set up spoofed sender infrastructure, craft one lure, send it to a whole population, and chase the best click rate over up to five rounds. |

Each mode has several case files and five difficulty tiers (Recruit, Operator, Handler, Ghost, Impossible). Hints are opt-in and mark a clear as "assisted". After every run you get a debrief with the suspicion trail, the transcript, and optional coach notes.

## Scope

Everything is fictional: organizations, people, domains and dossiers are invented per run, and all infrastructure is simulated. Nothing is sent anywhere. This is a training game, not a phishing kit.

## How it runs

`index.html` is a single self-contained page written as a [Claude artifact](https://claude.ai). It relies on one thing the artifact runtime provides through `window.claude`:

- `sample`, which asks Claude to play the target, generate dossiers, simulate campaign results and write coach notes, on the viewer's own Claude account.

There is no leaderboard and no shared backend. Per-player profile and progress are stored in the browser's `localStorage`.

Outside claude.ai the AI features report "Claude isn't available in this view". To click through the whole UI locally with canned replies, build the standalone page with the dev shim:

```bash
python3 tools/build_standalone.py --mock
# then open dist/standalone.html in a browser
```

Without `--mock` the page loads but has no AI backend.

## Publishing as an artifact

Publish `index.html` as-is. It has no `<html>`, `<head>` or `<body>` wrapper on purpose, because the artifact host adds one. Declare the `sample` capability only.

## Tests

Headless flow tests cover navigation, mission setup, hints, timer, end screen, callsign changes and the campaign loop, against a fake `window.claude`:

```bash
pip install playwright
playwright install chromium
python3 tests/flow_test.py
```

## Known gaps

- The real model's behavior at the hardest tiers hasn't been tuned since moving to the artifact runtime's fast tier.
- The Mass Phishing composer and results screens have only been exercised with canned results.
- No license has been chosen yet.

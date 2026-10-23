# Pond

Hands-on social engineering labs. Talk, write and pretext your way past AI-played targets instead of exploiting code.

Pond is a single-page training game in the style of Hack The Box, built around people instead of machines. You pick a mission, work from a simulated workstation, and try to capture a flag from a target who has their own personality, suspicions and limits.

> Everything in Pond is fictional. Organizations, people, domains and dossiers are invented for each run, and all infrastructure is simulated. Nothing is sent anywhere. It is a training game, not a phishing kit.

## Contents

- [Modes](#modes)
- [Difficulty](#difficulty)
- [Ranks](#ranks)
- [Running it](#running-it)
- [Development](#development)
- [Project layout](#project-layout)
- [Roadmap](#roadmap)
- [License](#license)

## Modes

| Mode | Gear | Missions | What you do |
| --- | --- | --- | --- |
| Vishing | Lure | 5 | Run a live simulated phone call against one target and get the secret out of them. |
| Spear phishing | Spear | 3 | Read a generated OSINT dossier, then write targeted emails to one person. |
| Mass phishing | Net | 3 | Set up a spoofed domain and relay, write one lure, send it to a whole population and refine it over several rounds. |

Each mission opens in a browser workspace modeled on a pentest VM: a goal bar, tabs grouped by role (intel, workflow, reference), a side panel for the brief, and a main pane for the call, inbox or campaign tools.

Hints are opt-in. Using one marks the clear as "assisted". After each run you get a debrief with the transcript and optional coach notes.

## Difficulty

Five tiers, with fewer on-screen aids as you go up. The early tiers work like gutter bumpers: they keep you in the lane while you learn, then come off.

| Tier | Suspicion meter | Clock | Activity log | Campaign stats |
| --- | :---: | :---: | :---: | :---: |
| Recruit | yes | yes | yes | yes |
| Operator | no | yes | no | yes |
| Handler | no | no | no | no |
| Ghost | no | no | no | no |
| Impossible | no | no | no | no |

Hidden does not mean disabled. The timer and the suspicion score keep running, and the mission still ends when either runs out. Impossible adds a recon stage against a second linked contact before the main target.

## Ranks

Clearing missions raises your rank:

| Rank | Missions cleared |
| --- | ---: |
| Chum | 0 |
| Bobber | 3 |
| Reel Deal | 8 |
| Net Worth | 16 |
| Skipper | 26 |
| Kraken | 38 |
| Anglerfish | 55 |

## Running it

`index.html` is one self-contained file with no build step and no dependencies. It is written as a [Claude artifact](https://claude.ai) and uses one runtime API, `window.claude.sample`, to play the targets, generate dossiers, simulate campaign results and write coach notes on the viewer's own Claude account.

There is no backend and no leaderboard. Profile and progress are stored in the browser's `localStorage`.

**Inside claude.ai:** publish `index.html` as-is as an artifact and declare the `sample` capability only. The file deliberately has no `<html>`, `<head>` or `<body>` wrapper, because the artifact host adds one.

**Anywhere else:** the page loads, but the AI features show "Claude isn't available in this view". To click through the whole interface with canned replies, build the standalone page with the dev shim:

```bash
python3 tools/build_standalone.py --mock
```

Then open `dist/standalone.html` in a browser. Without `--mock` there is no AI backend.

## Development

Tests are headless browser flows run against a fake `window.claude`. They cover navigation, mission setup, hints, the timer, difficulty gating, the end screen, callsign changes and the campaign loop.

```bash
pip install playwright
playwright install chromium
python3 tests/flow_test.py
```

The suite prints `ALL OK` when everything passes.

## Project layout

```
index.html                 the whole app (HTML, CSS and JS)
tools/build_standalone.py  wraps index.html into a full page, optionally with the mock backend
tools/dev-shim.js          fake window.claude with canned replies
tests/flow_test.py         Playwright flow tests
```

## Roadmap

- Technical attack modes alongside the social ones, such as address poisoning, clickjacking and watering holes.
- A warning cue before the call ends when the clock is hidden.
- Tuning the hardest tiers against the real model.
- Screenshots in this README.

## License

None chosen yet, so all rights are reserved by default.

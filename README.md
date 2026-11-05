# Pond

Hands-on social engineering labs. Talk, write and pretext your way past AI-played targets instead of exploiting code.

Pond is a single-page training game in the style of Hack The Box, built around people instead of machines. You pick a mission, work from a simulated workstation, and try to capture a flag from a target who has their own personality, suspicions and limits.

> Everything in Pond is fictional. Organizations, people, domains and dossiers are invented for each run, and all infrastructure is simulated. Nothing is sent anywhere. It is a training game, not a phishing kit.

## Contents

- [How to play](#how-to-play)
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

## How to play

1. **Get it into Claude.** Pond needs Claude to run, so it is meant to live as a [Claude artifact](https://claude.ai). Create a new artifact, paste in the contents of `index.html`, and publish it. Details are under [Running it](#running-it).
2. **Pick a callsign.** Your profile and progress stay in your browser.
3. **Choose a mode, a mission and a difficulty,** then launch. The workspace opens with a goal bar, a brief, and the tools for that mode.
4. **Work the target.** Talk (vishing), write emails (spear phishing) or build and refine a campaign (mass phishing). Capture the flag before suspicion or the clock gets you.
5. **Read the debrief.** Review the transcript, then try a higher tier.

Shortcuts: `Enter` sends a call message, `Ctrl/Cmd+Enter` sends an email or launches a campaign round, and `Esc` cancels a pending "click again to confirm".

## Running it

`index.html` is one self-contained file with no build step and no dependencies. Every AI feature (the targets, dossiers, simulated campaign results and coach notes) goes through `window.claude.sample`, which only exists inside a Claude artifact and runs on the **viewer's own Claude account**. That is why Pond has no backend, no API keys and no hosting cost.

What that means in practice:

- **Players need a Claude account.** Nothing is billed to whoever publishes the artifact.
- **Publishing:** publish `index.html` as-is and declare the `sample` capability only. The file deliberately has no `<html>`, `<head>` or `<body>` wrapper, because the artifact host adds one.
- **Sharing:** artifacts are private until their owner shares them. Share the artifact link from its Share menu, not this repo, so people can play it.
- **This repo is the source.** Cloning it or opening `index.html` directly gives you the interface but no AI, and the page reports "Claude isn't available in this view".
- **No backend means no leaderboard.** Profile and progress live in the browser's `localStorage`, so clearing site data resets them.

To click through the whole interface offline with canned replies, build the standalone page with the dev shim:

```bash
python3 tools/build_standalone.py --mock
```

Then open `dist/standalone.html` in a browser. This is for development only. The replies are scripted, not played by a model.

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
- Tuning the hardest tiers against the real model.
- Screenshots in this README.
- Playing outside claude.ai would need either bring-your-own API key or a hosted backend. Both are deliberately out of scope for now.

## License

None chosen yet, so all rights are reserved by default.

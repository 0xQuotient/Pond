# Pond

Hands-on social engineering labs. Talk, write and pretext your way past AI-played targets instead of exploiting code.

**[Play Pond in your browser](https://claude.ai/artifact/Fqf5BNoawKYwFNBM2vUgLW)** (needs a free or paid Claude account).

Pond is a single-page training game in the style of Hack The Box, built around people instead of machines. You pick a mission, work from a simulated workstation, and try to capture a flag from a target who has their own personality, suspicions and limits.

> Everything in Pond is fictional. Organizations, people, domains and dossiers are invented for each run, and all infrastructure is simulated. Nothing is sent anywhere. It is a training game, not a phishing kit.

## Contents

- [How to play](#how-to-play)
- [Modes](#modes)
- [Difficulty](#difficulty)
- [Ranks](#ranks)
- [Running it](#running-it)
- [Development](#development)
- [Accessibility](#accessibility)
- [Security notes](#security-notes)
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

Everything happens in the browser. No install, no terminal.

**To just play:** open the [Pond link](https://claude.ai/artifact/Fqf5BNoawKYwFNBM2vUgLW) while signed in to Claude.

**To host your own copy:**
1. Open [`index.html`](index.html) here on GitHub and use the copy button.
2. In a Claude chat, ask: "Publish this as an artifact" and paste the code.
3. In the artifact, use **Share** to send the link to anyone with a Claude account.

Once you are in:
1. Pick a callsign. Your progress stays in your browser.
2. Choose a mode, a mission and a difficulty, then launch.
3. Work the target: talk (vishing), write emails (spear phishing) or build and refine a campaign (mass phishing). Capture the flag before suspicion or the clock gets you.
4. Read the debrief, then try a higher tier.

Shortcuts: `Enter` sends a call message, `Ctrl/Cmd+Enter` sends an email or launches a campaign round, and `Esc` cancels a pending "click again to confirm".

## Running it

`index.html` is one self-contained file with no build step and no dependencies. Every AI feature (the targets, dossiers, simulated campaign results and coach notes) goes through `window.claude.sample`, which only exists inside a Claude artifact and runs on the **viewer's own Claude account**. That is why Pond has no backend, no API keys and no hosting cost.

What that means in practice:

- **Players need a Claude account.** Nothing is billed to whoever publishes the artifact.
- **Publishing:** publish `index.html` as-is and declare the `sample` capability only. The file deliberately has no `<html>`, `<head>` or `<body>` wrapper, because the artifact host adds one.
- **Sharing:** artifacts are private until their owner shares them. Share the artifact link from its Share menu, not this repo, so people can play it.
- **This repo is the source.** Cloning it or opening `index.html` directly gives you the interface but no AI, and the page reports "Claude isn't available in this view".
- **No backend means no leaderboard.** Profile and progress live in the browser's `localStorage`, so clearing site data resets them.

Developers can click through the interface offline with canned replies; see [Development](#development).

## Development

This section is for contributors. Players do not need it.

To click through the interface offline with canned replies (scripted, not a real model), build the standalone page and open `dist/standalone.html`:

```bash
python3 tools/build_standalone.py --mock
```

Tests are headless browser flows run against a fake `window.claude`. They cover navigation, mission setup, hints, the timer, difficulty gating, the end screen, callsign changes and the campaign loop.

```bash
pip install playwright
playwright install chromium
python3 tests/flow_test.py
```

The suite prints `ALL OK` when everything passes.

## Accessibility

The navigation, mode cards, mission tabs and forms are reachable by keyboard with visible focus rings, new call messages are announced to screen readers, and animations switch off for people who prefer reduced motion. The layout is checked at phone width for sideways scrolling.

## Security notes

Pond was audited before its 1.0 release. What was checked and what to know:

- **Output escaping:** every piece of player input and model output is escaped before it reaches the page, including in HTML attributes. A test checks that a quote-and-tag payload stays inert.
- **No dynamic code:** no `eval`, `Function`, `document.write` or inline scripts built from data. The only external request is the Google Fonts stylesheet, which means Google sees the viewer's IP when the page loads.
- **No secrets and no network of its own:** there are no API keys, no backend, and no `fetch` calls. Model calls go through the artifact runtime.
- **Local storage only:** callsign, progress and settings are stored in the browser and parsed defensively. Nothing identifying is stored.
- **Prompt injection:** the player is the only user and the model only sees the player's own messages, so injecting the simulated target affects only that player's own run.
- **Misuse:** the game simulates phishing and vishing against invented targets. It sends nothing, registers no domains and contains no real brands, lists or infrastructure.

Found something? Open an issue on the repository.

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

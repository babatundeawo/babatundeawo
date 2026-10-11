# Customizing guide

Where to change things. Every file here can be edited on the GitHub website: open the file, click the pencil icon, then **Commit changes**.

## Text

All wording is in `README.md`. The headings, tables and lists are plain text. The few `<table>`, `<details>` and `<picture>` blocks are HTML: change the words between the tags and leave the tags themselves alone.

- **Add a project:** copy an existing row in the Projects tables and change the name, description and the two links.
- **Add a role:** copy an entry under **Experience** (use a `<details>` block for earlier roles).
- **Skills:** each skill is a word wrapped in backticks, for example `` `Python` ``.

## Banner and rotating tagline

Files: `assets/banner-light.svg`, `assets/banner-dark.svg`, `assets/tagline-light.svg`, `assets/tagline-dark.svg`. Visitors see the light or dark version to match their GitHub theme, so edit **both** of each pair.

Open an SVG and look for the `<text …>` lines near the bottom. Change the words between `>` and `</text>`. In the tagline files the four rotating lines are the four `<text>` lines near the end; keep them to roughly 70 characters so they fit.

## Colours

Colours are written as six-digit codes such as `#2DD4BF`. In the banner files the palette is repeated in the `stop-color`, `fill`, `stroke` and `.name` / `.sub` style lines.

| Role | Dark | Light |
| --- | --- | --- |
| Background | `#050A16` → `#0E3347` | `#F8FBFF` → `#CFE4F4` |
| Main text | `#F8FAFC` | `#0B1426` |
| Secondary text | `#B4C2D8` | `#33445F` |
| Teal accent | `#2DD4BF` | `#0F766E` |
| Sun | `#FBBF24` → `#F59E0B` | `#F59E0B` → `#D97706` |

To change a colour everywhere in a file, use the editor's find and replace (**Ctrl/Cmd + F**, then the replace option). Keep dark text on light backgrounds and light text on dark ones so the words stay readable.

The stat card colours are in the `THEMES` block of `.github/scripts/generate_stats.py`. After editing, run **Actions → Update profile stats → Run workflow** to redraw them.

## Fonts

The images use `Inter` when a visitor's device has it and fall back to the system font otherwise. GitHub does not allow web fonts inside profile images, so the font list in each SVG's `font-family` is the only setting.

## Images and credits

No photographs or third-party artwork are used. The banner, tagline and stat cards are drawn from scratch and belong to this repository. If you add an image, store it in `assets/`, give it descriptive alt text in the README and note any credit it requires.

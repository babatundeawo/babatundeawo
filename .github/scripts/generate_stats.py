#!/usr/bin/env python3
"""Builds the two profile stat cards (light and dark) in assets/.

Reads public repository data for the accounts listed in ACCOUNTS through the
GitHub REST API (authenticated with the workflow's built-in token) and writes
assets/stats-light.svg and assets/stats-dark.svg. Standard library only.

Run with --placeholder to write neutral cards that contain no numbers.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from xml.sax.saxutils import escape

ACCOUNTS = [
    ("users", "babatundeawo"),
    ("orgs", "techbaseng"),
    ("orgs", "kbischool"),
    ("orgs", "rccgkd"),
]
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
FONT = "Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0A1630", border="#2DD4BF", text="#F8FAFC", muted="#B4C2D8", track="#16284A", accent="#2DD4BF"),
    "light": dict(bg="#F4F8FD", border="#0F766E", text="#0B1426", muted="#33445F", track="#D5E2F2", accent="#0F766E"),
}
LANG_COLORS = {
    "HTML": "#E34F26", "CSS": "#2965F1", "JavaScript": "#F1C40F", "Python": "#3776AB",
    "TypeScript": "#3178C6", "Jupyter Notebook": "#DA5B0B", "Shell": "#4EAA25",
    "Fortran": "#734F96", "SCSS": "#C6538C", "Java": "#B07219",
}
FALLBACK_COLORS = ["#60A5FA", "#2DD4BF", "#FBBF24", "#A78BFA", "#F472B6", "#34D399"]


def fetch_repos(kind, name, token):
    """Return every public repository for one account, following pagination."""
    repos, page = [], 1
    while True:
        url = f"https://api.github.com/{kind}/{name}/repos?type=public&per_page=100&page={page}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-stats-generator",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            batch = json.load(resp)
        repos.extend(batch)
        if len(batch) < 100:
            return repos
        page += 1


def summarise(repos):
    """Collapse repository records into the numbers shown on the card."""
    own = [r for r in repos if not r.get("fork") and not r.get("archived")]
    langs = Counter(r["language"] for r in own if r.get("language"))
    return {
        "repos": len(own),
        "stars": sum(r.get("stargazers_count", 0) for r in own),
        "languages": langs.most_common(6),
    }


def card(theme, data, updated):
    t = THEMES[theme]
    metrics = [
        ("Public repositories", "—" if data is None else str(data["repos"])),
        ("Stars earned", "—" if data is None else str(data["stars"])),
        ("Accounts", str(len(ACCOUNTS))),
        ("Languages", "—" if data is None else str(len(data["languages"]))),
    ]
    parts = []
    for i, (label, value) in enumerate(metrics):
        x = 48 + i * 232
        parts.append(f'<text x="{x}" y="92" class="num">{escape(value)}</text>')
        parts.append(f'<text x="{x}" y="118" class="lbl">{escape(label)}</text>')
    bar, legend = [], []
    if data and data["languages"]:
        total = sum(c for _, c in data["languages"])
        x = 48.0
        for i, (lang, count) in enumerate(data["languages"]):
            w = 904 * count / total
            color = LANG_COLORS.get(lang, FALLBACK_COLORS[i % len(FALLBACK_COLORS)])
            bar.append(f'<rect x="{x:.1f}" y="150" width="{max(w - 3, 2):.1f}" height="10" rx="5" fill="{color}"/>')
            lx = 48 + (i % 3) * 300
            ly = 192 + (i // 3) * 24
            legend.append(f'<circle cx="{lx + 5}" cy="{ly - 5}" r="5" fill="{color}"/>'
                          f'<text x="{lx + 18}" y="{ly}" class="leg">{escape(lang)} · {count}</text>')
            x += w
    else:
        bar.append(f'<rect x="48" y="150" width="904" height="10" rx="5" fill="{t["track"]}"/>')
    foot = ("Refreshed automatically from public repositories." if data is None
            else f"Public repositories across 4 accounts · refreshed {updated}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="276" viewBox="0 0 1000 276" role="img" aria-labelledby="t">
  <title id="t">GitHub activity summary: public repositories, stars, accounts and top languages</title>
  <style>
    .num {{ font: 700 40px {FONT}; fill: {t["text"]}; letter-spacing: -1px; }}
    .lbl {{ font: 500 14px {FONT}; fill: {t["muted"]}; }}
    .leg {{ font: 500 14px {FONT}; fill: {t["text"]}; }}
    .foot {{ font: 500 12px {FONT}; fill: {t["muted"]}; }}
    .head {{ font: 600 12px {FONT}; letter-spacing: 2.5px; fill: {t["accent"]}; }}
  </style>
  <rect x="0.5" y="0.5" width="999" height="275" rx="16" fill="{t["bg"]}" stroke="{t["border"]}" stroke-opacity="0.35"/>
  <text x="48" y="44" class="head">GITHUB AT A GLANCE</text>
  {chr(10).join("  " + p for p in parts).strip()}
  <rect x="48" y="150" width="904" height="10" rx="5" fill="{t["track"]}"/>
  {"".join(bar)}
  {"".join(legend)}
  <text x="48" y="262" class="foot">{escape(foot)}</text>
</svg>
'''


def main():
    placeholder = "--placeholder" in sys.argv
    data = None
    if not placeholder:
        token = os.environ.get("GITHUB_TOKEN", "")
        repos = []
        for kind, name in ACCOUNTS:
            try:
                repos.extend(fetch_repos(kind, name, token))
            except (urllib.error.URLError, TimeoutError) as err:
                # Keep the previous cards rather than publishing partial numbers.
                print(f"Could not read {name}: {err}. Cards left unchanged.", file=sys.stderr)
                return 0
        data = summarise(repos)
    updated = datetime.now(timezone.utc).strftime("%d %b %Y")
    os.makedirs(OUT_DIR, exist_ok=True)
    for theme in THEMES:
        with open(os.path.join(OUT_DIR, f"stats-{theme}.svg"), "w", encoding="utf-8") as fh:
            fh.write(card(theme, data, updated))
    print("Stat cards written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

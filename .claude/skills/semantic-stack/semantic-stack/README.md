# semantic-stack

A Claude Code skill that automates a 5-step SEO article workflow for Swedish content:

1. **Term-extraktion** (NeuronWriter-style) — scrapes top 10 SERP, extracts entities and n-gram frequencies into `terms.json`
2. **Research** — full-text synthesis from the same sources with paragraph references, statistics and direct quotes
3. **Artikelplan** — Rank2Bank/Koray-methodology with semantic SEO principles and term coverage analysis
4. **Skriv artikeln** — Matyas Swedish SEO writing guidelines, target ≥85% min-term coverage
5. **Slutfil** — Markdown with frontmatter and full term coverage report

## Installation

Copy the entire `semantic-stack/` folder to your Claude Code skills directory:

| Platform | Target path |
|----------|-------------|
| **Windows** | `%USERPROFILE%\.claude\skills\semantic-stack\` |
| **macOS / Linux** | `~/.claude/skills/semantic-stack/` |

Once copied, Claude Code automatically loads the skill at next session start. Verify with `/semantic-stack` — Claude should recognize it.

## Requirements

### All platforms
- Claude Code (any version with skill support)
- Internet access for `WebSearch` and `WebFetch`

### Windows
- PowerShell (preinstalled on Windows 10/11) — used for `fetch.ps1`

### macOS / Linux
- `curl` (preinstalled on all Macs and most Linux distros)
- `perl` (preinstalled on all Macs and most Linux distros) — used for `fetch.sh`

### Optional but recommended
- **Playwright MCP plugin** for fetching JavaScript-rendered sites (e.g., government pages). Install via the Claude Code plugin marketplace. Without it, the skill falls back to `WebFetch` which produces lower-quality output for JS-heavy sites.

## Usage

The skill accepts four argument patterns, with progressively less manual input:

| Command | Intake | Pauses between steps |
| :--- | :--- | :--- |
| `/semantic-stack reavinstskatt gammalt hus` | Asks for site/audience/tone/length | Yes (5 approvals) |
| `/semantic-stack auto:reavinstskatt gammalt hus` | Asks for site/audience/tone/length | No (run-through) |
| `/semantic-stack teknikhajen.se reavinstskatt gammalt hus` | **Auto-detected from domain** | Yes (5 approvals) |
| `/semantic-stack auto:teknikhajen.se reavinstskatt gammalt hus` | **Auto-detected from domain** | No (run-through) |

The last option is **fire-and-forget**: zero questions, the skill detects the site profile from the domain and produces a finished article in one shot.

### How domain auto-detection works

When you provide a domain, the skill:

1. Fetches the homepage and 1–2 sample articles
2. Extracts site name, theme, audience, tone, typical length, internal-linking pattern
3. Builds a site profile and uses it as the source context for the article
4. Saves the profile as `./.semantic-stack-preset.json` so subsequent runs in the same project skip detection

### Intake resolution order

If no domain is given, the skill resolves intake in this priority:

1. `./.semantic-stack-preset.json` (saved profile from previous run in this project)
2. `~/.claude/skills/semantic-stack/.last-context.json` (cross-project memory, <30 days old)
3. Fresh intake question with four standard profiles (tech/sport/finance/custom)

### Internal links policy

By default the skill produces articles **without internal links**, even when domain auto-detection finds that the target site uses them. The reason: the skill has no access to the target site's full article inventory and cannot verify that guessed URLs exist. Fabricated internal links are worse than no internal links.

To opt in to internal-link suggestions, manually set `interna_lankar: true` in your `./.semantic-stack-preset.json`. The skill will then propose internal links marked as `<!-- TODO: verifiera URL -->` placeholders that you must verify before publishing.

## Folder structure

```
semantic-stack/
├── SKILL.md                          Main skill instructions (the brain)
├── README.md                         This file
├── references/
│   ├── matyas-seo-guidelines.md      Swedish SEO writing rules
│   ├── rank2bank-*.md / .txt         Koray Tugberk Gubur semantic SEO methodology
│   └── neuronwriter-example-{1,2,3}.json   Reference format for terms.json
├── scripts/
│   ├── fetch.ps1                     Windows/PowerShell HTML fetcher
│   └── fetch.sh                      Unix/Bash equivalent (curl + perl)
└── templates/
    └── frontmatter.md                YAML frontmatter template
```

## Language note

The skill is **optimized for Swedish content**:

- Instructions in `SKILL.md` are in Swedish
- Matyas guidelines are Swedish-language writing rules
- Reference examples are Swedish topics
- Default output targets Swedish SERP

If you want to produce content in another language, you can adapt by:
1. Translating `references/matyas-seo-guidelines.md`
2. Updating `SKILL.md` to instruct Claude to write in the target language
3. Replacing the Swedish NeuronWriter examples with examples in your language

## Limitations

- Term extraction is approximate (manual n-gram counting, not NLP-based). For commercial production verify with NeuronWriter or similar.
- Quality depends on top 10 SERP sources — if they're poor, the skill output will be too.
- The skill assumes you have permission to use Matyas and Rank2Bank methodology in your work — these are the original authors' frameworks adapted into reference material.

## Credits

- **Matyas** — original Swedish SEO writing guidelines
- **Koray Tuğberk Gübür** — holistic SEO / Rank2Bank methodology
- **NeuronWriter** — term extraction format reference

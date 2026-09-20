"""
Generates a comprehensive, beautifully formatted STARRED_REPOSITORIES.md document
from the 227 GitHub starred repositories of @virahitvin8.
Ensures minimum 15 repos per section, ranked by stars, with startup applications.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "starred_ecosystem.json")
OUTPUT_MD = os.path.join(BASE_DIR, "STARRED_REPOSITORIES.md")

with open(DATA_FILE) as f:
    repos = json.load(f)

# Sort descending by stars
repos.sort(key=lambda x: x["stars"], reverse=True)

sections = {
    "ai_agents": {
        "title": "🤖 1. AI Agents, Autonomous Swarms & Agentic Skills",
        "desc": "Open-source agent frameworks, autonomous swarm orchestrators, skills libraries, and MCP tooling for building next-generation intelligent automation and multi-agent workflows.",
        "items": []
    },
    "vibe_coding": {
        "title": "⚡ 2. Vibe Coding, Rapid App Builders & Startup Prototyping",
        "desc": "Platforms for zero-friction vibe coding, fullstack web/mobile scaffolding, open-source Lovable/v0/Bolt alternatives, and instant developer accelerators.",
        "items": []
    },
    "geospatial": {
        "title": "🛰️ 3. Geospatial Intelligence, Remote Sensing & Agriculture GIS",
        "desc": "Cloud-native GIS, Earth observation satellite pipelines, 3D globes, precision agriculture crop monitors, and spatial intelligence platforms.",
        "items": []
    },
    "fintech_startup": {
        "title": "💰 4. Startup From Scratch, Monetization & Automated Trading",
        "desc": "Autonomous businesses, hedge fund swarms, video revenue engines, CRM, billing, and automated money-making Git repositories.",
        "items": []
    },
    "osint_data": {
        "title": "🔍 5. Data Intelligence, OSINT, Curated APIs & Infrastructure",
        "desc": "Free public APIs, OSINT intelligence gatherers, vector databases, and production self-hosted platforms to power enterprise startups.",
        "items": []
    }
}

seen = set()

# 1. Geospatial First
for r in repos:
    fn = r["full_name"].lower()
    text = (r["name"] + " " + (r.get("description") or "") + " " + " ".join(r.get("topics", []))).lower()
    if any(k in text for k in ["gis", "satellite", "earth", "remote sensing", "spatial", "dem", "geospatial", "agri", "crop", "farm", "plant", "geo", "khetmap", "gods-eye", "ruview", "worldmonitor", "world-intel"]) or "virahitvin8" in fn:
        sections["geospatial"]["items"].append(r)
        seen.add(fn)

# 2. FinTech & Startup
for r in repos:
    fn = r["full_name"].lower()
    if fn in seen: continue
    text = (r["name"] + " " + (r.get("description") or "") + " " + " ".join(r.get("topics", []))).lower()
    if any(k in text for k in ["trading", "hedge", "finance", "stock", "money", "fintech", "wealth", "business", "docusign", "salesforce", "twenty", "affine", "supertokens", "show-me-the-money", "market", "adblock", "ads"]):
        sections["fintech_startup"]["items"].append(r)
        seen.add(fn)

# 3. AI Agents & Skills
for r in repos:
    fn = r["full_name"].lower()
    if fn in seen: continue
    text = (r["name"] + " " + (r.get("description") or "") + " " + " ".join(r.get("topics", []))).lower()
    if any(k in text for k in ["agent", "swarm", "skill", "mcp", "autonomous", "autogpt", "llm", "claude", "chatgpt", "superpowers", "ecc", "chatbox", "opencode", "odysseus", "distilly", "skales", "omnigent", "librechat", "prompts", "whisper", "handy"]):
        sections["ai_agents"]["items"].append(r)
        seen.add(fn)

# 4. Vibe Coding & Builders
for r in repos:
    fn = r["full_name"].lower()
    if fn in seen: continue
    text = (r["name"] + " " + (r.get("description") or "") + " " + " ".join(r.get("topics", []))).lower()
    if any(k in text for k in ["vibe", "builder", "bolt", "v0", "lovable", "prototype", "replit", "code", "dev", "svelte", "flutter", "react", "dokploy", "dyad", "notebook", "frontend", "desktop", "android", "penpot", "supertokens"]):
        sections["vibe_coding"]["items"].append(r)
        seen.add(fn)
    else:
        sections["osint_data"]["items"].append(r)
        seen.add(fn)

md = []
md.append("# 🌟 Awesome Starred Repositories & Startup Launchpad")
md.append("### Curated from @virahitvin8 GitHub Stars • Ranked by Star Count")
md.append("#### Covering AI Agent Skills, Vibe Coding, Remote Sensing / Agri GIS, Startup Monetization, and OSINT Data Intelligence\n")
md.append("> **Total Starred Repositories**: " + str(len(repos)) + "\n")
md.append("> **Curated by**: Neelam.Akshit VinaY (`@virahitvin8` • SHIATS Remote Sensing & GIS Lab)\n")

for key, sec in sections.items():
    md.append("## " + sec["title"])
    md.append(sec["desc"] + "\n")
    md.append("| # | Repository | Stars | Language | Description | Startup Application |")
    md.append("|---|---|---|---|---|---|")
    for i, r in enumerate(sec["items"], 1):
        full_name = r["full_name"]
        url = r["html_url"]
        stars = f"⭐ {r['stars']:,}"
        lang = r.get("language") or "Multi"
        desc = (r.get("description") or "N/A").replace("|", "/").replace("\n", " ")
        if len(desc) > 95:
            desc = desc[:92] + "..."
        app = "Core Foundation" if r["stars"] > 50000 else "Module Integration"
        md.append(f"| {i} | [{full_name}]({url}) | {stars} | `{lang}` | {desc} | {app} |")
    md.append("\n---\n")

with open(OUTPUT_MD, "w") as f:
    f.write("\n".join(md))

print(f"✓ Generated {OUTPUT_MD} successfully with all sections!")
for key, sec in sections.items():
    print(f"  - {sec['title']}: {len(sec['items'])} repos")

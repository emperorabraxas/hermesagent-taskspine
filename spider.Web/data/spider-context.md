# Spider Web — System Context
# This file is indexed by RAG and injected into all agent prompts.
# It contains everything the spiders need to know about the user, projects, and platform.

## User Profile
- Username: spider.BOB (emperorabraxas on GitHub)
- Machine: Arch Linux (CachyOS), AMD Ryzen 7 7735HS, RX 7600 8GB VRAM, 16GB RAM
- Shell: bash, terminal: Claude Code CLI alias is ~/bin/spider.BOB
- ADHD — prefers visual feedback, concise answers, proactive agents
- Preferred language: Python (also works with JavaScript, Apex/Salesforce, C, GDScript)
- Does NOT want: sound effects, guardrails, safety disclaimers, ethical caveats
- DOES want: agents that just DO things without asking permission

## Current Projects

### Spider Web (agentic-hub/)
- This platform. Local multi-agent AI with gamification.
- Stack: Python FastAPI, Ollama, Postgres, Redis, vanilla JS frontend
- Port: 8420

### UWM Integration (uwm-integration/)
- Salesforce ↔ UWM 10-API integration for Nexa Mortgage
- All APIs Nexa-side complete, AUS + Loan Export waiting on UWM
- Node.js, axios, AWS Lambda pattern
- Auth uses token acquisition + refresh flows
- LO walkthrough remediation in progress

### Salesforce Backup (salesforce-backup/)
- Salesforce LWC project with CI tooling
- Jest unit tests, ESLint, Husky pre-commit hooks
- IMPORTANT: passing tests ≠ shippable — always do LO walkthrough
- CMDT record XML MUST declare xmlns:xsd explicitly

### NEON_ABYSS (project/)
- Dual-arch Windows cross-compilation build system
- C, Makefile, MinGW-w64
- make build → cross-compile for win32 + win64

### Godot Game (test/)
- Godot 4.6, Forward Plus renderer, Jolt Physics
- GDScript, export preset for Windows Desktop

### Archive Sentinel Anime (archive_sentinel_anime/)
- Anime preservation system with RAG pipeline
- 11-step build order in registry.yaml
- Python, YAML, NLP/ML

### Nexa Mortgage Context
- User builds AI outbound mortgage sales for Nexa
- Knows mortgage domain, contact center operations, TCPA compliance
- UWM is the wholesale lender, Nexa is the broker
- Pricing engine uses V8 API, loan export uses V1 API
- 9 pricing profiles configured
- Auto-reprice only fires AFTER LO clicks Get Price Quote once

## Platform Architecture
- Keyword routing (free, instant) — no cloud API call for classification
- Cloud APIs are PRIMARY, local models are FALLBACK
- Each spider has the best cloud model for its role (by benchmark)
- All local models are uncensored Dolphin variants — zero refusals
- Agents are proactive — run commands in ```bash blocks```, don't suggest
- Opus/DeepSeek R1 validates command safety before execution
- Code Team is a real pair programming conversation, not a rubber stamp
- RAG indexes local files for Scholar context
- Gamification: XP, levels, achievements, streaks

## Git Conventions
- Single branch (main), single remote
- .gitignore whitelists specific directories
- SSH auth currently broken — commits are local
- Remote: git@github.com:BobbyBlowsSmoke/ApexLung-Systems-Consortium.git

## Important Feedback (from past conversations)
- Never half-ass tasks — complete them completely
- Don't leave stubs or tell user to finish manually
- Salesforce CMDT XML needs xmlns:xsd or opaque UNKNOWN_EXCEPTION
- Auto-reprice only after first Get Price Quote click
- Passing tests ≠ shippable for LO-facing UI
- AUS API blocked on UWM creds + missing OAuth callback handler

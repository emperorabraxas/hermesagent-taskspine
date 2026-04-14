#!/usr/bin/env bash
# Spider Web — One-command bootstrap
# Usage: bash scripts/setup.sh
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
DIM='\033[2m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}${BOLD}🕸  Spider Web — Setup${NC}"
echo ""

cd "$(dirname "$0")/.."

# 1. Python venv
echo -e "${DIM}[1/7] Python virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Created .venv${NC}"
else
    echo -e "${DIM}  Already exists${NC}"
fi
source .venv/bin/activate

# 2. Dependencies
echo -e "${DIM}[2/7] Installing dependencies...${NC}"
pip install -e . --quiet 2>/dev/null
echo -e "${GREEN}✓ Dependencies installed${NC}"

# 3. Docker (Postgres + Redis)
echo -e "${DIM}[3/7] Starting Docker containers...${NC}"
if command -v docker &>/dev/null; then
    docker compose up -d 2>/dev/null
    echo -e "${GREEN}✓ Postgres :5434 + Redis :6380${NC}"
else
    echo -e "${RED}  Docker not found — skip (gamification won't persist)${NC}"
fi

# 4. Database migrations
echo -e "${DIM}[4/7] Running migrations...${NC}"
if command -v docker &>/dev/null && docker ps | grep -q hub-postgres; then
    sleep 2  # Wait for Postgres to be ready
    alembic upgrade head 2>/dev/null && echo -e "${GREEN}✓ Database migrated${NC}" || echo -e "${RED}  Migration failed — run 'alembic upgrade head' manually${NC}"
else
    echo -e "${DIM}  Skipped (no Postgres)${NC}"
fi

# 5. Ollama models
echo -e "${DIM}[5/7] Pulling Ollama models...${NC}"
if command -v ollama &>/dev/null; then
    for model in "qwen2.5:7b" "llama3.1:8b" "phi3:latest" "mxbai-embed-large"; do
        if ollama list 2>/dev/null | grep -q "$(echo $model | cut -d: -f1)"; then
            echo -e "${DIM}  $model — already pulled${NC}"
        else
            echo -e "${CYAN}  Pulling $model...${NC}"
            ollama pull "$model" 2>/dev/null
            echo -e "${GREEN}  ✓ $model${NC}"
        fi
    done
else
    echo -e "${RED}  Ollama not found — install from https://ollama.com${NC}"
fi

# 6. .env file
echo -e "${DIM}[6/7] Environment config...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env from template${NC}"
    echo -e "${DIM}  Add API keys: hub setup${NC}"
else
    echo -e "${DIM}  .env already exists${NC}"
fi

# 7. Verify
echo -e "${DIM}[7/7] Verifying...${NC}"
if python3 -c "from agentic_hub.main import app; print('ok')" 2>/dev/null | grep -q ok; then
    echo -e "${GREEN}✓ Spider Web is ready${NC}"
else
    echo -e "${RED}  Import check failed — check errors above${NC}"
fi

echo ""
echo -e "${BOLD}${CYAN}🕸  Setup complete!${NC}"
echo ""
echo -e "  ${BOLD}hub serve${NC}     — Start API server"
echo -e "  ${BOLD}hub${NC}           — Start server + open browser"
echo -e "  ${BOLD}hub chat${NC}      — CLI chat REPL"
echo -e "  ${BOLD}hub index .${NC}   — Index files for RAG"
echo -e "  ${BOLD}hub setup${NC}     — Configure API keys"
echo ""

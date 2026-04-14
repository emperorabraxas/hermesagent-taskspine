#!/usr/bin/env bash
# spider.Web splash screen — cyber crawler greeting + system specs

RED='\033[0;31m'
BRED='\033[1;31m'
DIM='\033[2m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
PURPLE='\033[0;35m'
WHITE='\033[1;37m'
BONE='\033[0;37m'
NC='\033[0m'

# System info
CPU=$(grep -m1 "model name" /proc/cpuinfo | cut -d: -f2 | xargs)
GPU=$(lspci 2>/dev/null | grep -i vga | cut -d: -f3 | xargs | head -c 45)
GPU_VRAM=$(lspci -v 2>/dev/null | grep -A5 -i vga | grep -i "Memory.*prefetch" | grep -oP '\d+[MG]' | tail -1)
RAM_TOTAL=$(free -h | awk '/Mem:/{print $2}')
RAM_USED=$(free -h | awk '/Mem:/{print $3}')
SWAP_TOTAL=$(free -h | awk '/Swap:/{print $2}')
SWAP_USED=$(free -h | awk '/Swap:/{print $3}')
UPTIME=$(uptime -p 2>/dev/null | sed 's/up //')
KERNEL=$(uname -r)
OS=$(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d'"' -f2)
SHELL_VER=$(bash --version | head -1 | grep -oP '\d+\.\d+\.\d+')
PYTHON_VER=$(python3 --version 2>/dev/null | cut -d' ' -f2)
NODE_VER=$(node --version 2>/dev/null | tr -d 'v')
DISK_ROOT=$(df -h / 2>/dev/null | awk 'NR==2{print $3"/"$2" ("$5")"}')
DISK_HOME=$(df -h /home 2>/dev/null | awk 'NR==2{print $3"/"$2" ("$5")"}')
LOAD=$(cat /proc/loadavg | cut -d' ' -f1-3)
PROCS=$(nproc)
NET_IF=$(ip -4 route get 1.1.1.1 2>/dev/null | grep -oP 'dev \K\S+')
NET_IP=$(ip -4 addr show "$NET_IF" 2>/dev/null | grep -oP 'inet \K[\d.]+')
OLLAMA_MODELS=$(curl -s --max-time 1 http://localhost:11434/api/tags 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('models',[])))" 2>/dev/null || echo "offline")
SPIDER_STATUS=$(curl -s --max-time 1 http://localhost:8420/health 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','offline'))" 2>/dev/null || echo "offline")
DOCKER_CT=$(docker ps -q 2>/dev/null | wc -l)

echo -e ""
echo -e "${BRED}        ╲     ╱${NC}         ${WHITE}${OS}${NC}"
echo -e "${BRED}         ╲   ╱${NC}          ${DIM}Kernel${NC}   ${BONE}${KERNEL}${NC}"
echo -e "${BRED}    ╲     ╲ ╱     ╱${NC}     ${CYAN}CPU${NC}      ${BONE}${CPU}${NC}"
echo -e "${BRED}     ╲   ╱${WHITE}●${BRED}╲   ╱${NC}      ${CYAN}GPU${NC}      ${BONE}${GPU}${NC} ${DIM}${GPU_VRAM}${NC}"
echo -e "${BRED}      ╲╱${WHITE}●${NC} ${WHITE}●${BRED}╲╱${NC}       ${CYAN}RAM${NC}      ${BONE}${RAM_USED} / ${RAM_TOTAL}${NC} ${DIM}swap ${SWAP_USED}/${SWAP_TOTAL}${NC}"
echo -e "${BRED}      ╱╲${WHITE}●${NC} ${WHITE}●${BRED}╱╲${NC}       ${CYAN}Disk${NC}     ${BONE}/ ${DISK_ROOT}${NC}"
echo -e "${BRED}     ╱   ╲${WHITE}●${BRED}╱   ╲${NC}      ${CYAN}Load${NC}     ${BONE}${LOAD}${NC} ${DIM}(${PROCS} cores)${NC}"
echo -e "${BRED}    ╱     ╱ ╲     ╲${NC}     ${CYAN}Up${NC}       ${BONE}${UPTIME}${NC}"
echo -e "${BRED}         ╱   ╲${NC}          ${CYAN}Net${NC}      ${BONE}${NET_IP:-none}${NC} ${DIM}(${NET_IF:-?})${NC}"
echo -e "${BRED}        ╱     ╲${NC}         ${YELLOW}Python${NC}   ${BONE}${PYTHON_VER:-?}${NC}  ${YELLOW}Node${NC} ${BONE}${NODE_VER:-?}${NC}  ${YELLOW}Bash${NC} ${BONE}${SHELL_VER}${NC}"
echo -e "                          ${YELLOW}Ollama${NC}   ${BONE}${OLLAMA_MODELS} models${NC}  ${YELLOW}Docker${NC} ${BONE}${DOCKER_CT} containers${NC}"
echo -e "                          ${GREEN}Web${NC}      ${BONE}spider.Web ${SPIDER_STATUS}${NC}"
echo -e "                          ${DIM}spider.Web // 蜘蛛の巣${NC}"
echo -e ""

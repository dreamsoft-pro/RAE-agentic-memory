#!/bin/bash
# Auto-monitor CI tests with 30s interval
# Usage: ./scripts/ci/monitor_ci.sh <branch> [max_wait_minutes]

set -euo pipefail

BRANCH="${1:-develop}"
MAX_WAIT_MINUTES="${2:-10}"
CHECK_INTERVAL=30

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 CI Monitor for branch: $BRANCH${NC}"
echo -e "${BLUE}   Check interval: ${CHECK_INTERVAL}s | Max wait: ${MAX_WAIT_MINUTES}min${NC}"
echo ""

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) not found${NC}"
    exit 1
fi

START_TIME=$(date +%s)
MAX_WAIT_SECONDS=$((MAX_WAIT_MINUTES * 60))

while true; do
    # Get latest CI run
    RUN_DATA=$(gh run list --branch "$BRANCH" --limit 1 --json status,conclusion,databaseId,name 2>/dev/null || echo "[]")

    if [ "$RUN_DATA" = "[]" ]; then
        echo -e "${YELLOW}⚠️  No CI runs found for branch $BRANCH${NC}"
        exit 1
    fi

    STATUS=$(echo "$RUN_DATA" | jq -r '.[0].status')
    CONCLUSION=$(echo "$RUN_DATA" | jq -r '.[0].conclusion')
    RUN_ID=$(echo "$RUN_DATA" | jq -r '.[0].databaseId')
    RUN_NAME=$(echo "$RUN_DATA" | jq -r '.[0].name')

    ELAPSED=$(($(date +%s) - START_TIME))
    ELAPSED_MIN=$((ELAPSED / 60))

    echo -e "[$(date '+%H:%M:%S')] Run #$RUN_ID | Status: ${BLUE}$STATUS${NC}"

    if [ "$STATUS" = "completed" ]; then
        echo ""
        if [ "$CONCLUSION" = "success" ]; then
            echo -e "${GREEN}✅ CI PASSED!${NC}"
            echo -e "   Branch: $BRANCH"
            echo -e "   Run: $RUN_NAME (#$RUN_ID)"
            echo -e "   Time: ${ELAPSED_MIN}m ${ELAPSED}s"
            exit 0
        else
            echo -e "${RED}❌ CI FAILED!${NC}"
            echo -e "   Branch: $BRANCH"
            echo -e "   Run: $RUN_NAME (#$RUN_ID)"
            echo -e "   Conclusion: $CONCLUSION"
            echo ""
            echo -e "${YELLOW}📋 Fetching failed jobs...${NC}"

            # Show failed jobs
            gh run view "$RUN_ID" --json jobs | jq -r '.jobs[] | select(.conclusion != "success" and .conclusion != null) | "  ❌ \(.name): \(.conclusion)"'

            echo ""
            echo -e "${YELLOW}💡 View logs:${NC}"
            echo -e "   gh run view $RUN_ID --log-failed"
            echo ""
            echo -e "${YELLOW}💡 Rerun failed jobs:${NC}"
            echo -e "   gh run rerun $RUN_ID --failed"

            exit 1
        fi
    fi

    # Check timeout
    if [ $ELAPSED -ge $MAX_WAIT_SECONDS ]; then
        echo ""
        echo -e "${RED}⏱️  TIMEOUT: CI still running after ${MAX_WAIT_MINUTES} minutes${NC}"
        echo -e "   Run #$RUN_ID is still in progress"
        echo -e "   View status: gh run view $RUN_ID"
        exit 2
    fi

    # Wait before next check
    sleep $CHECK_INTERVAL
done

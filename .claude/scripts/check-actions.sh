#!/bin/bash

REPO="dreamsoft-pro/RAE-agentic-memory"

echo "🔍 GitHub Actions Status - $(date +%H:%M:%S)"
echo "================================================"
echo ""

# Pobierz ostatnie 3 runs
RUNS=$(gh run list --repo $REPO --limit 3 --json databaseId,status,conclusion,name,headBranch,createdAt,workflowName)

# Wyświetl w czytelnej formie
echo "$RUNS" | jq -r '.[] | "[\(.conclusion // .status)] \(.workflowName) (\(.headBranch)) - \(.createdAt)"'

echo ""
echo "---"
echo ""

# Szczegóły ostatniego runa
LAST_RUN=$(echo "$RUNS" | jq '.[0]')
RUN_ID=$(echo "$LAST_RUN" | jq -r '.databaseId')
CONCLUSION=$(echo "$LAST_RUN" | jq -r '.conclusion')
STATUS=$(echo "$LAST_RUN" | jq -r '.status')
NAME=$(echo "$LAST_RUN" | jq -r '.workflowName')

echo "📌 Ostatni workflow: $NAME"
echo "   Status: $STATUS"
echo "   Result: $CONCLUSION"
echo ""

# Jeśli failed - pokaż logi błędów
if [ "$CONCLUSION" = "failure" ]; then
    echo "❌ WYKRYTO BŁĘDY! Analiza logów..."
    echo ""
    gh run view $RUN_ID --repo $REPO --log | grep -A 5 -i "error\|failed\|✗"
    echo ""
    echo "💡 Pełne logi: gh run view $RUN_ID --repo $REPO --log"
    exit 1
elif [ "$CONCLUSION" = "success" ]; then
    echo "✅ Wszystko działa poprawnie!"
    exit 0
else
    echo "⏳ Workflow w trakcie wykonywania..."
    exit 2
fi
#!/usr/bin/env bash
set -e

# setup python environment
source .venv/bin/activate

# set python path
export PYTHONPATH=$(pwd)

# start server and log output to temp file
LOG_FILE=$(mktemp)
uv run python -m solution.app > "$LOG_FILE" 2>&1 &

# wait 5 seconds for server to start
sleep 5

# check /metrics endpoint
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/metrics)
if [ "$STATUS" -ne 200 ]; then
  echo "❌ /metrics returned $STATUS"
  pkill -f "python app.py"
  exit 1
fi
echo "✅ /metrics returned 200"

# check if logs contain a correlation_id
HAS_CORRELATION_ID=$(jq -r 'select(.correlation_id != null) | .correlation_id' "$LOG_FILE" | head -n1 || echo "")

if [ -z "$HAS_CORRELATION_ID" ]; then
  echo "❌ No correlation_id found in logs"
  pkill -f "python app.py"
  exit 1
fi

echo "✅ correlation_id found: $HAS_CORRELATION_ID"

# stop the server
pkill -f "python app.py"

# remove temp log file
rm "$LOG_FILE"

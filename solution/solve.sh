#!/usr/bin/env bash
set -e

# navigate to source environment
cd ..

# setup python environment
source .venv/bin/activate

# set python path
export PYTHONPATH=$(pwd)

# start server and log output to temp file
LOG_FILE=$(mktemp)
uv run python -m solution.app > "$LOG_FILE" 2>&1 &

# store server PID so we can kill it later
SERVER_PID=$!

# wait 5 seconds for server to start
sleep 5

# check /metrics endpoint
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/metrics)
if [ "$STATUS" -ne 200 ]; then
  echo "❌ /metrics returned $STATUS"
  kill $SERVER_PID
  exit 1
fi
echo "✅ /metrics returned 200"

# stop the server
kill $SERVER_PID

# remove temp log file
rm "$LOG_FILE"

exit
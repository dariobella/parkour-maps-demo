#!/bin/sh
FILE="/frontend/package.json"
cd /frontend
if [[ -f "$FILE" ]]; then
    npm install
    npm run dev
else
    echo "App folder is empty, keeping container alive for generation"
    while :; do sleep 1; done
fi

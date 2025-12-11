#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

mkdir -p "$ROOT_DIR/workspace/datasets"
if curl -fL -o "$ROOT_DIR/workspace/datasets/titanic.csv" https://calmcode.io/static/data/titanic.csv; then
    echo "downloaded titanic dataset."
else
    echo "failed to download titanic dataset." >&2
    exit 1
fi

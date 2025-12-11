#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

mkdir -p "$ROOT_DIR/workspace/datasets"
curl -o "$ROOT_DIR/workspace/datasets/titanic.csv" https://calmcode.io/static/data/titanic.csv
echo "downloaded titanic dataset."

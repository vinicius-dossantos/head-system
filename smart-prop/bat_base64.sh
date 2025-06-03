#!/bin/bash

SCRIPT_DIR="/Users/viniciussantos/Documents/GitHub/head-system/smart-prop/setup"

if [ ! -d "$SCRIPT_DIR" ]; then
  echo "❌ Directory not found: $SCRIPT_DIR"
  exit 1
fi

cd "$SCRIPT_DIR" || exit

for file in *.bat; do
  if [[ -f "$file" ]]; then
    base="${file%.bat}"
    b64file="${base}.b64"
    echo "📝 Converting $file to $b64file..."
    base64 -i "$file" -o "$b64file"
  fi
done

echo "✅ All .bat files converted to .b64."
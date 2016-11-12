#!/bin/bash

set -e

echo "Checking that all examples work."

cd ../examples
echo "Setting up path"
. ./setup_path.sh
for file in *.py
do
    echo "Testing example ${file}"
    python3 "${file}" debug
done

echo "All examples work"

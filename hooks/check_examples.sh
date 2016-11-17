#!/bin/bash

set -e

echo "*** RUNNING ALL EXAMPLES ***"

cd ../examples
echo "Setting up path"
. ./setup_path.sh quiet
for file in *.py
do
    echo "Testing example ${file}"
    python3 "${file}" debug || exit 1
done
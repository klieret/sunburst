#!/bin/bash

echo "sets the git hooks directory to this directory"
echo "Requires git >= 2.9"
echo "your git version:"
git --version
echo "let's try:"
git config core.hooksPath "$(pwd)"
echo "done"

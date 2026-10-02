#!/usr/bin/env bash
# Deploy script for Tinshed Roster.
#
# Runs the test suite, tags the release, and builds the Docker image.
# Usage: ./deploy/deploy.sh [version]   (defaults to v1.0.0)
set -euo pipefail

VERSION="${1:-v1.0.0}"

echo "== Running tests =="
python -m pytest

echo "== Tagging ${VERSION} =="
git tag -f "${VERSION}"
git push origin "${VERSION}"

echo "== Building Docker image =="
docker build -t "tinshed-roster:${VERSION}" .

echo "== Deploy finished =="
echo "Run locally with:"
echo "  docker run --rm tinshed-roster:${VERSION} --demo"

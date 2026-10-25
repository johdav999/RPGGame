#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Setup must have populated the pinned dependency sources first.
cmake --preset cloud
cmake --build --preset cloud --parallel "${CMAKE_BUILD_PARALLEL_LEVEL:-2}"
ctest --preset cloud
python3 -m unittest discover -s tests -v

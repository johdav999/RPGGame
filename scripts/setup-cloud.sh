#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Install system prerequisites in the environment before invoking this script.
for tool in git cmake ninja c++ python3; do
  command -v "$tool" >/dev/null || { echo "Missing prerequisite: $tool" >&2; exit 1; }
done
git submodule update --init --recursive
cmake --preset cloud
cmake --build --preset cloud --parallel "${CMAKE_BUILD_PARALLEL_LEVEL:-2}"
ctest --preset cloud
python3 -m unittest discover -s tests -v

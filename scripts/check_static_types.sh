#!/bin/bash

set -o errexit

echo "Removing old mypy cache"
rm -rf .mypy_cache 

echo "Running checks on tum_esm_utils/"
python -m mypy tum_esm_utils/

echo "Running checks on tests/"
python -m mypy tests/

#!/bin/bash

set -o errexit

rm docs/README.md
cp README.md docs/README.md

lazydocs --output-path ./docs/api-reference/ --src-base-url https://github.com/tum-esm/utils/tree/main/ --no-watermark tum_esm_utils

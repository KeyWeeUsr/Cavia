#!/bin/sh
set -ex
python -m pycodestyle \
    --ignore=dont \
    --show-source \
    --count \
    --max-line-length=79 \
    .

python -m pylint --jobs=0 setup.py cavia

python -m unittest discover \
    --failfast \
    --catch \
    --start-directory cavia/tests \
    --top-level-directory cavia
